from reactor import component

import logging
logger = logging.getLogger("PluginManager")

# custom plugins: TODO: auto import by name
from plugins.echo.echo import EchoPlugin
from plugins.history.history import HistoryPlugin
from plugins.websocket.websocket import WebsocketPlugin

class PluginManager(component.Component):
    def __init__(self):
        self.plugins = []
        
        # TODO: additional servers from config
        component.Component.__init__(self, "PluginManager")
        
    def start(self):
        for plugin in self.plugins:
            plugin.daemon = True;
            plugin.start()
        
    # load plugin by name
    def load(self, name):
        
        plugin = globals()[name+"Plugin"]()
        self.register(plugin)   
        
        
    def register(self, plugin):
        self.plugins.append(plugin)
        logger.debug("Plugin registred: %s", plugin.name)
        
    def get_plugin_by_name(self, name):
        for plugin in self.plugins:
            if(plugin.name == name):
                return plugin
            
        return None
            
    def get_plugin(self, name):
        return self.get_plugin_by_name(name)
    
    def get(self, name):
        return self.get_plugin_by_name(name)
    
    def get_plugins(self):
        return self.plugins
    
    def __iter__(self):
        return self.plugins.__iter__()
        