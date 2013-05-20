# packet definition

from zope.interface import Interface, implements

class IAdapter(Interface):
    
    def write(self, message):
        """ send message to device """
        
    def start(self):
        """ start adapter """
        
    def stop(self):
        """ stop adapter """
        
class Adapter(object):
    implements(IAdapter)
    
    def __init__(self):
        self.messagesIn = 0
        self.messagesOut = 0
