from reactor import log, component

# custom plugins: TODO: auto import by name

from plugins.history.history import *
from plugins.echo.echo import *

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
        log.debug("plugin registred: %s", plugin.name)
        
    def getPluginByName(self, name):
        for plugin in self.plugins:
            if(plugin.name == name):
                return plugin
            
        return None
            
    def getPlugin(self, name):
        return self.getPluginByName(name)
    
    def get(self, name):
        return self.getPluginByName(name)
        