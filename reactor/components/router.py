from reactor import component
from reactor import utils
from reactor.event import Event
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
        
        self.zmq_init()
        
        logger.info("Starting processing messages")
        
        # infinite loop
        while 1:
            self.zmq_recv()
            
    def process(self, event, src):        
        # get components
        core = component.get("Core")
        devices = component.get("DeviceManager")

        # TODO: packet routing
        
        core.process(event, src)
        self.dispatch(event)

    def dispatch(self, event):
        plugins = component.get("PluginManager")
        adapters = component.get("AdapterManager")

        # dispatch event to all plugins except sender
        for plugin in plugins:
            if(plugin.name != event.src and plugin.ready == True):
                self.zmq_send(event, plugin.name)

        # dispatch event to all adapters except sender
        for adapter in adapters:
            if(adapter.name != event.src and adapter.ready == True):
                self.zmq_send(event, adapter.name)

    def zmq_init(self):
        config = component.get("Config")
        zmq_addr = config.get("core.zmq_addr")
        
        self.zmq_context = zmq.Context()
        self.zmq_socket = self.zmq_context.socket(zmq.ROUTER)
        self.zmq_socket.bind(zmq_addr)

    def zmq_send(self, event, dst):
        #logger.debug("Sending message: " + msg.uuid + " to: " + dst)
        self.zmq_socket.send_unicode(dst, zmq.SNDMORE)
        return self.zmq_socket.send_unicode(event.to_json())

    def zmq_recv(self):
        # zmq recv
       # receive message
        src = self.zmq_socket.recv()
        obj = self.zmq_socket.recv()
        event = Event()
        event.from_json(obj)

        logger.debug("Event received from: " + src + ", " + event.to_json())
    
        # process message
        self.process(event, src)