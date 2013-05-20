'''
Created on 19.5.2013

@author: Jurex
'''
# packet definition
from zope.interface import Interface, implements
from twisted.internet import protocol, reactor, defer

from reactor import log, component
from reactor.event import MessageInQueueEvent
from reactor.message import Message
from reactor.models.adapter import Adapter, IAdapter

from multiprocessing import Process
from threading import Thread

class NetworkAdapter(Thread):
    
    #implements(IAdapter)
    
    def __init__(self, queue):
        
        Thread.__init__(self)
        
        self.protocol = DatagramProtocol(self)
        self.addresses = {} # dstAddress => ipAddress
        self.port = 4444
        self.name = "NetworkAdapter"
        self.queue = queue
        
        self.messagesIn = 0
        self.messagesOut = 0
        
        # base class initialization
        
        
        log.debug('network adapter initlialized')
        
    def run(self):
        # start lan adapter
        reactor.listenUDP(self.port, self.protocol)
        log.debug('network adapter started on port: ' + str(self.port))
        reactor.run(installSignalHandlers=False)
        
    def stop(self):
        reactor.stop()
        pass
        
    def write(self, message):
        address = self.addresses.get(message.dst)
        if (address == None) : 
            log.error("unknown dst IP address for device " + str(message.dst))
            raise Exception("unknown dst IP address for device " + str(message.dst))
        
        self.protocol.transport.write(message.pack(), address)
        log.debug("message sent: " + message.toString() + " ip: " + str(address))
        self.messagesOut += 1
        
    def addAddress(self, src, address):
        addr = self.addresses.get(src)
        if (addr == None or addr != address):
            self.addresses[src] = address
            log.debug('ip address registred: ' + str(src) + " = " + str(address))
            
    def toDictonary(self):
        d = self.__dict__.copy()
        if( d.has_key("protocol")):
            d.pop("protocol") 
        return d
        
class DatagramProtocol(protocol.DatagramProtocol):
    
    def __init__(self, adapter):
        self.adapter = adapter
        log.debug('datagram protocol initialized')
    
    def datagramReceived(self, datagram, address):
        # rise counter
        self.adapter.messagesIn += 1
        
        # parse message
        message = Message()
        message.unpack(datagram)
        message.adapter = self.adapter
        
        log.debug("mesage received: " + message.toString() + " ip: " + str(address))
        self.adapter.addAddress(message.src, address)
        
        self.adapter.queue.put(message)
        
        # fire event
        #em = component.get("EventManager")
        #em.fireEvent(MessageInQueueEvent(self.adapter))
        
        log.debug("datagram processing finished")
         
        # fire system event
        #reactor.addSystemEventTrigger('during', 'MessageReceivedEvent', processor.MessageReceivedEventHandler)
        #reactor.fireSystemEvent('MessageInQueueEvent') 
    
    
        
    

        