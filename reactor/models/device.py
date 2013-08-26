
class Device(object):
    def __init__(self):
        self.id = 0
        self.address = None
        self.status = "unknown"
        self.adapter = None
        self.server = None
    
    def send(self, message):
        self.adapter.write(message)
        
    def getStatus(self):
        return "Status OK"
    
    def to_dict(self):
        d = self.__dict__.copy()
        if( d.has_key("adapter")):
            d.pop("adapter") 
        return d