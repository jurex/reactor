#!/usr/bin/env python

import sys
sys.path.append("../")

from reactor.packet import Packet
import time

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, task

class WhistlerDatagramProtocol(DatagramProtocol):
 
    def startProtocol(self):
        self.transport.connect('192.168.1.2', 4444)

    def datagramReceived(self, datagram, host):
        #print 'Datagram received: ', repr(datagram)
        
        packet = Packet()
        packet.unpack(datagram)
        print "Packet received: " +  packet.to_string()

def main():
    protocol = WhistlerDatagramProtocol()
    t = reactor.listenUDP(0, protocol)
    
    tsk = task.LoopingCall(send_packet, protocol)
    tsk.start(1)
    
    #reactor.callInThread(sendMessagesForever(protocol))
    reactor.run()
    
def send_packet(protocol):
    packet = Packet()
    packet.src = 25
    packet.dst = 1
    packet.cmd = 1
    packet.add_variable("hellou", "world")
    """
    message.add_variable("int", 221)
    message.add_variable("bool", False)
    message.add_variable("float", 1.1)
    message.add_variable("empty", None)
    """
    protocol.transport.write(packet.to_bytes())
    print "Packet sent: " + packet.to_string()

if __name__ == '__main__':
    main()