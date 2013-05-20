from reactor import log, component, event
from reactor.components.plugin import Plugin

class HistoryPlugin(Plugin):
    
    def __init__(self):
        self.name = "History"
        self.history = []
        Plugin.__init__(self, self.name)
    
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
        self.history.append(message)
        log.debug("message added to history")