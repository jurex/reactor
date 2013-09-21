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
                # create packet
                packet = Packet()
                packet.__dict__ = msg.packet
                packet.dst = packet.src
                packet.src = 1
                
                # create command
                cmd = commands.PacketSend()
                cmd.src = self.name
                cmd.dst = "EthernetAdapter"
                cmd.packet = packet.to_dict()
                
                # send command
                self.send(cmd)
                
                # create command
                cmd = commands.DeviceUpdate()
                cmd.src = self.name
                cmd.dst = "Core"
                cmd.device = {'id': 25, 'data': {'io.output.1': 25}}
                
                # send command
                self.send(cmd)