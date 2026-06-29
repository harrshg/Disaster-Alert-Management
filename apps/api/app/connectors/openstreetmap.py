from typing import Any

from app.connectors.base import fetch_json
from app.core.config import Settings
from app.schemas.data_sources import ConnectorResponse


async def geocode_place(settings: Settings, query: str, limit: int) -> ConnectorResponse:
    params: dict[str, Any] = {
        "q": query,
        "format": "jsonv2",
        "limit": limit,
        "addressdetails": 1,
    }
    headers = {"User-Agent": f"{settings.app_name}/0.1.0"}
    request_url, data = await fetch_json(
        settings.openstreetmap_nominatim_base_url,
        "search",
        params,
        headers,
    )
    return ConnectorResponse(
        source="openstreetmap_nominatim",
        request_url=request_url,
        params=params,
        data={"results": data},
    )


async def reverse_geocode(settings: Settings, latitude: float, longitude: float) -> ConnectorResponse:
    params: dict[str, Any] = {
        "lat": latitude,
        "lon": longitude,
        "format": "jsonv2",
        "addressdetails": 1,
    }
    headers = {"User-Agent": f"{settings.app_name}/0.1.0"}
    request_url, data = await fetch_json(
        settings.openstreetmap_nominatim_base_url,
        "reverse",
        params,
        headers,
    )
    return ConnectorResponse(
        source="openstreetmap_nominatim",
        request_url=request_url,
        params=params,
        data=data,
    )
