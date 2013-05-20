from reactor import log, component, event
from reactor.components.plugin import Plugin

class EchoPlugin(Plugin):
    
    def __init__(self):
        self.name = "Echo"
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
        
        # reply message
        src = message.src
        dst = message.dst
        
        message.src = dst
        message.dst = src
        
        devices = component.get("DeviceManager")
        device = devices.getDeviceByAddress(message.dst)
        
        if (device != None):
            device.send(message)
        else:
            log.error("Device not found: %s ", src)