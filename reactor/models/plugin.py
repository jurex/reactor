from reactor import component
from reactor.packet import Packet
from reactor.models.adapter import Adapter
from reactor.messages import events
from reactor.messages import commands

from threading import Thread

import logging
import zmq

class Plugin(Thread):
    
    def __init__(self, name):
        self._name = name
        self._state = "Stopped"
        
        config = component.get("Config")
        
        self.zmq_context = zmq.Context()
        self.zmq_addr = config.get('adapters.network.zmq_addr', 'tcp://127.0.0.1:6001')
        
        # create zmq socket
        zmq_core_addr = config.get('core.zmq_addr')
        self.zmq_socket = self.zmq_context.socket(zmq.DEALER)
        self.zmq_socket.setsockopt(zmq.IDENTITY, self._name)
        self.zmq_socket.connect(zmq_core_addr)
        
        Thread.__init__(self)
        

    
    