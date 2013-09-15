from reactor import  component
from reactor.models.plugin import Plugin
from reactor import utils
import os

import logging
logger = logging.getLogger("HistoryPlugin")

class HistoryPlugin(Plugin):
    
    def __init__(self):
        self.history = []
        Plugin.__init__(self, "HistoryPlugin")
        
    def run(self):
        
        # connect
        self.connect()
        logger.info("Plugin started. PID: " + str(os.getpid()))
        
        while True:
            msg = self.receive()
            
            #logger.debug("Message Received: " + msg.to_json())
    