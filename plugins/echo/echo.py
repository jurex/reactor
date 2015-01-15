from reactor import component
from reactor import utils
from reactor.models.plugin import Plugin
from reactor.event import Event

import os

import logging
logger = logging.getLogger("EchoPlugin")

class EchoPlugin(Plugin):
    
    def __init__(self):
        Plugin.__init__(self, "@echo")
    
    def run2(self):
        
        # connect
        self.init()
        logger.info("Plugin started. PID: " + str(os.getpid()))
        counter = 0;
        
        while True:
            # blocking call to receive event
            event = self.eventbus.receive()
            logger.debug("Event received: " + event.to_json())
            
            if(event.name  == "device.update"):
                counter = counter + 1
                
                # create command
                e = Event("device.push")
                e.data = event.data

                # send command
                self.eventbus.dispatch(e)


    def run(self):
        # connect
        self.init()
        logger.info("Plugin started. PID: " + str(os.getpid()))
        counter = 0;

        self.eventbus.subscribe("core")
        self.eventbus.subscribe("adapter")
        self.eventbus.subscribe("plugin")

        for event in self.eventbus.listen():

            logger.debug("Event received: " + event.to_json())
            
            if(event.name  == "device.update"):
                counter = counter + 1
                
                # create command
                e = Event("device.push")
                e.data = event.data

                # send command
                # self.eventbus.dispatch(e)
                self.eventbus.publish(e, "plugin")
                