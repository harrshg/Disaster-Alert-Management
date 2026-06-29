from typing import Any

from app.connectors.base import fetch_json
from app.core.config import Settings
from app.schemas.data_sources import ConnectorResponse


async def get_recent_earthquakes(
    settings: Settings,
    latitude: float | None,
    longitude: float | None,
    radius_km: float,
    min_magnitude: float,
    limit: int,
) -> ConnectorResponse:
    params: dict[str, Any] = {
        "format": "geojson",
        "orderby": "time",
        "minmagnitude": min_magnitude,
        "limit": limit,
    }

    if latitude is not None and longitude is not None:
        params.update(
            {
                "latitude": latitude,
                "longitude": longitude,
                "maxradiuskm": radius_km,
            }
        )

    request_url, data = await fetch_json(settings.usgs_earthquake_base_url, "query", params)
    return ConnectorResponse(source="usgs_earthquake", request_url=request_url, params=params, data=data)
