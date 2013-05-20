#!/usr/bin/env python

import sys
sys.path.append("../")

from reactor.message import Message
import time

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, task

class WhistlerDatagramProtocol(DatagramProtocol):
 
    def startProtocol(self):
        self.transport.connect('192.168.1.2', 4444)

    def datagramReceived(self, datagram, host):
        #print 'Datagram received: ', repr(datagram)
        
        msg = Message()
        msg.unpack(datagram)
        print "Message received: " +  msg.toString()

def main():
    protocol = WhistlerDatagramProtocol()
    t = reactor.listenUDP(0, protocol)
    
    tsk = task.LoopingCall(sendMessage, protocol)
    tsk.start(1)
    
    #reactor.callInThread(sendMessagesForever(protocol))
    reactor.run()
    
def sendMessage(protocol):
    msg = Message()
    msg.src = 25
    msg.dst = 1
    msg.cmd = 1
    msg.addVariable("hellou", "world")
    """
    message.addVariable("int", 221)
    message.addVariable("bool", False)
    message.addVariable("float", 1.1)
    message.addVariable("empty", None)
    """
    protocol.transport.write(msg.toBytes())
    print "Message sent: " + msg.toString()

if __name__ == '__main__':
    main()