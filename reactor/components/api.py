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
