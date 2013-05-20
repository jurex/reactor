from reactor import log, component
from reactor.adapters.network import NetworkAdapter

class AdapterManager(component.Component):
    def __init__(self):
        self.adapters = []
        
        # TODO: add adapters based on config or options
        
        # crate network adapter
        mq = component.get("MessageQueue")
        networkAdapter = NetworkAdapter(mq)
        self.register(networkAdapter)
        
        # create RFM12B adapter
        #adapter = RFM12BAdapter()
        #self.register(adapter)
        
        # component constructor
        component.Component.__init__(self, "AdapterManager")
        
    def register(self, adapter):
        self.adapters.append(adapter)
        log.debug(adapter.name + " registred")
        
    def unregister(self, adapter):
        pass
        
    def start(self):
        for adapter in self.adapters:
            adapter.start()
            
    def getAdapterByName(self, name):
        for adapter in self.adapters:
            if(adapter.name == name):
                return adapter
            
        return None
            
    
    def get(self, name):
        return self.getAdapterByName(name)

        