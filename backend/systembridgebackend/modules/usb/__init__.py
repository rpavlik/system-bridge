"""USB Bridge: USB"""
from __future__ import annotations
from usb.core import find as find_usb_devices
from usb.util import get_string as get_usb_string

from systembridgeshared.base import Base


class USB(Base):
    """USB"""

    def devices(self) -> list:
        """Get USB devices"""
        devices = []
        for device in find_usb_devices(find_all=True):
            devices.append(
                {
                    "address": device.address,
                    "bus": device.bus,
                    "configuration_index": device.configuration_index,
                    "configuration_value": device.configuration_value,
                    "configuration": device.configuration,
                    "device_class": device.device_class,
                    "device_power": device.device_power,
                    "device_protocol": device.device_protocol,
                    "device_release": device.device_release,
                    "device_speed": device.device_speed,
                    "device_subclass": device.device_subclass,
                    "device_version": device.device_version,
                    "interface_alternate": device.interface_alternate,
                    "interface_class": device.interface_class,
                    "interface_number": device.interface_number,
                    "interface_protocol": device.interface_protocol,
                    "interface_subclass": device.interface_subclass,
                    "interface": device.interface,
                    "manufacturer": get_usb_string(device, device.iManufacturer),
                    "port": device.port_number,
                    "product_name": get_usb_string(device, device.iProduct),
                    "product": get_usb_string(device, device.idProduct),
                    "serial": get_usb_string(device, device.iSerialNumber),
                    "speed": device.speed,
                    "vendor": get_usb_string(device, device.idVendor),
                }
            )

        return devices
