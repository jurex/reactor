from reactor import  component
from reactor.models.plugin import Plugin
from reactor import utils
import os
import logging

logger = logging.getLogger("HistoryPlugin")

class HistoryPlugin(Plugin):
    
    def __init__(self):
        self.history = []
        Plugin.__init__(self, "@history")
        
    def run(self):
        
        # initialize
        self.init()

        logger.info("Plugin started. PID: " + str(os.getpid()))

        # subscribe
        self.eventbus.subscribe("core")
        self.eventbus.subscribe("adapter")
        self.eventbus.subscribe("plugin")

        for event in self.eventbus.listen():
            logger.debug("Event received: " + event.to_json())

        
        #while True:
        #    event = self.eventbus.receive()
        #    logger.debug("Event received: " + event.to_json())
    