import logging
import yaml

from reactor import components
from reactor.components.router import Router
from reactor.components.config import Config

from reactor.managers.device import DeviceManager
from reactor.managers.server import ServerManager
from reactor.managers.plugin import PluginManager
from reactor.managers.adapter import AdapterManager

from reactor import logger

# init config
config = Config('./config/reactor.yaml')

# setup logger
#loglevel = config.get("app", "loglevel")
logfile = None

if('file' in config.get("logging")):
    logfile = config.get("logging.file")
    
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=logfile,
    filemode="w"
)
   
class App(object):
        
    def run(self):
        self.version = '0.1.0'

        logger.info("Version: " + self.version)
        
        # init core parts 
        self.router = Router()
        
        # init other managers
        self.serverManager = ServerManager()
        self.deviceManager = DeviceManager()
        self.adapterManager = AdapterManager()
        self.pluginManager = PluginManager()
        
        
        # load plugins
        # TODO: load plugins from config
        self.pluginManager.load("History")
        self.pluginManager.load("Echo")
        
        #print "Application thread: " + str(thread.get_ident())
        
        # init complete
        logger.debug("App initialized")
        
        try:
            # start components
            components.start()
            logger.info("All compnents started") 
            
            # run blocking queue
            self.router.ProcessQueue()
            
        finally:
            self.shutdown()
    
        
    def shutdown(self, *args, **kwargs):
        components.shutdown()
        
        


    

    
