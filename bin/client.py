#!/usr/bin/env python

import sys
import time

sys.path.append("../")

from reactor.packet import Packet
from reactor import logger

from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM

SERVER_IP = "192.168.1.2"
SERVER_PORT = 4444


def main():
    
    # create udp socket
    sock = socket(AF_INET,SOCK_DGRAM)
    
    # send messages to server
    for i in range(0, 3):
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
        
        
    # run receive in separate thread
    #receiver_thread = Thread(target=receiver, args=(sock,))
    #receiver_thread.start()
    
    print("Listening for packets...")
    
    while True:
        # blocking read
        datagram, address = sock.recvfrom(1024) # buffer size is 1024 bytes
    
        # parse message
        packet = Packet()
        packet.unpack(datagram)

        print("Packet received: " + packet.to_string() + " ip: " + str(address))
    
    # wait for responses
    #time.sleep(20)
        
    
def receiver(sock):
    #sock.bind(("0.0.0.0", SERVER_PORT))
    print "Listening for packets..."
    
    while True:
        # blocking read
        datagram, address = sock.recvfrom(1024) # buffer size is 1024 bytes
    
        # parse message
        packet = Packet()
        packet.unpack(datagram)

        print("Packet received: " + packet.to_string() + " ip: " + str(address))

if __name__ == '__main__':
    main()