from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.common import SourceMetadata
from app.schemas.location import Location
from app.schemas.observation import WeatherMetrics


class ForecastPeriod(BaseModel):
    starts_at: datetime
    ends_at: datetime
    weather: WeatherMetrics
    probability_percent: float | None = Field(default=None, ge=0, le=100)


class Forecast(BaseModel):
    id: str | None = None
    issued_at: datetime
    location: Location
    source: SourceMetadata
    periods: list[ForecastPeriod]
    raw_payload: dict[str, Any] = Field(default_factory=dict)
