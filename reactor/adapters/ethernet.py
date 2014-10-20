'''
Created on 19.5.2013

@author: Jurex
'''
from reactor import component
from reactor.packet import Packet
from reactor import utils
from reactor.models.adapter import Adapter
from reactor.event import Event
from reactor.cache import Cache
from reactor.components.database import Database

import logging
import time

#import zmq
import zmq.green as zmq

import gevent
import gevent.monkey

gevent.monkey.patch_socket()

from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_RCVBUF

logger = logging.getLogger("EthernetAdapter")


class EthernetAdapter(Adapter):
    
    def __init__(self):
        Adapter.__init__(self, "#ethernet")
        
    def receiver(self, socket):

        config = component.get("Config")
        
        # bind udp listener
        interface = config.get('adapters.ethernet.interface', '0.0.0.0')
        port = config.get('adapters.ethernet.port', '4444')
        socket.bind((interface, port))
        
        logger.debug('Binded on port: ' + str(port))
        
        while True:
            # blocking read
            datagram, address = socket.recvfrom(1024) # buffer size is 1024 bytes
        
            # parse message
            packet = Packet()
            packet.unpack(datagram)
            
            logger.debug("Packet received: " + packet.to_string() + " from ip: " + str(address))
             
            # update address cache
            if(packet.src not in self.cache):
                self.cache[packet.src] = str(address[0])+":"+str(address[1])
                logger.debug('IP address registred: ' + str(packet.src) + " = " + str(address[0])+":"+str(address[1]))
            elif(self.cache[packet.src] != str(address[0])+":"+str(address[1])):
                self.cache[packet.src] = str(address[0])+":"+str(address[1])


            # create message
            event = Event("device.update")
            event.src = self.name
            event.data = packet.to_dict()

            # send event to core
            self.eventbus.dispatch(event)
            
    def sender(self, socket):
        logger.debug('Waiting for events')
        
        while True:
            event = self.eventbus.receive()
            logger.debug("Event received: " + event.to_json())

            if(event.name == "device.push"):
                packet = Packet()
                packet.__dict__ = event.data
                packet.dst = packet.src
                packet.src = 1

                logger.debug("packet to send: " + packet.to_json())
                
                addr = self.cache.get(packet.dst)
                if(addr == None):
                    logger.error("Address not found for device: " + str(packet.dst))
                    continue
                    
                address = addr.split(":")
                
                # send packet
                socket.sendto(packet.to_bytes(), (address[0], int(address[1])))
                logger.debug("Packet sent: " + packet.to_json() + " to: " + addr)
                continue
            
    def run(self):
        
        config = component.get("Config")
        # uncomment this if adapter is running in separate process
        #self.db = Database()
        
        # init cache // maybe better cache ?
        self.cache = Cache(self.name)
        #self.cache = {}
        
        # create udp socket
        self.socket = socket(AF_INET,SOCK_DGRAM)
        
        self.init()
        logger.debug('Adapter initlialized')
        
        # spawn green threads
        g1 = gevent.spawn(self.receiver, self.socket)
        g2 = gevent.spawn(self.sender, self.socket)
        
        # join threads
        gevent.joinall([g1,g2])       