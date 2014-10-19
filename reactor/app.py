import logging
import yaml
import os

from reactor import components
from reactor.components.core import Core
from reactor.components.config import Config
from reactor.components.database import Database

from reactor.managers.plugin import PluginManager
from reactor.managers.device import DeviceManager
from reactor.managers.adapter import AdapterManager

from reactor import logger

# init config
config = Config('../conf/reactor.yml')

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
        self.version = '0.2.0'

        logger.info("Version: " + self.version)
        
        # init core parts 
        self.core = Core();
        self.database = Database()
        
        # init other managers
        self.adapters = AdapterManager()
        self.devices = DeviceManager()
        self.plugins = PluginManager()
        
        
        # load plugins
        # TODO: load plugins from config
        self.plugins.load("History")
        self.plugins.load("Echo")
        
        # init complete
        logger.debug("App initialized. PID: " + str(os.getpid()))
        
        try:
            # start components
            components.start()
            logger.info("All compnents started") 
            
            # start router / blocking call
            self.core.run()
            
        finally:
            self.shutdown()
    
        
    def shutdown(self, *args, **kwargs):
        components.shutdown()
        
        


    

    

