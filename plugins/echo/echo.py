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
    
    def run(self):
        
        # connect
        self.init()
        logger.info("Plugin started. PID: " + str(os.getpid()))
        counter = 0;
        
        while True:
            # blocking call to receive event
            event = self.eb_receive()
            logger.debug("Event Received: " + event.uuid)
            
            if(event.name  == "device.update"):
                counter = counter + 1
                
                # create command
                e = Event("device.push")
                e.data = event.data

                # send command
                self.eb_dispatch(e)
                