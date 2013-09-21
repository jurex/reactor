from reactor import component
from reactor.managers.device import DeviceManager
from reactor.messages import events
from reactor.messages import commands
from reactor.packet import Packet
from reactor.models.device import Device

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
            return
        
        # packet received 
        if(event.__class__.__name__ == "PacketReceived"):
            
            packet = Packet()
            packet.__dict__ = event.packet
            
            # check device
            device = devices.get_device(packet.src)
            if(device == None):
                # create device
                device = Device()
                device.id = int(packet.src)
                device.address = packet.src
                device.adapter = event.src
                
                # register device
                devices.register(device)
                
            # dispatch packet event
            self.dispatch_event(event)
         
            msg = events.DeviceUpdated()
            msg.src = "Core"
            msg.device = packet.src
            msg.data = packet.data
            
            # dispatch device updated event
            self.dispatch_event(msg)
            return
        
        else:
            logger.error("Unknown event type: " + event.uuid)
            return
        
        
        
    def dispatch_event(self, msg):
        router = component.get("Router")
        plugins = component.get("PluginManager")
        
        # dispatch event to all plugins except sender
        for plugin in plugins:
            msg.src = "Core"
            msg.dst = plugin.name
            if(msg.src != msg.dst and plugin.ready == True):
                router.send(msg, msg.dst)
    
    def process_command(self, cmd):
        logger.debug("Processing command: " + cmd.uuid)
        
        router = component.get("Router")
        plugins = component.get("PluginManager")
        devices = component.get("DeviceManager")
        
        # update device
        if(cmd.__class__.__name__ == "DeviceUpdate"):
            # get device from manager
            device = devices.get_device_by_id(cmd.device["id"])
            if(device == None):
                logger.error("Device not found: " + str(cmd.device["id"]))
                return
                
            # send packet to device
            packet = Packet()
            packet.src = 1
            packet.dst = device.id
            packet.cmd = 2
            packet.data = cmd.device["data"]
            
            msg = commands.PacketSend()
            msg.src = "Core"
            msg.dst = device.adapter
            msg.packet = packet.to_dict()
            
            logger.debug("Sending update request to device: " + msg.to_json())
            router.send(msg)
            return
        
        else:
            logger.error("Unknown command type: " + cmd.uuid)
        
    

    
    
        