from reactor import  component
from reactor.web.utils import JSONResponse
from reactor.components.plugin import Plugin

import logging
logger = logging.getLogger("HistoryPlugin")

class HistoryPlugin(Plugin):
    
    def __init__(self):
        self.name = "History"
        self.history = []
        Plugin.__init__(self, self.name)
        
        
        #app = component.get('API').app

        #@app.route('/history', methods=['GET'])
        #@login_required
        #def get_history():
        #   return JSONResponse(self.history)
    
    def start(self):
        logger.info("Plugin started")
        
        # register event handlers
    
    def stop(self):
        pass
    
    def shutdown(self):
        pass
    
    def onMessageReceivedHandler(self, source, message):
        self.history.append(message.to_dict())
        logger.debug("message added to history")