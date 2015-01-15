from threading import Thread
from multiprocessing import Process

from reactor.eventbus import ZMQEventBus
from reactor.eventbus import RedisEventBus
from reactor.event import Event

class Adapter(Thread):
    def __init__(self, name):
        Thread.__init__(self)

        self.name = name
        self.ready = False

    def init(self):
      # init eventbus
      self.eventbus = RedisEventBus(self.name)

      # notify core
      event = Event("adapter.ready")        
      #self.eventbus.dispatch(event)
      self.eventbus.publish(event, "adapter")
   
    def shutdown(self):
        pass