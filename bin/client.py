#!/usr/bin/env python

import sys
import time

sys.path.append("../")

from reactor.packet import Packet
from reactor import logger

from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM

SERVER_IP = "localhost"
SERVER_PORT = 4444


def main():
    
    # create udp socket
    sock = socket(AF_INET,SOCK_DGRAM)
    sock.bind(("0.0.0.0", SERVER_PORT))
    
    # send messages to server
    for i in range(0, 100)
        packet = Packet()
        packet.src = 25
        packet.dst = 1
        packet.cmd = 1
        packet.seq = i
        packet.add_data("hellou", "world")
        packet.add_data("counter", i)
        """
        packet.add_variable("int", 221)
        packet.add_variable("bool", False)
        packet.add_variable("float", 1.1)
        packet.add_variable("empty", None)
        """
        sock.sendto(packet.to_bytes(), (SERVER_IP, SERVER_PORT))
        print "Packet sent: " + packet.to_string()
        
        #time.sleep(0.001)
        
    print("Listening for packets...")
    
    counter = 0

    while True:
        # blocking read
        datagram, address = sock.recvfrom(1024) # buffer size is 1024 bytes
    
        # parse message
        #packet = Packet()
        #packet.unpack(datagram)

        counter = counter + 1

        print("Packet received: " + str(datagram) + " ip: " + str(address) + " c: " + str(counter))
    
        # wait for responses
        #time.sleep(20)

if __name__ == '__main__':
    main()