#!/usr/bin/env python
import sys, os
sys.path.append("../")

#from whistler.factory import DefaultFactory
from whistler import main


if __name__ == '__main__':
    #start server
    main.start_server()

