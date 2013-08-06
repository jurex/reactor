from reactor import log, component, event
from reactor.web.utils import JSONResponse
from reactor.components.plugin import Plugin


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
        log.info("plugin started: " + self.name)
        
        # register event handlers
        em = component.get("EventManager")
        em.registerEventHandler("MessageReceivedEvent", self.onMessageReceivedHandler)
    
    def stop(self):
        pass
    
    def shutdown(self):
        pass
    
    def onMessageReceivedHandler(self, source, message):
        self.history.append(message.toDictonary())
        log.debug("message added to history")