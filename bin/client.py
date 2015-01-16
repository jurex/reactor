#!/usr/bin/env python

import sys
import time

sys.path.append("../")

from reactor.packet import Packet
from reactor import logger

from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM

SERVER_IP = "192.168.1.129"
SERVER_PORT = 4444


def main():
    
    # create udp socket
    sock = socket(AF_INET,SOCK_DGRAM)
    #sock.bind(("0.0.0.0", SERVER_PORT))
    
    # send messages to server
    for i in range(0, 10):
        packet = Packet()
        packet.src = 25
        packet.dst = 1
        packet.cmd = "device.update"
        packet.seq = i
        packet.data = {"sys.banner":"hello world", "io.counter": i}

        sock.sendto(packet.to_json(), (SERVER_IP, SERVER_PORT))
        print "Packet sent: " + packet.to_json()
        
        #time.sleep(0.001)
        
    print("Listening for packets...")
    
    counter = 0

    while True:
        # blocking read
        datagram, address = sock.recvfrom(1024) # buffer size is 1024 bytes

        counter = counter + 1

        print("Packet received: " + str(datagram) + " ip: " + str(address) + " c: " + str(counter))
    
        # wait for responses
        #time.sleep(20)

if __name__ == '__main__':
    main()