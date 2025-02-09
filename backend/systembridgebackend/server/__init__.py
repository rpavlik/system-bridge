"""System Bridge: Server"""
import asyncio
from collections.abc import Callable
from datetime import timedelta
import os
from os import walk
import sys

from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic_scheduler import SanicScheduler, task
from systembridgeshared.base import Base
from systembridgeshared.const import (
    QUERY_API_KEY,
    SECRET_API_KEY,
    SETTING_LOG_LEVEL,
    SETTING_PORT_API,
)
from systembridgeshared.database import Database
from systembridgeshared.models.media_play import MediaPlay
from systembridgeshared.models.notification import Notification
from systembridgeshared.settings import Settings

from systembridgebackend.data import Data
from systembridgebackend.gui import GUIAttemptsExceededException, start_gui_threaded
from systembridgebackend.modules.listeners import Listeners
from systembridgebackend.server.auth import ApiKeyAuthentication
from systembridgebackend.server.cors import add_cors_headers
from systembridgebackend.server.keyboard import handler_keyboard
from systembridgebackend.server.mdns import MDNSAdvertisement
from systembridgebackend.server.media import (
    handler_media_directories,
    handler_media_file,
    handler_media_file_data,
    handler_media_file_write,
    handler_media_files,
    handler_media_play,
)
from systembridgebackend.server.notification import handler_notification
from systembridgebackend.server.open import handler_open
from systembridgebackend.server.options import setup_options
from systembridgebackend.server.power import (
    handler_hibernate,
    handler_lock,
    handler_logout,
    handler_restart,
    handler_shutdown,
    handler_sleep,
)
from systembridgebackend.server.update import handler_update
from systembridgebackend.server.websocket import WebSocketHandler


class ApplicationExitException(BaseException):
    """Forces application to close."""


