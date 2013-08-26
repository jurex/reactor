from reactor import component
from reactor.models.device import Device

import logging
logger = logging.getLogger("DeviceManager")

class DeviceManager(component.Component):
    def __init__(self):
        # init devices
        self.devices = []
        
        # component constructor
        component.Component.__init__(self, "DeviceManager")
        
    def register(self, address, adapter, server):
        if (self.getDeviceByAddress(address) == None):
            device = Device()
            device.address = address
            device.adapter = adapter
            device.server = server
            self.devices.append(device)
            logger.debug("Device \""+str(address)+"\" registred")
    
    def getDeviceByAddress(self,  address):
        for device in self.devices:
            if (device.address == address):
                return device;
            
    def getDeviceById(self,  _id):
        for device in self.devices:
            if (device.id == _id):
                return device;
            
    def getDevice(self, id_or_address):
        if (isinstance(id_or_address, (int))):
            return self.getDeviceById(id_or_address)
        else:
            return self.getDeviceByAddress(id_or_address)