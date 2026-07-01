from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.common import ConfidenceLevel, HazardType, SeverityLevel, SourceMetadata
from app.schemas.location import Location


class Hazard(BaseModel):
    id: str | None = None
    hazard_type: HazardType
    severity: SeverityLevel
    title: str
    description: str
    location: Location
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    source: SourceMetadata
    indicators: dict[str, Any] = Field(default_factory=dict)


class RiskScore(BaseModel):
    id: str | None = None
    hazard_type: HazardType
    location: Location
    score: float = Field(ge=0, le=1)
    severity: SeverityLevel
    confidence: ConfidenceLevel
    calculated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    model_name: str | None = None
    model_version: str | None = None
    explanation: str
    contributing_factors: list[str] = Field(default_factory=list)
    source_observation_ids: list[str] = Field(default_factory=list)
