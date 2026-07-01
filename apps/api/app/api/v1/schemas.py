from datetime import UTC, datetime, timedelta

from fastapi import APIRouter

from app.schemas.alert import Alert, AlertChannel, AlertMessage, AlertRecipient
from app.schemas.common import ConfidenceLevel, HazardType, SeverityLevel, SourceMetadata
from app.schemas.forecast import Forecast, ForecastPeriod
from app.schemas.location import Coordinates, Location
from app.schemas.normalized import NormalizedDisasterRecord
from app.schemas.observation import Observation, WeatherMetrics
from app.schemas.risk import Hazard, RiskScore
from app.schemas.travel import TravelPlan, TravelRiskAssessment, VehicleType

router = APIRouter(prefix="/schemas", tags=["schemas"])


@router.get("/metadata")
def schema_metadata() -> dict[str, list[str]]:
    return {
        "core_schemas": [
            "Location",
            "Observation",
            "Forecast",
            "Hazard",
            "RiskScore",
            "Alert",
            "TravelPlan",
            "TravelRiskAssessment",
            "NormalizedDisasterRecord",
        ],
        "hazard_types": [hazard.value for hazard in HazardType],
        "severity_levels": [severity.value for severity in SeverityLevel],
        "confidence_levels": [confidence.value for confidence in ConfidenceLevel],
        "vehicle_types": [vehicle.value for vehicle in VehicleType],
    }


@router.get("/example", response_model=NormalizedDisasterRecord)
def schema_example() -> NormalizedDisasterRecord:
    now = datetime.now(UTC)
    location = Location(
        id="loc-delhi",
        name="Delhi",
        coordinates=Coordinates(latitude=28.6139, longitude=77.2090, elevation_meters=216),
        country="India",
        region="Delhi",
        timezone="Asia/Kolkata",
    )
    source = SourceMetadata(
        source_name="example_source",
        source_url="https://example.com/source",
        collected_at=now,
        quality_score=0.8,
    )
    observation = Observation(
        id="obs-example-1",
        observed_at=now,
        location=location,
        source=source,
        weather=WeatherMetrics(
            temperature_celsius=42.0,
            humidity_percent=28,
            precipitation_mm=0,
            wind_speed_kph=18,
        ),
    )
    forecast = Forecast(
        id="forecast-example-1",
        issued_at=now,
        location=location,
        source=source,
        periods=[
            ForecastPeriod(
                starts_at=now,
                ends_at=now + timedelta(hours=24),
                weather=WeatherMetrics(temperature_celsius=43.0, humidity_percent=25),
                probability_percent=70,
            )
        ],
    )
    hazard = Hazard(
        id="hazard-example-1",
        hazard_type=HazardType.heatwave,
        severity=SeverityLevel.high,
        title="Possible heatwave conditions",
        description="High temperature forecast indicates heat stress risk.",
        location=location,
        starts_at=now,
        ends_at=now + timedelta(days=1),
        source=source,
        indicators={"temperature_celsius": 43.0},
    )
    risk_score = RiskScore(
        id="risk-example-1",
        hazard_type=HazardType.heatwave,
        location=location,
        score=0.76,
        severity=SeverityLevel.high,
        confidence=ConfidenceLevel.medium,
        calculated_at=now,
        model_name="rule_based_mvp",
        model_version="0.1.0",
        explanation="Temperature exceeds configured heat-risk threshold.",
        contributing_factors=["high_temperature", "low_humidity"],
        source_observation_ids=["obs-example-1"],
    )
    alert = Alert(
        id="alert-example-1",
        hazard_type=HazardType.heatwave,
        severity=SeverityLevel.high,
        channels=[AlertChannel.dashboard],
        recipients=[AlertRecipient(location=location)],
        message=AlertMessage(
            title="Heatwave risk detected",
            body="Avoid outdoor exposure during peak afternoon hours.",
            recommended_action="Stay hydrated and follow official local advisories.",
        ),
        risk_score_id="risk-example-1",
        created_at=now,
    )
    travel_plan = TravelPlan(
        id="travel-example-1",
        origin=location,
        destination=location,
        starts_at=now + timedelta(days=1),
        vehicle_type=VehicleType.car,
        traveler_notes="Example same-city trip.",
    )
    travel_assessment = TravelRiskAssessment(
        travel_plan=travel_plan,
        overall_risk="moderate",
        route_risk_scores=[risk_score],
        summary="Route has potential heat-related risk.",
        recommendations=["Carry water", "Avoid travel during peak heat"],
    )
    return NormalizedDisasterRecord(
        observations=[observation],
        forecasts=[forecast],
        hazards=[hazard],
        risk_scores=[risk_score],
        alerts=[alert],
        travel_plans=[travel_plan],
        travel_assessments=[travel_assessment],
    )
