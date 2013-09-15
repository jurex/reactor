from reactor import component
from reactor.packet import Packet
from reactor.models.adapter import Adapter
from reactor.messages import events
from reactor.messages import commands
from reactor import utils

from threading import Thread
from multiprocessing import Process

import logging
import zmq

class Plugin(Thread):
    
    def __init__(self, name):
        Thread.__init__(self)
        
        self.name = name
        # self.state = "Stopped"
        self.ready = False;
        
        
    def connect(self):
        config = component.get("Config")
        
        self.zmq_context = zmq.Context()
        self.zmq_addr = config.get('adapters.network.zmq_addr', 'tcp://127.0.0.1:6000')
        
        # create zmq socket
        zmq_core_addr = config.get('core.zmq_addr')
        self.zmq_socket = self.zmq_context.socket(zmq.DEALER)
        self.zmq_socket.setsockopt(zmq.IDENTITY, self.name)
        self.zmq_socket.connect(zmq_core_addr)
        
        # send ready
        msg = events.PluginReady()
        msg.src = self.name
        msg.dst = "Core"
            
        # send request to core
        self.zmq_socket.send_unicode(msg.to_json())
        
    def send(self, msg):
        return self.zmq_socket.send_unicode(msg.to_json())
        
    def receive(self):
        msg_json = self.zmq_socket.recv()
        return utils.decode_message(msg_json)
        
        

    
    