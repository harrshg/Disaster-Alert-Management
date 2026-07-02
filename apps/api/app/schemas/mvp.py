from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.alert import Alert
from app.schemas.location import Location
from app.schemas.risk import Hazard, RiskScore
from app.schemas.travel import TravelRiskAssessment, VehicleType


class RiskAssessmentRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    place_name: str | None = None
    forecast_days: int = Field(default=3, ge=1, le=7)


class RiskAssessmentResponse(BaseModel):
    location: Location
    risk_scores: list[RiskScore]
    hazards: list[Hazard]
    summary: str
    recommended_actions: list[str]
    data_sources: list[str]


class NaturalLanguageTravelRequest(BaseModel):
    message: str = Field(min_length=10, max_length=1000)
    vehicle_type: VehicleType | None = None
    starts_at: datetime | None = None


class TravelAssessmentResponse(BaseModel):
    parsed_origin: str | None
    parsed_destination: str | None
    assessment: TravelRiskAssessment
    warnings: list[str]


class AlertPreviewRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    phone_number: str | None = None
    min_score: float = Field(default=0.65, ge=0, le=1)


class AlertPreviewResponse(BaseModel):
    alerts: list[Alert]
    sms_enabled: bool
    delivery_mode: str
