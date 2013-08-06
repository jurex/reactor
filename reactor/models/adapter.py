# packet definition

class Adapter(object):
    
    def __init__(self):
        self.messagesIn = 0
        self.messagesOut = 0
        
    def write(self, message):
        """ send message to device """
        raise NotImplementedError( "Method not implemented" )
    
    def start(self):
        """ start adapter """
        raise NotImplementedError( "Method not implemented" )
        
    def stop(self):
        """ stop adapter """
        raise NotImplementedError( "Method not implemented" )
