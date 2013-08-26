from reactor import component

import logging
logger = logging.getLogger("PluginManager")

# custom plugins: TODO: auto import by name
from plugins.echo.echo import EchoPlugin
from plugins.history.history import HistoryPlugin

class PluginManager(component.Component):
    def __init__(self):
        self.plugins = []
        
        # TODO: additional servers from config
        component.Component.__init__(self, "PluginManager")
        
    def start(self):
        for plugin in self.plugins:
            plugin.start()
        
    # load plugin by name
    def load(self, name):
        
        plugin = globals()[name+"Plugin"]()
        self.register(plugin)   
        
        
    def register(self, plugin):
        self.plugins.append(plugin)
        logger.debug("Plugin registred: %s", plugin.name)
        
    def getPluginByName(self, name):
        for plugin in self.plugins:
            if(plugin.name == name):
                return plugin
            
        return None
            
    def getPlugin(self, name):
        return self.getPluginByName(name)
    
    def get(self, name):
        return self.getPluginByName(name)
        