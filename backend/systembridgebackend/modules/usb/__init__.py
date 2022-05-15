"""USB Bridge: USB"""
from __future__ import annotations

import libusb_package
from systembridgeshared.base import Base


class USB(Base):
    """USB"""

    def devices(self) -> list:
        """Get USB devices"""
        devices = []
        for device in libusb_package.find(find_all=True):
            self._logger.info("Found device: %s", device)
            devices.append(
                {
                    "address": device.address,
                    "bus": device.bus,
                    "id_product": device.idProduct,
                    "id_vendor": device.idVendor,
                    "manufacturer": device.iManufacturer,
                    "port": device.port_number,
                    "product": device.iProduct,
                    "serial": device.iSerialNumber,
                    "speed": device.speed,
                }
            )

        return devices
