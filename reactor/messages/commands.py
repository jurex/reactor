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


class PacketSend(Command):
    pass

class DeviceDiscover(Command):
    pass

class DeviceCreate(Command):
    pass

class DeviceUpdate(Command):
    device = {}

class DeviceDelete(Command):
    pass

class FirmwareUpdate(Command):
    pass
