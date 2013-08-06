import os, flask, logging
from reactor import log, component
from gevent.wsgi import WSGIServer
from flask import Flask
from threading import Thread

class API(component.Component):
    def __init__(self):
        component.Component.__init__(self, "API")
        
        # init flask
        self.app = Flask(__name__)
        self.config = component.get("Config")
        self.port = self.config.config.getint("api", "port")
        # init config
        #self.app.config.from_pyfile('../config/app.conf')
        
        # init session key
        self.app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
        
        # init db
        #mongo = pymongo.MongoClient(app.config['DB_HOST'], app.config['DB_PORT'])
        #db = mongo.dmhelper
        
        # init app db
        #app.mongo = mongo
        #app.db = db
        
        # init logging
        self.app.logger.setLevel(logging.INFO)
        
        # init auth
        #auth = Auth(app)
        
        # init views
        from reactor.web.api import device
        
        log.debug("api initialized")

    def start(self):
        t = Thread(target=self.run,args=())
        t.start()
        
    def run(self):
        log.info("api started on port: " + str(self.port))
        self.api_server = WSGIServer(('', self.port), self.app)
        self.api_server.serve_forever()


"""
rom zope.interface import Interface, implements
from twisted.internet import reactor, defer
from twisted.web import server, resource

from whistler.device import Device
from whistler import log
from whistler import component

import sys, copy

try: 
    import simplejson as json
except ImportError: 
    import json

class Response(object):
    def __init__(self, object = None):
        
        self.version = 1
        self.object = object
        self.error = None
        self.result = None
        
    def __str__(self):
        self.result = self.object
        
        if(self.error != None):
            #return json.dumps({"version":self.version, "result": self.result, "error": self.error })
            return json.dumps({"error": self.error})
        else:
            
            return json.dumps(self.result)
        
class ApiDevice(resource.Resource):
    
    def render_GET(self, request):
        path = request.path
        
        log.debug("device api called: " + str(request.path))
        
        devices = []
        for device in component.get("DeviceManager").devices:
            devices.append(component.get("DeviceManager").devices[device].toDictonary())
            
        response = Response(devices)   
        return str(response)
    
class ApiMessage(resource.Resource):
    
    def render_GET(self, request):
        path = request.path
        
        log.debug("message api called: " + str(request.path))
        
        pm = component.get("PluginManager")
        history = pm.get("HistoryPlugin")
        
        messages = history.history
        #for msg in application.factory.messages:
        #    messages.append(msg.toDictonary())
        
        response = Response(messages)
        return str(response)
    
class ApiStatus(resource.Resource):
    
    def render_GET(self, request):
        path = request.path
        
        log.debug("status api called: " + str(request.path))
        
        pm = component.get("PluginManager")
        history = pm.get("History")
        queue = component.get("MessageQueue")
        
        result = {}
        result["HistorySize"] = len(history.history)
        result["QueueSize"] = queue.size()
        
        am = component.get("AdapterManager")
        result["NetworkAdapter"] = am.get("NetworkAdapter").toDictonary()
        
        response = Response(result)
        return str(response)
    
        
class ApiNotFoundError(resource.Resource):

    def render_GET(self, request):
        response = Response()
        response.error = 'API Not Found!'
        return str(response)
    
class ApiServer(component.Component):
    def __init__(self):
        self.port = 8888
        # component constructor
        component.Component.__init__(self, "ApiServer")
        
    def start(self):
        # start api server
        reactor.listenTCP(self.port, Site(ApiResource()))
        log.info("API started on port: " + str(self.port))
    
    def stop(self):
        log.info("API stopped")
        pass
    
    def shutdown(self):
        pass
    
class ApiResource(resource.Resource):
    
    def getResource(self, request):
        
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Content-Type', 'text/javascript')
        path = request.path
        
        if( str(path).startswith("/device")): 
            return ApiDevice()
        
        if( str(path).startswith("/message")): 
            return ApiMessage()
        
        if( str(path).startswith("/status")): 
            return ApiStatus() 
        
        return ApiNotFoundError()

    def render_GET(self, request):
        '''
        get response method for the root resource
        localhost:8000/
        '''
        log.debug("render get called: " + str(request) + " path: " + str(request.path))
        
        return 'Whistler JSON REST API'
        
        
"""
