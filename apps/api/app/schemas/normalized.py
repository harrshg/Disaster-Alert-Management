from pydantic import BaseModel, Field

from app.schemas.alert import Alert
from app.schemas.forecast import Forecast
from app.schemas.observation import Observation
from app.schemas.risk import Hazard, RiskScore
from app.schemas.travel import TravelPlan, TravelRiskAssessment


class NormalizedDisasterRecord(BaseModel):
    observations: list[Observation] = Field(default_factory=list)
    forecasts: list[Forecast] = Field(default_factory=list)
    hazards: list[Hazard] = Field(default_factory=list)
    risk_scores: list[RiskScore] = Field(default_factory=list)
    alerts: list[Alert] = Field(default_factory=list)
    travel_plans: list[TravelPlan] = Field(default_factory=list)
    travel_assessments: list[TravelRiskAssessment] = Field(default_factory=list)
