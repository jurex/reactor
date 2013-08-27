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
        zmq_request_addr = config.get("core.zmq_addr")
        
        context = zmq.Context()
        zmq_socket = context.socket(zmq.ROUTER)
        zmq_socket.bind(zmq_request_addr)
        
        #print "router thread: " + str(thread.get_ident())
        
        logger.info("Starting processing messages")
        
        # infinite loop
        while 1:
      
            # receive message
            _id = zmq_socket.recv()
            msg_json = zmq_socket.recv()
            msg = utils.decode_message(msg_json)
    
            
            logger.debug("Message received (" + _id + "): " + str(msg.to_json()))
            
            # send ack
            #zmq_socket.send(_id, zmq.SNDMORE)
            #zmq_socket.send("ok")
            
            # process message
            self.process(msg)
            
            logger.debug("Message processing finished")
        
    
    def process(self, msg):
    
        logger.debug("Routing message: " + msg.to_string())
    
        #time.sleep(1)
    
        # put message to history
        #history = component.get("MessageHistory")
        #history.put(message)
        
        # message routing start here
        
        core = component.get("Core")
        dm = core.get_device_manager()
        
        server = sm.getServer(message.dst)
        
        # dst => registred server
        if (server != None):    
            server.onMessageReceived(message)
            return
        
        # dst => registred device
        device = dm.getDevice(message.dst)
        if (device != None):
            device.send(message)
            return
        
        # unknown route
        logger.error("no route found for id/address: " + str(message.dst))
        return
        
