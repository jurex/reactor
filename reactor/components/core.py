from reactor import component
from reactor.managers.device import DeviceManager
from reactor.event import Event
from reactor.packet import Packet
from reactor.eventbus import ZMQEventBus
from reactor.models.device import Device

import logging
logger = logging.getLogger("Core")

class Core(component.Component):
    def __init__(self):
        component.Component.__init__(self, "Core")
        
        self.id = 1
        self.address = 1
        self.eventbus = ZMQEventBus("@core")

    def run(self):

        while 1:
            # listen for events
            event = self.eventbus.receive()
            logger.debug("Event received: " + event.to_json())

            # process events
            self.process(event)

            # dispatch events
            self.eventbus.dispatch(event)
    
    def process(self, event):
        #logger.debug("Processing event: " + event.uuid)
        
        adapters = component.get("AdapterManager")
        plugins = component.get("PluginManager")
        devices = component.get("DeviceManager")
        
        # set adapter as ready
        if(event.name == "adapter.ready"):
            adapter = adapters.get(event.src)
            adapter.ready = True;
            return
        
        # set plugin as ready
        elif(event.name == "plugin.ready"):
            plugin = plugins.get(event.src)
            plugin.ready = True;
            return
        
        # packet received 
        elif(event.name == "device.update"):

            logger.info("updating device")

            # get device from manager
            #device = devices.get_device_by_id(event.data["id"])
            #if(device == None):
            #    logger.error("Device not found: " + str(cmd.device["id"]))
            #    return
            
            # dispatch device updated event
            # self.dispatch_event(event)
            return
        
        else:
            pass
            #logger.error("Unknown event: " + event.name)       
        