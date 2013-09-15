from reactor import component
from reactor import utils
from reactor.messages import commands
from reactor.messages import events
import logging
import zmq
import json

logger = logging.getLogger("Router")

class Router(component.Component):
    def __init__(self):
        component.Component.__init__(self, "Router")

    def start(self):
        pass
        
    def run(self):
        
        config = component.get("Config")
        zmq_addr = config.get("core.zmq_addr")
        
        self.zmq_context = zmq.Context()
        self.zmq_socket = self.zmq_context.socket(zmq.ROUTER)
        self.zmq_socket.bind(zmq_addr)
        
        #print "router thread: " + str(thread.get_ident())
        
        logger.info("Starting processing messages")
        
        # infinite loop
        while 1:
      
            # receive message
            src = self.zmq_socket.recv()
            msg_json = self.zmq_socket.recv()
            msg = utils.decode_message(msg_json)
    
            logger.debug("Message received (" + src + "): " + str(msg.to_json()))
        
            # process message
            self.process(msg, src)

    def process(self, msg, src):
    
        # logger.debug("Routing message: " + msg.uuid)
        
        # get components
        core = component.get("Core")
        devices = component.get("DeviceManager")

        # TODO: packet routing
        
        if(msg.dst == "Core"):
            # dispatch message to core
            core.process(msg, src)
        else:
            self.send(msg, msg.dst)
        
    def send(self, msg, dst):
        logger.debug("Sending message: " + msg.uuid + " to: " + dst)
        self.zmq_socket.send_unicode(dst, zmq.SNDMORE)
        return self.zmq_socket.send_unicode(msg.to_json())
        
