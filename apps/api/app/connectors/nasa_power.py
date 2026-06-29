from typing import Any

from app.connectors.base import fetch_json
from app.core.config import Settings
from app.schemas.data_sources import ConnectorResponse


async def get_climate_daily(
    settings: Settings,
    latitude: float,
    longitude: float,
    start: str,
    end: str,
) -> ConnectorResponse:
    params: dict[str, Any] = {
        "parameters": "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,WS10M",
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": start,
        "end": end,
        "format": "JSON",
    }
    request_url, data = await fetch_json(settings.nasa_power_base_url, "temporal/daily/point", params)
    return ConnectorResponse(source="nasa_power", request_url=request_url, params=params, data=data)
