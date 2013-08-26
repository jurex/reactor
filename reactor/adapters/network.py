'''
Created on 19.5.2013

@author: Jurex
'''
# packet definition
from reactor import component
from reactor.packet import Packet
from reactor.models.adapter import Adapter
from reactor.messages import events
from reactor.messages import commands

import logging
import zmq
import time

from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM

logger = logging.getLogger("NetworkAdapter")

class NetworkAdapter(Adapter):
    
    def __init__(self):
        
        config = component.get("Config")
        
        self.addresses = {} # dstAddress => ipAddress
        self.name = "NetworkAdapter"
        
        self.zmq_context = zmq.Context()
        self.zmq_addr = config.get('adapters.network.zmq_addr', 'tcp://127.0.0.1:6001')
        
        self.socket = socket(AF_INET,SOCK_DGRAM)
        
        # base class initialization
        
        logger.debug('Adapter initlialized')
        
    def receiver(self, socket):
        
        #time.sleep(2)
        
        config = component.get("Config")
        
        interface = config.get('adapters.network.interface', '0.0.0.0')
        port = config.get('adapters.network.port', '4444')
        zmq_core_request_addr = config.get('core.zmq_addr')
        
        
        socket.bind((interface, port))
        logger.debug('Network adapter binded on port: ' + str(port))
        
        
        zmq_socket = self.zmq_context.socket(zmq.DEALER)
        zmq_socket.setsockopt(zmq.IDENTITY, self.name)
        zmq_socket.connect(zmq_core_request_addr)
        
        # send ready
        msg = events.AdapterReady()
        msg.src = self.name
            
        # send request to core
        zmq_socket.send(msg.to_json())
        
        while True:
            # blocking read
            datagram, address = self.socket.recvfrom(1024) # buffer size is 1024 bytes
        
            # parse message
            packet = Packet()
            packet.unpack(datagram)
            #message.adapter = self
            
            logger.debug("Packet received: " + packet.to_string() + " ip: " + str(address))
            
            # create message
            msg = events.PacketReceived()
            msg.src = self.name
            
            # send request to core
            zmq_socket.send(msg.to_json())
            
            # wait for core response
            # zmq_socket.recv()
            
            logger.debug("Datagram processing finished")
            
    def sender(self, socket):
        logger.debug('Waiting for messages to send')
        
        config = component.get("Config")
        zmq_addr = config.get('adapters.network.zmq_addr')
        
        zmq_socket = self.zmq_context.socket(zmq.REP)
        zmq_socket.bind(zmq_addr)
        
        while True:
            data = zmq_socket.recv();
            print "Sending data: " + data
        
    def start(self):
        # start network adapter
        
        
        
        self.receiver_thread = Thread(target=self.receiver, args=(self.socket,))
        self.receiver_thread.start()
        
        self.sender_thread = Thread(target=self.sender, args=(self.socket,))
        self.sender_thread.start()
        
    def stop(self):
        pass
        
    def write(self, message):
        address = self.addresses.get(message.dst)
        if (address == None) : 
            logger.error("unknown dst IP address for device " + str(message.dst))
            raise Exception("unknown dst IP address for device " + str(message.dst))
        
        self.server.sendto(message.pack(), address)
        logger.debug("message sent: " + message.to_string() + " ip: " + str(address))
        self.messagesOut += 1
        
    def addAddress(self, src, address):
        addr = self.addresses.get(src)
        if (addr == None or addr != address):
            self.addresses[src] = address
            logger.debug('ip address registred: ' + str(src) + " = " + str(address))
            
    def to_dict(self):
        d = self.__dict__.copy()
        if( d.has_key("protocol")):
            d.pop("protocol") 
        return d

        
    

        