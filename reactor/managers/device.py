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
        
    def register(self, device):
        if (self.get_device_by_address(device.address) == None and self.get_device_by_id(device.id) == None):
            self.devices.append(device)
            logger.debug("Device registred: " + str(device))
    
    def get_device_by_address(self,  address):
        for device in self.devices:
            if (device.address == address):
                return device;
            
    def get_device_by_id(self,  _id):
        for device in self.devices:
            if (device.id == _id):
                return device;
            
    def get_device(self, id_or_address):
        if (isinstance(id_or_address, (int))):
            return self.get_device_by_id(id_or_address)
        else:
            return self.get_device_by_address(id_or_address)