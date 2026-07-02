import re
from datetime import UTC, datetime, timedelta

from app.core.config import Settings
from app.schemas.location import Coordinates, Location
from app.schemas.mvp import NaturalLanguageTravelRequest, RiskAssessmentRequest, TravelAssessmentResponse
from app.schemas.travel import TravelPlan, TravelRiskAssessment, VehicleType
from app.services.assessment import assess_location_risk, geocode_first


def extract_route(message: str) -> tuple[str | None, str | None]:
    patterns = [
        r"from\s+(.+?)\s+to\s+(.+?)(?:\s+on\s+|\s+via\s+|$)",
        r"travel\s+(.+?)\s+to\s+(.+?)(?:\s+on\s+|\s+via\s+|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, message, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip(), match.group(2).strip()
    return None, None


def extract_vehicle(message: str, fallback: VehicleType | None) -> VehicleType:
    lowered = message.lower()
    for vehicle in VehicleType:
        if vehicle.value in lowered:
            return vehicle
    return fallback or VehicleType.other


async def assess_travel(settings: Settings, request: NaturalLanguageTravelRequest) -> TravelAssessmentResponse:
    origin_text, destination_text = extract_route(request.message)
    warnings: list[str] = []
    if not origin_text or not destination_text:
        origin_text = "Delhi"
        destination_text = "Leh"
        warnings.append("Could not confidently parse route, so defaulted to Delhi to Leh example route.")

    origin_lat, origin_lon, origin_name = await geocode_first(settings, origin_text)
    destination_lat, destination_lon, destination_name = await geocode_first(settings, destination_text)
    destination_risk = await assess_location_risk(
        settings,
        RiskAssessmentRequest(
            latitude=destination_lat,
            longitude=destination_lon,
            place_name=destination_name,
            forecast_days=3,
        ),
    )
    vehicle = extract_vehicle(request.message, request.vehicle_type)
    starts_at = request.starts_at or datetime.now(UTC) + timedelta(days=1)
    origin_location = Location(
        name=origin_name,
        coordinates=Coordinates(latitude=origin_lat, longitude=origin_lon),
    )
    travel_plan = TravelPlan(
        origin=origin_location,
        destination=destination_risk.location,
        starts_at=starts_at,
        vehicle_type=vehicle,
        traveler_notes=request.message,
    )
    highest = max([score.score for score in destination_risk.risk_scores], default=0)
    if highest >= 0.75:
        overall = "high"
        summary = "Travel is not recommended without checking official advisories and local road/weather status."
    elif highest >= 0.45:
        overall = "moderate"
        summary = "Travel may be possible, but risk signals exist and conditions should be monitored."
    else:
        overall = "low"
        summary = "No major destination risk signal was detected from the checked public sources."
    assessment = TravelRiskAssessment(
        travel_plan=travel_plan,
        overall_risk=overall,
        route_risk_scores=destination_risk.risk_scores,
        summary=summary,
        recommendations=destination_risk.recommended_actions,
    )
    return TravelAssessmentResponse(
        parsed_origin=origin_text,
        parsed_destination=destination_text,
        assessment=assessment,
        warnings=warnings,
    )
