# generated by datamodel-codegen:
#   filename:  media_directories.json

from __future__ import annotations

from pydantic import BaseModel, Field


class MediaDirectories(BaseModel):
    """
    Media Directories
    """

    __root__: list[str] = Field(..., description="Media Directories")
