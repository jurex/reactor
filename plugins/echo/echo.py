from reactor import component
from reactor.components.plugin import Plugin

import logging
logger = logging.getLogger("EchoPlugin")

class EchoPlugin(Plugin):
    
    def __init__(self):
        self.name = "Echo"
        Plugin.__init__(self, self.name)
    
    def start(self):
        
        logger.info("Plugin started")
        
        # register event handlers
    
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
            logger.error("Device not found: %s ", src)