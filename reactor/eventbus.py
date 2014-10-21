from reactor import component
from reactor import utils
from reactor.event import Event
import zmq.green as zmq
import json
import logging

import gevent
import gevent.monkey

import redis
import redis.connection

gevent.monkey.patch_socket()

logger = logging.getLogger("EventBus")

class EventBus(object):

    def __init__(self, name="unknown"):
        self.name = name
        self.config = component.get("Config")

    def receive(self):
        pass

    def dispatch(self, event):
        pass

class ZMQCoreEventBus(EventBus):

    def __init__(self, name="unknown"):
        # parent init
        EventBus.__init__(self, name)

        # zmq init
        zmq_addr = self.config.get("core.zmq_addr")
        
        self.zmq_context = zmq.Context()
        self.zmq_socket = self.zmq_context.socket(zmq.ROUTER)
        self.zmq_socket.bind(zmq_addr)

    def receive(self):
        src = self.zmq_socket.recv()
        obj = self.zmq_socket.recv()
        event = Event()
        event.from_json(obj)
        return event;

    def dispatch(self, event):
        plugins = component.get("PluginManager")
        adapters = component.get("AdapterManager")

        # dispatch event to all plugins except sender
        for plugin in plugins:
            if(plugin.name != event.src and plugin.ready == True):
                self.zmq_socket.send_unicode(plugin.name, zmq.SNDMORE)
                self.zmq_socket.send_unicode(event.to_json())

        # dispatch event to all adapters except sender
        for adapter in adapters:
            if(adapter.name != event.src and adapter.ready == True):
                self.zmq_socket.send_unicode(adapter.name, zmq.SNDMORE)
                self.zmq_socket.send_unicode(event.to_json())

class ZMQEventBus(EventBus):

    def __init__(self, name="unknown"):
        # parent init
        EventBus.__init__(self, name)
        
        # create zmq socket
        config = component.get("Config")
        zmq_core_addr = config.get('core.zmq_addr')
        self.zmq_context = zmq.Context()
        self.zmq_socket = self.zmq_context.socket(zmq.DEALER)
        self.zmq_socket.setsockopt(zmq.IDENTITY, name)
        self.zmq_socket.connect(zmq_core_addr)

    def receive(self):
        obj = self.zmq_socket.recv()
        event = Event()
        event.from_json(obj)
        return event;

    def dispatch(self, event):
        # dispatch to core
        event.src = self.name
        self.zmq_socket.send_unicode(event.to_json())


class RedisEventBus(EventBus):

    def __init__(self, name="unknown"):
        # parent init
        EventBus.__init__(self, name)

        # zmq init
        self.redis = redis.StrictRedis()
        self.redis.hset("eventbus_subs", self.name, "*")

    def receive(self):
        # redis blocking pop
        obj = self.redis.brpop(self.name)

        event = Event()
        event.from_json(obj[1])
        return event;

    def dispatch(self, event):
        event.src = self.name

        if event.src != "@core":
            self.redis.lpush("@core", event.to_json())


class RedisCoreEventBus(EventBus):

    def __init__(self, name="unknown"):
        # parent init
        EventBus.__init__(self, name)

        # zmq init
        self.redis = redis.StrictRedis()

    def receive(self):
        # redis blocking pop
        obj = self.redis.brpop("@core")

        event = Event()
        event.from_json(obj[1])
        return event;

    def dispatch(self, event):
        plugins = component.get("PluginManager")
        adapters = component.get("AdapterManager")

        #logger.debug("dispatching event: " + event.to_json())

        # dispatch event to all plugins except sender
        for plugin in plugins:
            if(plugin.name != event.src and plugin.ready == True):
                #logger.debug("dispatching to plugin: " + plugin.name)
                self.redis.lpush(plugin.name, event.to_json())

        # dispatch event to all adapters except sender
        for adapter in adapters:
            if(adapter.name != event.src and adapter.ready == True):
                #logger.debug("dispatching to adapter: " + adapter.name)
                self.redis.lpush(adapter.name, event.to_json())