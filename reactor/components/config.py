from reactor.component import Component

import ConfigParser

class Config(Component):
    def __init__(self, path):
        Component.__init__(self, "Config")
        
        self.config = ConfigParser.ConfigParser()
        self.config.read(path)
        
    def get(self, section, option):
        return self.config.get(section, option);