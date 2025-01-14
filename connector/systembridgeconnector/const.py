"""System Bridge Connector: Constants"""
from systembridgeconnector.models.battery import Battery
from systembridgeconnector.models.bridge import Bridge
from systembridgeconnector.models.cpu import Cpu
from systembridgeconnector.models.data import Data
from systembridgeconnector.models.disk import Disk
from systembridgeconnector.models.display import Display
from systembridgeconnector.models.generic import Generic
from systembridgeconnector.models.gpu import Gpu
from systembridgeconnector.models.keyboard_key import KeyboardKey
from systembridgeconnector.models.keyboard_text import KeyboardText
from systembridgeconnector.models.media_directories import MediaDirectories
from systembridgeconnector.models.media_files import File, MediaFiles
from systembridgeconnector.models.memory import Memory
from systembridgeconnector.models.network import Network
from systembridgeconnector.models.notification import Notification
from systembridgeconnector.models.open_path import OpenPath
from systembridgeconnector.models.open_url import OpenUrl
from systembridgeconnector.models.response import Response
from systembridgeconnector.models.sensors import Sensors
from systembridgeconnector.models.system import System

# Settings
SETTING_ADDITIONAL_MEDIA_DIRECTORIES = "additional_media_directories"
SETTING_AUTOSTART = "autostart"
SETTING_LOG_LEVEL = "log_level"
SETTING_PORT_API = "port_api"

# Secrets
SECRET_API_KEY = "api_key"

# Query Parameters
QUERY_ALBUM = "album"
QUERY_API_KEY = "apiKey"
QUERY_API_PORT = "apiPort"
QUERY_ARTIST = "artist"
QUERY_AUTOPLAY = "autoplay"
QUERY_BASE = "base"
QUERY_FILENAME = "filename"
QUERY_PATH = "path"
QUERY_TITLE = "title"
QUERY_URL = "url"
QUERY_VOLUME = "volume"


# Event Keys
EVENT_API_KEY = "api-key"
EVENT_APP_ICON = "app_icon"
EVENT_APP_NAME = "app_name"
EVENT_BASE = "base"
EVENT_DATA = "data"
EVENT_DIRECTORIES = "directories"
EVENT_EVENT = "event"
EVENT_FILE = "file"
EVENT_FILENAME = "filename"
EVENT_FILES = "files"
EVENT_ID = "id"
EVENT_KEY = "key"
EVENT_MESSAGE = "message"
EVENT_MODULE = "module"
EVENT_MODULES = "modules"
EVENT_PATH = "path"
EVENT_SETTING = "setting"
EVENT_SUBTYPE = "subtype"
EVENT_TEXT = "text"
EVENT_TIMEOUT = "timeout"
EVENT_TITLE = "title"
EVENT_TYPE = "type"
EVENT_URL = "url"
EVENT_VALUE = "value"
EVENT_VERSION = "version"
EVENT_VERSIONS = "versions"

