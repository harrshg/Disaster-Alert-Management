from typing import Any

from app.connectors.base import fetch_json
from app.core.config import Settings
from app.schemas.data_sources import ConnectorResponse


async def get_weather_forecast(
    settings: Settings,
    latitude: float,
    longitude: float,
    forecast_days: int,
) -> ConnectorResponse:
    params: dict[str, Any] = {
        "latitude": latitude,
        "longitude": longitude,
        "forecast_days": forecast_days,
        "current": "temperature_2m,relative_humidity_2m,precipitation,rain,snowfall,weather_code,wind_speed_10m",
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,rain,snowfall,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,snowfall_sum,wind_speed_10m_max",
        "timezone": "auto",
    }
    request_url, data = await fetch_json(settings.open_meteo_base_url, "forecast", params)
    return ConnectorResponse(source="open_meteo", request_url=request_url, params=params, data=data)
