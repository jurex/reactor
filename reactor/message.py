# packet definition
import struct
import ctypes
import binascii
import json
import random
import sys
import datetime
import uuid

class Message(object):
    
    def __init__(self):
        self.src = ''
        self.dst = 'Core'
        self.uuid = str(uuid.uuid4())
        self.created = datetime.datetime.now().isoformat()
        
    def to_bytes(self):
        return self.pack()
    
    def to_dict(self):
        fields = self.__dict__.copy()
        fields['class'] = self.__class__.__name__
        # dict.pop("packet_header_struct")
        return fields 
        
    def to_string(self):
        return str(self.to_dict())
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def __str__(self):
        return self.to_string()
