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

from Queue import Queue

import traceback
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

        self.rq = Queue()

    def publisher(self):
        counter = 0

        while True:
            datagram, address = self.rq.get()
            logger.debug("Packet received: " + datagram + " from ip: " + str(address))

            # parse packet
            try:
            
                packet = Packet()
                packet.from_json(datagram)

            except Exception, err:
                logger.error("could not parse packet: " +  str(datagram) + " : " + str(err))
                logger.debug(traceback.format_exc())
                continue
        
            # create event
            event = Event("device.update")
            event.src = self.name
            event.data = packet.data

            # logger.debug("publish counter: " + str(counter))

            # publish event
            self.eventbus.publish(event, "adapter")

        
    def receiver(self, socket):

        config = component.get("Config")
        
        # bind udp listener
        interface = config.get('adapters.ethernet.interface', '0.0.0.0')
        port = config.get('adapters.ethernet.port', '4444')
        socket.bind((interface, port))
        
        logger.debug('Binded on port: ' + str(port))
        counter = 0
        
        while True:
            # blocking read
            datagram, address = socket.recvfrom(1024) # buffer size is 1024 bytes
        
            # parse message
            #packet = Packet()
            #packet.unpack(datagram)

            # counter = counter + 1

            #print("receiver counter: " + str(counter))
            
            #logger.debug("Packet received: " + datagram + " from ip: " + str(address))

            # put datagram to queue
            self.rq.put([datagram, address])
             
            # update address cache
            #if(packet.src not in self.cache):
            #    self.cache[packet.src] = str(address[0])+":"+str(address[1])
            #    logger.debug('IP address registred: ' + str(packet.src) + " = " + str(address[0])+":"+str(address[1]))
            #elif(self.cache[packet.src] != str(address[0])+":"+str(address[1])):
            #    self.cache[packet.src] = str(address[0])+":"+str(address[1])

            # create message
            #event = Event("device.update")
            #event.src = self.name
            #event.data = datagram

            # send event to core
            # self.eventbus.dispatch(event)

            # publish event
            #self.eventbus.publish(event, "adapter")

            
    def sender(self, socket):
        logger.debug('Waiting for events')
        
        # subscribe
        self.eventbus.subscribe("core")
        self.eventbus.subscribe("plugin")

        # listen for events
        for event in self.eventbus.listen():

            logger.debug("Event received: " + event.to_json())

            if(event.name == "device.push"):
                
                packet = Packet()
                packet.dst = 125
                packet.src = 1
                packet.cmd = event.name
                packet.data = event.data

                #logger.debug("packet to send: " + packet.to_json())
                
                #addr = self.cache.get(packet.dst)
                #if(addr == None):
                #    logger.error("Address not found for device: " + str(packet.dst))
                #    continue
                    
                # address = addr.split(":")
                address = ["192.168.1.1", 4444]
                
                # send packet
                socket.sendto(packet.to_json(), (address[0], int(address[1])))
                logger.debug("Packet sent: " + packet.to_json() + " to: " + str(address))
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
        self.socket.setsockopt(SOL_SOCKET, SO_RCVBUF, 1024 * 1024 * 16)
        
        self.init()
        logger.debug('Adapter initlialized')
        
        # spawn green threads
        g0 = gevent.spawn(self.publisher)
        g1 = gevent.spawn(self.receiver, self.socket)
        g2 = gevent.spawn(self.sender, self.socket)

        
        # join threads
        gevent.joinall([g0,g1,g2])       