from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.common import SourceMetadata
from app.schemas.location import Location


class WeatherMetrics(BaseModel):
    temperature_celsius: float | None = None
    humidity_percent: float | None = Field(default=None, ge=0, le=100)
    precipitation_mm: float | None = Field(default=None, ge=0)
    rain_mm: float | None = Field(default=None, ge=0)
    snowfall_cm: float | None = Field(default=None, ge=0)
    wind_speed_kph: float | None = Field(default=None, ge=0)
    pressure_hpa: float | None = Field(default=None, ge=0)


class SeismicMetrics(BaseModel):
    magnitude: float | None = Field(default=None, ge=0)
    depth_km: float | None = None
    event_id: str | None = None


class Observation(BaseModel):
    id: str | None = None
    observed_at: datetime
    location: Location
    source: SourceMetadata
    weather: WeatherMetrics | None = None
    seismic: SeismicMetrics | None = None
    raw_payload: dict[str, Any] = Field(default_factory=dict)