class Server(Base):
    """Server"""

    def __init__(
        self,
        database: Database,
        settings: Settings,
    ) -> None:
        """Initialize"""
        super().__init__()
        self._database = database
        self._settings = settings
        self._server = Sanic("SystemBridge")
        # Add OPTIONS handlers to any route that is missing it
        self._server.register_listener(setup_options, "before_server_start")
        # Fill in CORS headers
        self._server.register_middleware(add_cors_headers, "response")

        implemented_modules = []
        for _, dirs, _ in walk(os.path.join(os.path.dirname(__file__), "../modules")):
            implemented_modules = list(filter(lambda d: "__" not in d, dirs))
            break

        SanicScheduler(self._server, utc=True)
        self._listeners = Listeners(self._database, implemented_modules)
        self._data = Data(self._database, self._callback_data_updated)

        auth = ApiKeyAuthentication(
            app=self._server,
            arg=QUERY_API_KEY,
            header="api-key",
            keys=[self._settings.get_secret(SECRET_API_KEY)],
        )

        mdns_advertisement = MDNSAdvertisement(self._settings)
        mdns_advertisement.advertise_server()

        @task(start=timedelta(seconds=2))
        async def _after_startup(_) -> None:
            """After startup"""
            if "--no-gui" not in sys.argv:
                try:
                    start_gui_threaded(self._logger, self._settings)
                except GUIAttemptsExceededException:
                    self._logger.error("GUI could not be started. Exiting application")
                    self._exit_application()

        @task(
            start=timedelta(seconds=10),
            period=timedelta(minutes=2),
        )
        async def _update_data(_) -> None:
            """Update data"""
            self._data.request_update_data()

        @task(
            start=timedelta(seconds=10),
            period=timedelta(seconds=30),
        )
        async def _update_frequent_data(_) -> None:
            """Update frequent data"""
            self._data.request_update_frequent_data()

        @auth.key_required
        async def _handler_data_all(
            _: Request,
            table: str,
        ) -> HTTPResponse:
            """Data handler all"""
            if table not in implemented_modules:
                return json({"message": f"Data module {table} not found"}, status=404)
            return json(self._database.table_data_to_ordered_dict(table))

        @auth.key_required
        async def _handler_data_by_key(
            _: Request,
            table: str,
            key: str,
        ) -> HTTPResponse:
            """Data handler by key"""
            if table not in implemented_modules:
                return json({"message": f"Data module {table} not found"}, status=404)

            data = self._database.read_table_by_key(table, key).to_dict(
                orient="records"
            )[0]
            return json(
                {
                    data["key"]: data["value"],
                    "last_updated": data["timestamp"],
                }
            )

        @auth.key_required
        async def _handler_generic(
            request: Request,
            function: Callable,
        ) -> HTTPResponse:
            """Generic handler"""
            return await function(request, self._settings)

        @auth.key_required
        async def _handler_media_play(request: Request) -> HTTPResponse:
            """Media play handler"""
            return await handler_media_play(
                request,
                self._settings,
                self._callback_media_play,
            )

        @auth.key_required
        async def _handler_notification(request: Request) -> HTTPResponse:
            """Notification handler"""
            return await handler_notification(
                request,
                self._settings,
                self._callback_notification,
            )

        async def _handler_websocket(
            _: Request,
            socket,
        ) -> None:
            """WebSocket handler"""
            websocket = WebSocketHandler(
                self._database,
                self._settings,
                self._listeners,
                implemented_modules,
                socket,
                self._exit_application,
            )
            await websocket.handler()

        self._server.add_route(
            _handler_data_all,
            "/api/data/<table:str>",
            methods=["GET"],
            name="Data",
        )
        self._server.add_route(
            _handler_data_by_key,
            "/api/data/<table:str>/<key:str>",
            methods=["GET"],
            name="Data by Key",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_keyboard),
            "/api/keyboard",
            methods=["POST"],
            name="Keyboard",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_media_directories),
            "/api/media",
            methods=["GET"],
            name="Media Directories",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_media_files),
            "/api/media/files",
            methods=["GET"],
            name="Media Files",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_media_file),
            "/api/media/file",
            methods=["GET"],
            name="Media File",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_media_file_data),
            "/api/media/file/data",
            methods=["GET"],
            name="Media File Data",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_media_file_write),
            "/api/media/file/write",
            methods=["POST"],
            name="Media File Write",
        )
        self._server.add_route(
            _handler_media_play,
            "/api/media/play",
            methods=["POST"],
            name="Media Play",
        )
        self._server.add_route(
            _handler_notification,
            "/api/notification",
            methods=["POST"],
            name="Notification",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_open),
            "/api/open",
            methods=["POST"],
            name="Open",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_sleep),
            "/api/power/sleep",
            methods=["POST"],
            name="Power Sleep",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_hibernate),
            "/api/power/hibernate",
            methods=["POST"],
            name="Power Hibernate",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_restart),
            "/api/power/restart",
            methods=["POST"],
            name="Power Restart",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_shutdown),
            "/api/power/shutdown",
            methods=["POST"],
            name="Power Shutdown",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_lock),
            "/api/power/lock",
            methods=["POST"],
            name="Power Lock",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_logout),
            "/api/power/logout",
            methods=["POST"],
            name="Power Logout",
        )
        self._server.add_route(
            lambda r: _handler_generic(r, handler_update),
            "/api/update",
            methods=["POST"],
            name="Update",
        )

        if "--no-frontend" not in sys.argv:
            try:
                # pylint: disable=import-error, import-outside-toplevel
                from systembridgefrontend import get_frontend_path

                frontend_path = get_frontend_path()
                self._logger.info("Serving frontend from: %s", frontend_path)
                self._server.static(
                    "/",
                    frontend_path,
                    strict_slashes=False,
                    content_type="text/html",
                    name="Frontend",
                )
            except (ImportError, ModuleNotFoundError) as error:
                self._logger.error("Frontend not found: %s", error)

        self._server.add_websocket_route(
            _handler_websocket,
            "/api/websocket",
            name="WebSocket",
        )

    async def _callback_data_updated(
        self,
        module: str,
    ) -> None:
        """Data updated"""
        await self._listeners.refresh_data_by_module(module)

    def _exit_application(self) -> None:
        """Exit application"""
        self.stop_server()
        self._logger.info("Server stopped. Exiting application")
        sys.exit(0)

    def _callback_media_play(
        self,
        media_type: str,
        media_play: MediaPlay,
    ) -> None:
        """Callback to open media player"""
        start_gui_threaded(
            self._logger,
            self._settings,
            "media-player",
            media_type,
            media_play.json(),
        )

    def _callback_notification(
        self,
        notification: Notification,
    ) -> None:
        """Callback to open media player"""
        start_gui_threaded(
            self._logger,
            self._settings,
            "notification",
            notification.json(),
        )

    def start_server(self) -> None:
        """Start Server"""
        if (port := self._settings.get(SETTING_PORT_API)) is None:
            raise ValueError("Port not set")
        self._logger.info("Starting server on port: %s", port)
        self._server.run(
            host="0.0.0.0",
            port=int(port),  # type: ignore
            access_log=False,
            debug=self._settings.get(SETTING_LOG_LEVEL) == "DEBUG",
            motd=False,
        )

    def stop_server(self) -> None:
        """Stop Server"""
        self._logger.info("Stopping server")
        loop = self._server.loop
        self._logger.info("Cancel any pending tasks")
        for pending_task in asyncio.all_tasks():
            pending_task.cancel()
        self._logger.info("Stop the event loop")
        loop.stop()
        self._listeners.remove_all_listeners()
        self._server.stop()
