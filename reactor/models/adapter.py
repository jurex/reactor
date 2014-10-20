from threading import Thread
from multiprocessing import Process

from reactor.eventbus import ZMQCEventBus
from reactor.event import Event

class Adapter(Thread):
    def __init__(self, name):
        Thread.__init__(self)

        self.name = name
        self.ready = False

    def init(self):
      # init eventbus
      self.eventbus = ZMQCEventBus(self.name)

      # notify core
      event = Event("adapter.ready")        
      self.eventbus.dispatch(event)
   
    def shutdown(self):
        pass