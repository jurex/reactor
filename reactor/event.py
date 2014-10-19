# packet definition
import struct
import ctypes
import binascii
import json
import random
import sys
import datetime
import uuid

class Event(object):
    
    def __init__(self, name="unknown", data={}, src=""):
        self.uuid = str(uuid.uuid4())
        self.time = datetime.datetime.now().isoformat()
        self.name = name
        self.data = data
        self.src = src

    def __str__(self):
        return self.to_json()

    def __unicode__(self):
        return self.to_json()
        
    def to_bytes(self):
        return self.pack()
    
    def to_dict(self):
        fields = self.__dict__.copy()
        return fields 
        
    def to_string(self):
        return str(self.to_dict())
    
    def to_json(self):
        return json.dumps(self.to_dict())

    def from_json(self, obj):
        # check type
        if(type(obj) is not str):
            raise NameError('Wrong object type!')    
        
        # create dictonary from json strimg
        json_obj = json.loads(obj)

        # set attributes
        self.__dict__ = json_obj
    
    def __str__(self):
        return self.to_string()
