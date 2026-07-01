from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class HazardType(StrEnum):
    earthquake = "earthquake"
    flood = "flood"
    heatwave = "heatwave"
    heavy_rain = "heavy_rain"
    landslide = "landslide"
    snowfall = "snowfall"
    storm = "storm"
    wildfire = "wildfire"
    coastal = "coastal"
    unknown = "unknown"


class SeverityLevel(StrEnum):
    low = "low"
    moderate = "moderate"
    high = "high"
    severe = "severe"
    critical = "critical"


class ConfidenceLevel(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class SourceMetadata(BaseModel):
    source_name: str
    source_url: str | None = None
    collected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    raw_reference: str | None = None
    quality_score: float | None = Field(default=None, ge=0, le=1)
    metadata: dict[str, Any] = Field(default_factory=dict)
