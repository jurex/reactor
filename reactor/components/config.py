from reactor.component import Component

import ConfigParser
import yaml

class Config(Component, dict):
    def __init__(self, path):
        Component.__init__(self, "Config")
        
        f = open(path)
        self.data = yaml.load(f)
        f.close()
        
    def __getitem__(self, item):
        try:
            return self.data.__getitem__(item)
        except KeyError:
            return None

        
    def get(self, section, default = None):
        
        try:
            parts = section.split(".")
            value = None;
            
            if(len(parts) <= 0):
                value = self.data[section]
            else:
                value = self.data
        
            for index, part in enumerate(parts):
                value = value[part]
        
        except KeyError, ex:
            if(default != None):
                return default
            else:
                raise KeyError('Config section not found: ' + section)

        return value;