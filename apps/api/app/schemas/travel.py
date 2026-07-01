from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from app.schemas.location import Location
from app.schemas.risk import RiskScore


class VehicleType(StrEnum):
    car = "car"
    bike = "bike"
    bus = "bus"
    train = "train"
    flight = "flight"
    walking = "walking"
    other = "other"


class TravelPlan(BaseModel):
    id: str | None = None
    origin: Location
    destination: Location
    waypoints: list[Location] = Field(default_factory=list)
    starts_at: datetime
    ends_at: datetime | None = None
    vehicle_type: VehicleType
    traveler_notes: str | None = None


class TravelRiskAssessment(BaseModel):
    travel_plan: TravelPlan
    overall_risk: str
    route_risk_scores: list[RiskScore]
    summary: str
    recommendations: list[str] = Field(default_factory=list)
