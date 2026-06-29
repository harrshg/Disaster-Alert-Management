from typing import Any

from pydantic import BaseModel, Field


class ConnectorResponse(BaseModel):
    source: str
    request_url: str
    params: dict[str, Any]
    data: dict[str, Any]


class DataSourceStatus(BaseModel):
    name: str
    type: str
    key_required: bool
    configured: bool
    base_url: str


class DataSourceStatusResponse(BaseModel):
    sources: list[DataSourceStatus]


class LocationQuery(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
