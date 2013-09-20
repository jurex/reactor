'''
Created on 19.5.2013

@author: Jurex
'''
# packet definition
from reactor import component
from reactor.packet import Packet
from reactor import utils
from reactor.models.adapter import Adapter
from reactor.messages import events
from reactor.messages import commands
from reactor.cache import Cache

import logging
import zmq
import time

from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM

logger = logging.getLogger("EthernetAdapter")

class EthernetAdapter(Adapter):
    
    def __init__(self):
        
        config = component.get("Config")
        
        self.name = "EthernetAdapter"
        self.cache = Cache(self.name)
        self.zmq_context = zmq.Context()
        self.zmq_addr = config.get('adapters.network.zmq_addr', 'tcp://127.0.0.1:6001')
        
        # create udp socket
        self.socket = socket(AF_INET,SOCK_DGRAM)
        
        # create zmq socket
        zmq_core_addr = config.get('core.zmq_addr')
        self.zmq_socket = self.zmq_context.socket(zmq.DEALER)
        self.zmq_socket.setsockopt(zmq.IDENTITY, self.name)
        self.zmq_socket.connect(zmq_core_addr)
        
        logger.debug('Adapter initlialized')
        
    def receiver(self, socket, zmq_socket):
        
        #time.sleep(2)
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
            #message.adapter = self
            
            # update address cache
            if(packet.src not in self.cache):
                self.cache[packet.src] = str(address[0])+":"+str(address[1])
                logger.debug('IP address registred: ' + str(packet.src) + " = " + str(address[0])+":"+str(address[1]))
            
            logger.debug("Packet received: " + packet.to_string() + " ip: " + str(address))
            
            # create message
            msg = events.PacketReceived()
            msg.src = self.name
            msg.packet = packet.to_dict();
            
            # send request to core
            zmq_socket.send(msg.to_json())
            
            # wait for core response
            # zmq_socket.recv()
            
            #logger.debug("Datagram processing finished")
            
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
                logger.debug("Sending packet: " + packet.to_json() + " to: " + addr)
                socket.sendto(packet.to_bytes(), (address[0], int(address[1])))
                continue
                
            logger.error("No action for message found!")
            
        
    def start(self):
        # start adapter threads
        self.receiver_thread = Thread(target=self.receiver, args=(self.socket,self.zmq_socket,))
        self.receiver_thread.start()
        
        self.sender_thread = Thread(target=self.sender, args=(self.socket,self.zmq_socket,))
        self.sender_thread.start()
        
    def stop(self):
        pass
            
    def to_dict(self):
        d = self.__dict__.copy()
        if( d.has_key("protocol")):
            d.pop("protocol") 
        return d

        
    

        