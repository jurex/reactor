from reactor import component
from reactor.adapters.ethernet import EthernetAdapter

import logging
logger = logging.getLogger("AdapterManager")

class AdapterManager(component.Component):
    def __init__(self):
        self.adapters = []
        
        # TODO: add adapters based on config or options
        
        # crate network adapter
        network_adapter = EthernetAdapter()
        self.register(network_adapter)
        
        # create RFM12B adapter
        #adapter = RFM12BAdapter()
        #self.register(adapter)
        
        # component constructor
        component.Component.__init__(self, "AdapterManager")
        
    def register(self, adapter):
        self.adapters.append(adapter)
        logger.debug("Adapter registred: " + adapter.name)

    def unregister(self, adapter):
        pass
        
    def start(self):
        for adapter in self.adapters:
            adapter.daemon = True;
            adapter.start()
            
    def get_adapter_by_name(self, name):
        for adapter in self.adapters:
            if(adapter.name == name):
                return adapter
            
        return None
            
    def get(self, name):
        return self.get_adapter_by_name(name)

    def __iter__(self):
        return self.adapters.__iter__()

        