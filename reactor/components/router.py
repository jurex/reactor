from reactor import log, component

import time, sys, thread

class Router(component.Component):
    def __init__(self):
        component.Component.__init__(self, "Router")

    def start(self):
        
        # register event
        #manager = component.get("EventManager")
        #manager.register_event_handler("MessageInQueueEvent", self.onMessageInQueueEventHandler)
        
        #log.info("virtual router started")
        #self.ProcessQueue()
        pass
        

    def onMessageInQueueEventHandler(self, adapter):
    
        log.debug("MessageInQueueEvent fired")
        #reactor.callInThread(ProcessMessageQueue)
        #reactor.callLater(4,ProcessMessageQueue)
        
        #reactor.callLater(0, self.ProcessMessageQueue)
        
        #d = maybeDeferred(self.ProcessMessageQueue)
        #self.ProcessMessageQueue()
        
        
    def ProcessQueue(self):
        
        # get message from messagequeue
        queue = component.get("MessageQueue")
        
        #print "router thread: " + str(thread.get_ident())
        
        log.info("starting processing queue")
        
        # infinite loop
        while 1:
      
            # get message from queue => blocking function
            message = queue.get()
            
            log.debug("message removed from queue. queuesize: " + str(queue.size()))
            
            # process message
            self.ProcessMessage(message)
            
            log.debug("finished processing message")
        
    
    def ProcessMessage(self, message):
    
        log.debug("processing message: " + message.toString())
    
        #time.sleep(1)
    
        # put message to history
        #history = component.get("MessageHistory")
        #history.put(message)
        
        # message routing start here
        
        sm = component.get("ServerManager")
        dm = component.get("DeviceManager")
        
        server = sm.getServer(message.dst)
        
        # dst => registred server
        if (server != None):    
            server.onMessageReceived(message)
            return
        
        # dst => registred device
        device = dm.getDevice(message.dst)
        if (device != None):
            device.send(message)
            return
        
        # unknown route
        log.error("no route found for id/address: " + str(message.dst))
        return
        
