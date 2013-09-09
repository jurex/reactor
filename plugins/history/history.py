from reactor import  component
from reactor.models.plugin import Plugin

import logging
logger = logging.getLogger("HistoryPlugin")

class HistoryPlugin(Plugin):
    
    def __init__(self):
        self.history = []
        Plugin.__init__(self, "HistoryPlugin")
        
    def run(self):
        logger.info("Plugin started")
        
        # register event handlers
    