import json

from reactor.messages.events import *
from reactor.messages.commands import *

def decode_message(obj):
    # check type
    if(type(obj) is not str):
        raise NameError('Wrong object type!')    
    
    # create dictonary from json strimg
    json_obj = json.loads(obj)    
    
    # check attributes
    if('class' not in json_obj or 'type' not in json_obj or 'src' not in json_obj):
        
        raise NameError('Cannot decode message: ' + str(json_obj))
    
    class_ = globals()[json_obj['class']]
    
    # create message
    msg = class_()
    msg.__dict__ = json_obj
    
    return msg