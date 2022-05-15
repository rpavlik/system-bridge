"""USB Bridge: Update USB"""
import asyncio

from systembridgeshared.database import Database

from systembridgebackend.modules.base import ModuleUpdateBase
from systembridgebackend.modules.usb import USB


class USBUpdate(ModuleUpdateBase):
    """USB Update"""

    def __init__(
        self,
        database: Database,
    ) -> None:
        """Initialize"""
        super().__init__(database, "usb")
        self._usb = USB()

    async def update_devices(self) -> None:
        """Update devices"""
        for device in self._usb.devices():
            self._logger.info("Device: %s", device)
            # await self._database.write(
            #     "usb",
            #     f"device_{device['address']}",
            #     device,
            # )

    async def update_all_data(self) -> None:
        """Update data"""
        await asyncio.gather(
            *[
                self.update_devices(),
            ]
        )
