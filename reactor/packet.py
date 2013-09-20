# packet definition
import struct
import ctypes
import binascii
import json
import random

from pyasn1.type import univ
from pyasn1.codec.ber import encoder, decoder
from pyasn1.type import univ,namedtype,namedval,tag,constraint

from reactor import logger

"""
class Packet(object):
    
    def pack(self):
        # pack attributes to raw bytes
        raise NotImplementedError( "Method not implemented" )
        
    def unpack(self, buffer):
        # unpack raw bytes to attributest
        raise NotImplementedError( "Method not implemented" )
"""

PACKET_HEADER_STRUCT = struct.Struct('<B H H H B H H')

class Packet(object):
    
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
        self.data =  {}
        
        # correction value      
        self.crc = 0         # 2 bytes
        
        # buffers
        self._packet_header = ctypes.create_string_buffer(PACKET_HEADER_STRUCT.size)
        self._packet_data = b""
        self._packet = b""
        
    def add_data(self, name, value = None):
        self.data[name] = value
        
    def get_data(self, name):
        return self.data[name]
    
    def get_src(self):
        return self.dst
    
    def get_dst(self):
        return self.dst
    
    def _pack_data(self):
        """ pack variables to ASN1 BER encoded data """
        sequence = AsnVariableSequence()
        i = 0
        
        for name in self.data:
            
            var = AsnVariable()
            var.setComponentByName("name", univ.OctetString(name))
            
            if (type(self.data[name]) is int):       
                var.setComponentByName("value", univ.Integer(self.data[name]))
                
            elif (type(self.data[name]) is float):       
                var.setComponentByName("value", univ.Real(self.data[name]))
                
            elif (type(self.data[name]) is str):       
                var.setComponentByName("value", univ.OctetString(self.data[name]))
            
            elif (type(self.data[name]) is bool):       
                var.setComponentByName("value", univ.Boolean(self.data[name]))
               
            elif (self.data[name] == None):       
                var.setComponentByName("value", univ.Null(self.data[name]))
                
            else:
                var.setComponentByName("value", univ.OctetString(str(self.data[name])))
                #raise NameError("unknown data type: " + str(name) + " : " + str(self.data[name]))   
                
            sequence.setComponentByPosition(i, var)
            i += 1

        self._packet_data = encoder.encode(sequence)
        #log.msg("Data packed: " + binascii.hexlify(self._packet_data))
        return self._packet_data
    
    def _unpack_data(self):
        """ unpack ASN1 DER encoded variables from _packet_data """
        self.data.clear()
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
            self.add_data(name, value)
    
    def _pack_header(self):
        """ pack header variables to buffer """
        values = (self.syn, self.flg, self.dst, self.src, self.cmd, self.seq, self.len)
        PACKET_HEADER_STRUCT.pack_into(self._packet_header, 0, *values)
        return self._packet_header.raw
    
    def _unpack_header(self):
        """ unpack header buffer to data """
        (self.syn, self.flg, self.dst, self.src, self.cmd, self.seq, self.len) = PACKET_HEADER_STRUCT.unpack_from(self._packet_header.raw, 0)
        #log.msg( 'Packed   :', binascii.hexlify(self.packet_header.raw), "size: " , len(self.packet_header.raw) )
        #log.msg( 'Unpacked:', self.packet_header_struct.unpack_from(self.packet_header.raw, 0))
        
    def pack(self):
        """ pack message to internal buffer """
        
        # init buffers
        self._packet_header = ctypes.create_string_buffer(PACKET_HEADER_STRUCT.size)
        self._packet_data = b""
        self._packet = b""
        
        # set random seq number
        if( self.seq == 0):
            self.seq = self.get_random_seq()
        
        # pack data variables
        self._pack_data()
        
        # get data length
        self.len = len(self._packet_data)
        
        # pack header
        self._pack_header()
        
        # combine packet = packet_header + packet_data
        self._packet = self._packet_header.raw + self._packet_data

        return self._packet
    
    def unpack(self, buffer):
        """ unpack message from buffer """
        
        # int buffers
        self._packet_header = ctypes.create_string_buffer(PACKET_HEADER_STRUCT.size)
        self._packet_data = b""
        self._packet = b""
        
        self._packet = buffer
        self._packet_header.raw = buffer[0:11]
        self._unpack_header()
        
        self._packet_data = buffer[12:len(buffer)]
        self._unpack_data()
        
    def get_random_seq(self):
        return random.randint(1, 65000)      
    
    def to_bytes(self):
        return self.pack()
    
    def to_dict(self):
        d = self.__dict__.copy()
        
        if("_packet_header" in d):
            d.pop("_packet_header")
        
        if("_packet_data" in d):
            d.pop("_packet_data")
            
        if("_packet" in d):
            d.pop("_packet")

        return d
        
    def to_string(self):
        return str(self.to_dict())
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def __str__(self):
        return self.to_string()

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

        
    
    

        
    

        