from threading import Thread
from multiprocessing import Process

class Adapter(Thread):
    def __init__(self):
        Thread.__init__(self)