from reactor import log

class Plugin(object):
    
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
        

    
    