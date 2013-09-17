#!/usr/bin/python
import sys
sys.path.append("../")

from reactor.app import App

if __name__ == '__main__':
    # init
    app = App()
    
    # run
    app.run() 