# Event Types
SUBTYPE_BAD_API_KEY = "BAD_API_KEY"
SUBTYPE_BAD_DIRECTORY = "BAD_DIRECTORY"
SUBTYPE_BAD_FILE = "BAD_FILE"
SUBTYPE_BAD_JSON = "BAD_JSON"
SUBTYPE_BAD_KEY = "MISSING_KEY"
SUBTYPE_BAD_PATH = "BAD_PATH"
SUBTYPE_BAD_REQUEST = "BAD_REQUEST"
SUBTYPE_LISTENER_ALREADY_REGISTERED = "LISTENER_ALREADY_REGISTERED"
SUBTYPE_LISTENER_NOT_REGISTERED = "LISTENER_NOT_REGISTERED"
SUBTYPE_MISSING_API_KEY = "MISSING_API_KEY"
SUBTYPE_MISSING_BASE = "MISSING_BASE"
SUBTYPE_MISSING_KEY = "MISSING_KEY"
SUBTYPE_MISSING_TITLE = "MISSING_TITLE"
SUBTYPE_MISSING_MODULES = "MISSING_MODULES"
SUBTYPE_MISSING_PATH = "MISSING_PATH"
SUBTYPE_MISSING_PATH_URL = "MISSING_PATH_URL"
SUBTYPE_MISSING_SETTING = "MISSING_SETTING"
SUBTYPE_MISSING_TEXT = "MISSING_TEXT"
SUBTYPE_MISSING_VALUE = "MISSING_VALUE"
SUBTYPE_UNKNOWN_EVENT = "UNKNOWN_EVENT"
TYPE_APPLICATION_UPDATE = "APPLICATION_UPDATE"
TYPE_APPLICATION_UPDATING = "APPLICATION_UPDATING"
TYPE_DATA_GET = "DATA_GET"
TYPE_DATA_LISTENER_REGISTERED = "DATA_LISTENER_REGISTERED"
TYPE_DATA_LISTENER_UNREGISTERED = "DATA_LISTENER_UNREGISTERED"
TYPE_DATA_UPDATE = "DATA_UPDATE"
TYPE_DIRECTORIES = "DIRECTORIES"
TYPE_ERROR = "ERROR"
TYPE_EXIT_APPLICATION = "EXIT_APPLICATION"
TYPE_FILE = "FILE"
TYPE_FILES = "FILES"
TYPE_GET_DATA = "GET_DATA"
TYPE_GET_DIRECTORIES = "GET_DIRECTORIES"
TYPE_GET_FILE = "GET_FILE"
TYPE_GET_FILES = "GET_FILES"
TYPE_GET_SETTING = "GET_SETTING"
TYPE_GET_SETTINGS = "GET_SETTINGS"
TYPE_KEYBOARD_KEY_PRESSED = "KEYBOARD_KEY_PRESSED"
TYPE_KEYBOARD_KEYPRESS = "KEYBOARD_KEYPRESS"
TYPE_KEYBOARD_TEXT = "KEYBOARD_TEXT"
TYPE_KEYBOARD_TEXT_SENT = "KEYBOARD_TEXT_SENT"
TYPE_NOTIFICATION = "NOTIFICATION"
TYPE_NOTIFICATION_SENT = "NOTIFICATION_SENT"
TYPE_OPEN = "OPEN"
TYPE_OPENED = "OPENED"
TYPE_POWER_HIBERNATE = "POWER_HIBERNATE"
TYPE_POWER_HIBERNATING = "POWER_HIBERNATING"
TYPE_POWER_LOCK = "POWER_LOCK"
TYPE_POWER_LOCKING = "POWER_LOCKING"
TYPE_POWER_LOGGINGOUT = "POWER_LOGGINGOUT"
TYPE_POWER_LOGOUT = "POWER_LOGOUT"
TYPE_POWER_RESTART = "POWER_RESTART"
TYPE_POWER_RESTARTING = "POWER_RESTARTING"
TYPE_POWER_SHUTDOWN = "POWER_SHUTDOWN"
TYPE_POWER_SHUTTINGDOWN = "POWER_SHUTTINGDOWN"
TYPE_POWER_SLEEP = "POWER_SLEEP"
TYPE_POWER_SLEEPING = "POWER_SLEEPING"
TYPE_REGISTER_DATA_LISTENER = "REGISTER_DATA_LISTENER"
TYPE_SETTING_RESULT = "SETTING_RESULT"
TYPE_SETTING_UPDATED = "SETTING_UPDATED"
TYPE_SETTINGS_RESULT = "SETTINGS_RESULT"
TYPE_UNREGISTER_DATA_LISTENER = "UNREGISTER_DATA_LISTENER"
TYPE_UPDATE_SETTING = "UPDATE_SETTING"

# Model
MODEL_BATTERY = "battery"
MODEL_BRIDGE = "bridge"
MODEL_CPU = "cpu"
MODEL_DATA = "data"
MODEL_DISK = "disk"
MODEL_DISPLAY = "display"
MODEL_GENERIC = "generic"
MODEL_GPU = "gpu"
MODEL_KEYBOARD_KEY = "keyboard_key"
MODEL_KEYBOARD_TEXT = "keyboard_text"
MODEL_MEDIA_DIRECTORIES = "media_directories"
MODEL_MEDIA_FILES = "media_files"
MODEL_MEDIA_FILE = "media_file"
MODEL_MEMORY = "memory"
MODEL_NETWORK = "network"
MODEL_NOTIFICATION = "notification"
MODEL_OPEN_PATH = "open_path"
MODEL_OPEN_URL = "open_url"
MODEL_RESPONSE = "response"
MODEL_SENSORS = "sensors"
MODEL_SYSTEM = "system"

MODEL_MAP = {
    MODEL_BATTERY: Battery,
    MODEL_BRIDGE: Bridge,
    MODEL_CPU: Cpu,
    MODEL_DATA: Data,
    MODEL_DISK: Disk,
    MODEL_DISPLAY: Display,
    MODEL_GENERIC: Generic,
    MODEL_GPU: Gpu,
    MODEL_KEYBOARD_KEY: KeyboardKey,
    MODEL_KEYBOARD_TEXT: KeyboardText,
    MODEL_MEDIA_DIRECTORIES: MediaDirectories,
    MODEL_MEDIA_FILE: File,
    MODEL_MEDIA_FILES: MediaFiles,
    MODEL_MEMORY: Memory,
    MODEL_NETWORK: Network,
    MODEL_NOTIFICATION: Notification,
    MODEL_OPEN_PATH: OpenPath,
    MODEL_OPEN_URL: OpenUrl,
    MODEL_RESPONSE: Response,
    MODEL_SENSORS: Sensors,
    MODEL_SYSTEM: System,
}
