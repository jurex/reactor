from reactor import component
from reactor.managers.device import DeviceManager

import logging
logger = logging.getLogger("Core")

class Core(component.Component):
    def __init__(self):
        component.Component.__init__(self, "Core")
        
        self.id = 1
        self.address = 1
    
    def process(self, msg, src):
        if(msg.type == "event"):
            return self.process_event(msg)

        if(msg.type == "command"):
            return self.process_command(msg)
            
        raise NameError("Unknown message type")
    
    def process_event(self, msg):
        logger.debug("Processing event: " + msg.uuid)
    
    def process_command(self, msg):
        logger.debug("Processing command: " + msg.uuid)
    
    
    def onMessageReceived(self, message):
        
        # get source device
                
        dm = component.get("DeviceManager")
        device = dm.getDeviceByAddress(message.src)
        
        if (device == None):
            logger.debug("device not found: %s", message.src)
            
            # create new device
            # TODO: craete only device if association completed
            
            dm.register(message.src, message.adapter, None)
            

        # fire events
        em = component.get("EventManager")
        # em.fireEvent(MessageReceivedEvent(self, message))
    
    
        