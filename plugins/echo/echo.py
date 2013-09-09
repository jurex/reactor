from reactor import component
from reactor.models.plugin import Plugin
from reactor.messages import events
from reactor.messages import commands

import logging
logger = logging.getLogger("EchoPlugin")

class EchoPlugin(Plugin):
    
    def __init__(self):
        Plugin.__init__(self, "EchoPlugin")
    
    def run(self):
        # send ready
        msg = events.PluginReady()
        msg.src = self._name
        msg.dst = "Core"
            
        # send request to core
        self.zmq_socket.send(msg.to_json())
        
        logger.info("Plugin started")
        
        while True:
            msg = self.zmq_socket.recv();
            logger.debug("Message Received: " + msg.uuid)
    
    
    def receiver(self, source, message):
        
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