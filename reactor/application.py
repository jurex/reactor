from reactor import log

from reactor.message import MessageQueue, MessageHistory

from reactor import components
from reactor.components.config import Config
from reactor.components.router import Router
from reactor.components.api import API

from reactor.managers.event import EventManager
from reactor.managers.device import DeviceManager
from reactor.managers.server import ServerManager
from reactor.managers.plugin import PluginManager
from reactor.managers.adapter import AdapterManager

#from whistler.api import ApiServer

    
class Application(object):
        
    def run(self):
        self.version = '0.0.2.0'
        
        # init core part
        self.config = Config('./config/app.conf')
        
        # setup logger
        loglevel = self.config.get("application", "loglevel")
        logfile = None
        
        if(self.config.config.has_option("application", "logfile")):
            logfile = self.config.get("application", "logfile")

        log.setupLogger(loglevel, logfile) 
        
        # app
        log.info("running app version: " + self.version)
        
        
        # init core parts 
        
        self.messageQueue = MessageQueue()
        self.messageHistory = MessageHistory()
        
        self.router = Router()
        self.api = API()
        
        # init other managers
        self.eventManager = EventManager()
        self.serverManager = ServerManager()
        self.deviceManager = DeviceManager()
        self.adapterManager = AdapterManager()
        self.pluginManager = PluginManager()
        
        
        # load plugins
        # TODO: load plugins from config
        self.pluginManager.load("History")
        self.pluginManager.load("Echo")

        # init JSON API
        #self.api = ApiServer();
        
        #print "Application thread: " + str(thread.get_ident())
        
        # init complete
        log.debug("application initialized")
        
        
            

        try:
            # start components
            components.start()
            log.info("application started") 
            
            # run blocking queue
            #self.router.ProcessQueue()
            
        finally:
            self.shutdown()
    
        
    def shutdown(self, *args, **kwargs):
        components.shutdown()
        
        


    

    

