# packet definition
import struct
import ctypes
import binascii
import json
import random

from pyasn1.type import univ
from pyasn1.codec.ber import encoder, decoder
from pyasn1.type import univ,namedtype,namedval,tag,constraint

from reactor import log, component
#from multiprocessing import Queue
from Queue import Queue
import sys


class Packet(object):
    
    def pack(self):
        """pack attributes to raw bytes"""
        raise NotImplementedError( "Method not implemented" )
        
    def unpack(self, buffer):
        """unpack raw bytes to attributest"""
        raise NotImplementedError( "Method not implemented" )

class Message(Packet):
    
    def __init__(self, bytes = None):
        # packet header      # 12 bytes
        self.syn = 81        # 1 bytes
        self.flg = 0         # 2 bytes
        
        self.dst = 0         # 2 bytes
        self.src = 0         # 2 bytes
        
        self.cmd = 0         # 1 bytes
        self.seq = 0         # 2 bytes
        self.len = 24        # 2 bytes       

        # packet data
        self.variables =  {}
        
        # correction value      
        self.crc = 0         # 2 bytes
        
        # buffers
        self.packet_header_struct = struct.Struct('<B H H H B H H')
        self.packet_header = ctypes.create_string_buffer(self.packet_header_struct.size)
        #self.packet_header = b""
        self._packet_data = b""
        self.packet = b""
        
        self.adapter = None;
        
    def addVariable(self, name, value = None):
        self.variables[name] = value
        
    def getVariable(self, name):
        return self.variables[name]
    
    def getSrc(self):
        return self.dst
    
    def getDst(self):
        return self.dst
    
    def _packVariables(self):
        """ pack variables to ASN1 BER encoded data """
        sequence = AsnVariableSequence()
        i = 0
        
        for name in self.variables:
            
            var = AsnVariable()
            var.setComponentByName("name", univ.OctetString(name))
            
            if (type(self.variables[name]) is int):       
                var.setComponentByName("value", univ.Integer(self.variables[name]))
                
            if (type(self.variables[name]) is float):       
                var.setComponentByName("value", univ.Real(self.variables[name]))
                
            if (type(self.variables[name]) is str):       
                var.setComponentByName("value", univ.OctetString(self.variables[name]))
                
            if (type(self.variables[name]) is bool):       
                var.setComponentByName("value", univ.Boolean(self.variables[name]))
                
            if (self.variables[name] == None):       
                var.setComponentByName("value", univ.Null(self.variables[name]))
                
            sequence.setComponentByPosition(i, var)
            i += 1

        self._packet_data = encoder.encode(sequence)
                
        #log.msg("Variables packed: " + binascii.hexlify(self._packet_data))
        return self._packet_data
    
    def _unpackVariables(self):
        """ unpack ASN1 DER encoded variables from _packet_data """
        self.variables.clear()
        sequence = decoder.decode(self._packet_data, asn1Spec=AsnVariableSequence())

        for i in range(len(sequence[0])):
            var = sequence[0][i]
            c_name = var.getComponentByName("name").getComponent()
            c_value = var.getComponentByName("value").getComponent()
            
            name = c_name._value
            value = c_value._value
            
            # do custom variable casting
            if ( isinstance (c_value, univ.Real) ):
                value = float(c_value)
                
            if ( isinstance (c_value, univ.Boolean) ):
                value = bool(c_value)
            
            # add variable to variables
            self.addVariable(name, value)
    
    def _packHeader(self):
        """ pack header variables to buffer """
        values = (self.syn, self.flg, self.dst, self.src, self.cmd, self.seq, self.len)
        self.packet_header_struct.pack_into(self.packet_header, 0, *values)
        return self.packet_header.raw
    
    def _unpackHeader(self):
        """ unpack header buffer to data """
        (self.syn, self.flg, self.dst, self.src, self.cmd, self.seq, self.len) = self.packet_header_struct.unpack_from(self.packet_header.raw, 0)
        #log.msg( 'Packed   :', binascii.hexlify(self.packet_header.raw), "size: " , len(self.packet_header.raw) )
        #log.msg( 'Unpacked:', self.packet_header_struct.unpack_from(self.packet_header.raw, 0))
        
    def pack(self):
        """ pack message to internal buffer """
        
        # set random seq number
        if( self.seq == 0):
            self.seq = self.getRandomSeq()
        
        # pack data variables
        self._packVariables()
        
        # get data length
        self.len = len(self._packet_data)
        
        # pack header
        self._packHeader()
        
        # combine packet = packet_header + packet_data
        self.packet = self.packet_header.raw + self._packet_data

        return self.packet
    
    def unpack(self, buffer):
        """ unpack message from buffer """
        self.packet = buffer
        self.packet_header.raw = buffer[0:11]
        self._unpackHeader()
        
        self._packet_data = buffer[12:len(buffer)]
        self._unpackVariables()
        
    def getRandomSeq(self):
        return random.randint(1, 65000)      
    
    def toBytes(self):
        return self.pack()
    
    def toDictonary(self):
        dict = self.__dict__.copy()
        dict.pop("packet_header_struct")
        dict.pop("packet_header")
        dict.pop("packet")
        dict.pop("_packet_data")
        dict.pop("adapter")
        return dict
        
    def toString(self):
        return str(self.toDictonary())
    
    def toJson(self):
        return json.dumps(self.toDictonary())
    
    def __str__(self):
        return self.toString()

class AsnVariableName(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('object', univ.ObjectIdentifier()),
        namedtype.NamedType('string', univ.OctetString()),
        )

class AsnVariableValue(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('number', univ.Integer()),
        namedtype.NamedType('string', univ.OctetString()),
        namedtype.NamedType('object', univ.ObjectIdentifier()),
        namedtype.NamedType('real', univ.Real()),
        namedtype.NamedType('boolean', univ.Boolean()),
        namedtype.NamedType('none', univ.Null())
        )

class AsnVariable(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('name', AsnVariableName()),
        namedtype.NamedType('value', AsnVariableValue())
        )
    
class AsnVariableSequence(univ.SequenceOf):
    componentType = AsnVariable()
    
    
class MessageQueue(component.Component):
    def __init__(self):
        
        config = component.get("Config")
        
        # set input queue
        self.inputQueue = Queue()
        component.Component.__init__(self, "MessageQueue")
        
    def put(self, message):
        try:
            self.inputQueue.put_nowait(message)
        except: 
            log.error("Unexpected error:" + sys.exc_info()[0])
            
    def get(self):
        try:
            return self.inputQueue.get()
        except: 
            log.error("Unexpected error:" + sys.exc_info()[0])
            return None
        
    def size(self):
        return self.inputQueue.qsize()
    

        
    
    

        
    

        