# generated by datamodel-codegen:
#   filename:  gpu.json

from __future__ import annotations

from pydantic import BaseModel, Extra, Field


class LastUpdated(BaseModel):
    """
    Last updated
    """

    class Config:
        extra = Extra.allow

    gpus: float


class Gpu(BaseModel):
    """
    GPU
    """

    class Config:
        extra = Extra.allow

    gpus: list
    last_updated: LastUpdated = Field(..., description="Last updated")
