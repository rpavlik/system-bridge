"""System Bridge: Settings"""
from __future__ import annotations

import io
import os
from os.path import exists
from uuid import uuid4

from appdirs import AppDirs
from cryptography.fernet import Fernet

from systembridgeshared.base import Base
from systembridgeshared.common import convert_string_to_correct_type
from systembridgeshared.const import (
    COLUMN_KEY,
    COLUMN_TIMESTAMP,
    COLUMN_VALUE,
    SECRET_API_KEY,
    SETTING_ADDITIONAL_MEDIA_DIRECTORIES,
    SETTING_AUTOSTART,
    SETTING_LOG_LEVEL,
    SETTING_PORT_API,
    TABLE_SECRETS,
    TABLE_SETTINGS,
)
from systembridgeshared.database import Database


class Settings(Base):
    """Settings"""

    def __init__(
        self,
        database: Database,
    ) -> None:
        """Initialize"""
        super().__init__()

        self._database = database
        self._database.create_table(
            TABLE_SECRETS,
            [
                (COLUMN_KEY, "TEXT PRIMARY KEY"),
                (COLUMN_VALUE, "TEXT"),
                (COLUMN_TIMESTAMP, "DOUBLE"),
            ],
        )

        self._database.create_table(
            TABLE_SETTINGS,
            [
                (COLUMN_KEY, "TEXT PRIMARY KEY"),
                (COLUMN_VALUE, "TEXT"),
                (COLUMN_TIMESTAMP, "DOUBLE"),
            ],
        )

        # Generate default encryption key
        self._encryption_key = None
        secret_key_path = os.path.join(
            AppDirs("systembridge", "timmo001").user_data_dir, "secret.key"
        )
        if exists(secret_key_path):
            with io.open(secret_key_path, encoding="utf-8") as file:
                self._encryption_key = file.read().splitlines()[0]
        if not self._encryption_key:
            self._encryption_key = Fernet.generate_key()
            with io.open(secret_key_path, "w", encoding="utf-8") as file:
                file.write(self._encryption_key.decode())

        # Default Secrets
        if self._database.check_table_for_key(TABLE_SECRETS, SECRET_API_KEY):
            self.set_secret(SECRET_API_KEY, str(uuid4()))

        # Default Settings
        if self._database.check_table_for_key(TABLE_SETTINGS, SETTING_AUTOSTART):
            self.set(SETTING_AUTOSTART, False)
        if self._database.check_table_for_key(TABLE_SETTINGS, SETTING_LOG_LEVEL):
            self.set(SETTING_LOG_LEVEL, "INFO")
        if self._database.check_table_for_key(TABLE_SETTINGS, SETTING_PORT_API):
            self.set(SETTING_PORT_API, 9170)
        if self._database.check_table_for_key(
            TABLE_SETTINGS, SETTING_ADDITIONAL_MEDIA_DIRECTORIES
        ):
            self.set(SETTING_ADDITIONAL_MEDIA_DIRECTORIES, [])

    def get_all(self) -> list[dict]:
        """Get settings"""
        records = self._database.read_table(TABLE_SETTINGS).to_dict(orient="records")
        for record in records:
            record[COLUMN_VALUE] = convert_string_to_correct_type(record[COLUMN_VALUE])
        return records

    def get(
        self,
        key: str,
    ) -> bool | float | int | str | list | dict | None:
        """Get setting"""
        record = self._database.read_table_by_key(TABLE_SETTINGS, key).to_dict(
            orient="records"
        )
        return (
            convert_string_to_correct_type(record[0]["value"])
            if record and len(record) > 0
            else None
        )

    def get_secret(
        self,
        key: str,
    ) -> str:
        """Get secret"""
        record = self._database.read_table_by_key(TABLE_SECRETS, key).to_dict(
            orient="records"
        )
        if not record or len(record) < 1:
            raise KeyError(f"Secret {key} not found")

        secret = record[0]["value"]
        fernet = Fernet(self._encryption_key)  # type: ignore
        return fernet.decrypt(secret.encode()).decode()

    def set(
        self,
        key: str,
        value: bool | float | int | str | list | dict | None,
    ) -> None:
        """Set setting"""
        self._database.write(TABLE_SETTINGS, key, value)

    def set_secret(
        self,
        key: str,
        value: str,
    ) -> None:
        """Set secret"""
        fernet = Fernet(self._encryption_key)  # type: ignore

        self._database.write(
            TABLE_SECRETS, key, fernet.encrypt(value.encode()).decode()
        )
