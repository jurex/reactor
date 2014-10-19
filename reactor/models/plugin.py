from reactor import component
from reactor.packet import Packet
from reactor.models.adapter import Adapter
from reactor.event import Event
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
        
    def init(self):
        # connect to event bus
        self.eb_connect()

        # notify core
        event = Event("plugin.ready")        
        
        # dispatch event to core
        self.eb_dispatch(event)

    # EVENT BUS subsystem

    def eb_connect(self):
        return self.zmq_connect()

    def eb_disconnect(self):
        return self.zmq_disconnect()
        
    def eb_receive(self):
        return self.zmq_receive()

    def eb_dispatch(self, event):
        return self.zmq_dispatch(event)

    # ZMQ subsystem

    def zmq_connect(self):
        self.zmq_context = zmq.Context()
        
        # create zmq socket
        config = component.get("Config")
        zmq_core_addr = config.get('core.zmq_addr')
        self.zmq_socket = self.zmq_context.socket(zmq.DEALER)
        self.zmq_socket.setsockopt(zmq.IDENTITY, self.name)
        return self.zmq_socket.connect(zmq_core_addr)

    def zmq_disconnect(self):
        pass

    def zmq_receive(self):
        obj = self.zmq_socket.recv()
        event = Event()
        event.from_json(obj)
        return event

    def zmq_dispatch(self, event):
        event.src = self.name
        return self.zmq_socket.send_unicode(event.to_json())
        

        
        

    
    