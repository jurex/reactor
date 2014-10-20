from reactor import component
from reactor.packet import Packet
from reactor.models.adapter import Adapter
from reactor.eventbus import ZMQCEventBus
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
        self.ready = False;
        
    def init(self):
        # init eventbus
        self.eventbus = ZMQCEventBus(self.name)

        # notify core
        event = Event("plugin.ready")        
        self.eventbus.dispatch(event)
   
    def shutdown(self):
        pass
