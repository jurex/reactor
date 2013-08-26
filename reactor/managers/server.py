from reactor import component
from reactor.models.server import Server

import logging
logger = logging.getLogger("ServerManager")

class ServerManager(component.Component):
    def __init__(self):
        self.servers = []
        
        # default server
        server = Server("Default")
        self.register(server)
        
        # TODO: additional servers from config
        component.Component.__init__(self, "ServerManager")
        
    def start(self):
        for server in self.servers:
            server.start()
        
        
    def register(self, server):
        self.servers.append(server)
        logger.debug("Server registred: " + server.name)
        
    def getServerByAddress(self,  address):
        for server in self.servers:
            if (server.address == address):
                return server;
            
    def getServerById(self,  _id):
        for server in self.servers:
            if (server.id == _id):
                return server;
            
    def getServer(self, id_or_address):
        if (isinstance(id_or_address, (int))):
            return self.getServerById(id_or_address)
        else:
            return self.getServerByAddress(id_or_address)