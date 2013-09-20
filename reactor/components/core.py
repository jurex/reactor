from reactor import component
from reactor.managers.device import DeviceManager
from reactor.messages import events
from reactor.messages import commands
from reactor.packet import Packet

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
    
    def process_event(self, event):
        logger.debug("Processing event: " + event.uuid)
        
        plugins = component.get("PluginManager")
        devices = component.get("DeviceManager")
        
        # set plugin as ready
        if(event.__class__.__name__ == "PluginReady"):
            plugin = plugins.get(event.src)
            plugin.ready = True;
        
        # packet received 
        if(event.__class__.__name__ == "PacketReceived"):
            
            packet = Packet()
            packet.__dict__ = event.packet
            
            # dispatch packet event
            self.dispatch_event(event)
            
            msg = events.DeviceUpdated()
            msg.src = "Core"
            msg.device = packet.src
            msg.data = packet.data
            
            # dispatch device updated event
            self.dispatch_event(msg)        
        
        
    def dispatch_event(self, msg):
        router = component.get("Router")
        plugins = component.get("PluginManager")
        
        # dispatch event to all plugins except sender
        for plugin in plugins:
            msg.src = "Core"
            msg.dst = plugin.name
            if(msg.src != msg.dst and plugin.ready == True):
                router.send(msg, msg.dst)
    
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
    
    
        