'''
Created on 19.5.2013

@author: Jurex
'''
from reactor import component
from reactor.packet import Packet
from reactor import utils
from reactor.models.adapter import Adapter
from reactor.messages import events
from reactor.messages import commands
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
        Adapter.__init__(self)
        self.name = "EthernetAdapter"
        
    def receiver(self, socket, zmq_socket):

        config = component.get("Config")
        
        # bind udp listener
        interface = config.get('adapters.ethernet.interface', '0.0.0.0')
        port = config.get('adapters.ethernet.port', '4444')
        socket.bind((interface, port))
        
        logger.debug('Binded on port: ' + str(port))
        
        # send ready
        msg = events.AdapterReady()
        msg.src = self.name
        msg.dst = "Core"
            
        # send request to core
        zmq_socket.send(msg.to_json())
        
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
            msg = events.PacketReceived()
            msg.src = self.name
            msg.packet = packet.to_dict();
            
            # send request to core
            zmq_socket.send(msg.to_json())
            
    def sender(self, socket, zmq_socket):
        logger.debug('Waiting for messages to send')
        
        while True:
            msg_json = zmq_socket.recv()
            msg = utils.decode_message(msg_json)
            
            if(msg.__class__.__name__ == "PacketSend"):
                packet = Packet()
                packet.__dict__ = msg.packet
                
                addr = self.cache.get(packet.dst)
                if(addr == None):
                    logger.error("Address not found for device: " + packet.dst)
                    continue
                    
                address = addr.split(":")
                
                # send packet
                socket.sendto(packet.to_bytes(), (address[0], int(address[1])))
                logger.debug("Packet sent: " + packet.to_json() + " to: " + addr)
                continue
                
            logger.error("No action for message found!")
            
    def run(self):
        
        config = component.get("Config")
        # uncomment this if adapter is running in separate process
        #self.db = Database()
        
        # init cache // maybe better cache ?
        self.cache = Cache(self.name)
        #self.cache = {}
        
        self.zmq_context = zmq.Context()
        
        # create udp socket
        self.socket = socket(AF_INET,SOCK_DGRAM)
        
        # create zmq socket
        zmq_core_addr = config.get('core.zmq_addr')
        self.zmq_socket = self.zmq_context.socket(zmq.DEALER)
        self.zmq_socket.setsockopt(zmq.IDENTITY, self.name)
        self.zmq_socket.connect(zmq_core_addr)
        
        logger.debug('Adapter initlialized')
        
        # spawn green threads
        g1 = gevent.spawn(self.receiver, self.socket, self.zmq_socket)
        g2 = gevent.spawn(self.sender, self.socket, self.zmq_socket)
        
        # join threads
        gevent.joinall([g1,g2])
        
    

        