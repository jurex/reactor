#!/usr/bin/python
import sys
import time

sys.path.append("../")

from reactor.packet import Packet
from reactor import logger

from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM

if __name__ == '__main__':
    
    #create udp socket
    sock = socket(AF_INET,SOCK_DGRAM)
    sock.bind(("0.0.0.0", 4444))

    print("Listening for packets...")
    
    counter = 0
    while True:
        # blocking read
        datagram, address = sock.recvfrom(4024) # buffer size is 1024 bytes

        counter = counter + 1

        #print("counter: " + str(counter))
        print("Packet received: " + str(counter))
        #print("jurajko je uplny paaaan najvacsi na svete               alskdjf asdlk jfaskdj k")


        # time.sleep(0.001)

    
        # parse message
        #packet = Packet()
        #packet.unpack(datagram)

        #print("Packet received: " + packet.to_string() + " ip: " + str(address))
