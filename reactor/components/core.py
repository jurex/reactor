from reactor import component
from reactor.managers.device import DeviceManager

import logging
logger = logging.getLogger("Core")

class Core(component.Component):
    def __init__(self):
        component.Component.__init__(self, "Router")
        
        self.id = 1
        self.address = 1
        self.device_manager = DeviceManager()
        
    def get_device_manager(self):
        return self.device_manager
        
    def start(self):
        logger.info("Started: " + self.name)
    
    def stop(self):
        logger.info("Stopped: " + self.name)
        pass
    
    def process(self, msg):
        pass
    
    def process_event(self, msg):
        pass
    
    def process_command(self, msg):
        pass
    
    
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
    
    
        