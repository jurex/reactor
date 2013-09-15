from reactor import component
from reactor import utils
from reactor.models.plugin import Plugin
from reactor.messages import events
from reactor.messages import commands
from reactor.packet import Packet

import os

import logging
logger = logging.getLogger("EchoPlugin")

class EchoPlugin(Plugin):
    
    def __init__(self):
        Plugin.__init__(self, "EchoPlugin")
    
    def run(self):
        
        # connect
        self.connect()
        logger.info("Plugin started. PID: " + str(os.getpid()))
        
        while True:
            msg = self.receive()
            logger.debug("Message Received: " + msg.to_json())
            
            if(msg.__class__.__name__ == "PacketReceived"):
                packet = Packet()
                packet.__dict__ = msg.packet
                packet.dst = packet.src
                packet.src = 1
                cmd = commands.PacketSend();
                cmd.src = self.name
                cmd.dst = "EthernetAdapter"
                cmd.packet = packet.to_dict()
                
                self.send(cmd)            
    
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