from reactor import component

import logging
logger = logging.getLogger("Server")


class Server(object):
    def __init__(self, name):
        
        self.id = 1
        self.address = 1
        self.name = name
        
    def start(self):
        logger.info("virtual server started: " + self.name)
    
    def stop(self):
        logger.info("virtual server stopped: " + self.name)
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
      #  em.fireEvent(MessageReceivedEvent(self, message))
    
    
        