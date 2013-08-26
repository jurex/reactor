# packet definition
import struct
import ctypes
import binascii
import json
import random
import sys
import datetime

from reactor.message import Message

class Command(Message):
    """
    The base class for all commands.
    """
    def to_dict(self):
        fields = self.__dict__.copy()
        fields['class'] = self.__class__.__name__
        fields['type'] = 'command'
        return fields 


class PacketSend(Message):
    pass

class DeviceDiscover(Message):
    pass

class DeviceCreate(Message):
    pass

class DeviceUpdate(Message):
    pass

class DeviceDelete(Message):
    pass

class FirmwareUpdate(Message):
    pass
