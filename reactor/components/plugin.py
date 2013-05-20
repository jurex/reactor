from zope.interface import Interface, implements
from reactor import log

class IPlugin(Interface):
        
    def start(self):
        """ start plugin """
        
    def stop(self):
        """ stop plugin """

class Plugin(object):
    
    implements(IPlugin)
    
    def __init__(self, name, depend=None):
        self._plugin_name = name
        self._plugin_depend = depend
        self._plugin_state = "Stopped"

    def start(self):
        pass
    
    def stop(self):
        pass

    def _plugin_start(self):
        pass

    def _plugin_stop(self):
        pass
        
    def _plugin_shutdown(self):
        pass
        

    
    