from app.connectors.open_meteo import get_weather_forecast
from app.connectors.openstreetmap import geocode_place
from app.connectors.usgs import get_recent_earthquakes
from app.core.config import Settings
from app.schemas.mvp import RiskAssessmentRequest, RiskAssessmentResponse
from app.services.risk_engine import build_location, score_open_meteo_forecast, score_usgs_earthquakes


async def assess_location_risk(settings: Settings, request: RiskAssessmentRequest) -> RiskAssessmentResponse:
    location = build_location(request.latitude, request.longitude, request.place_name)
    risk_scores = []
    hazards = []
    data_sources = []

    forecast = await get_weather_forecast(settings, request.latitude, request.longitude, request.forecast_days)
    weather_scores, weather_hazards = score_open_meteo_forecast(location, forecast.data)
    risk_scores.extend(weather_scores)
    hazards.extend(weather_hazards)
    data_sources.append("Open-Meteo")

    earthquakes = await get_recent_earthquakes(settings, request.latitude, request.longitude, 500, 2.5, 50)
    earthquake_scores, earthquake_hazards = score_usgs_earthquakes(location, earthquakes.data)
    risk_scores.extend(earthquake_scores)
    hazards.extend(earthquake_hazards)
    data_sources.append("USGS Earthquake")

    highest = max([score.score for score in risk_scores], default=0)
    if highest >= 0.75:
        summary = "High disaster-related risk signals detected. Review hazards before making decisions."
    elif highest >= 0.45:
        summary = "Moderate risk signals detected. Continue monitoring official advisories."
    else:
        summary = "No major risk signals detected from the currently checked free public sources."

    return RiskAssessmentResponse(
        location=location,
        risk_scores=sorted(risk_scores, key=lambda item: item.score, reverse=True),
        hazards=hazards,
        summary=summary,
        recommended_actions=[
            "Check official government disaster-management advisories.",
            "Use this MVP as decision support, not as a guaranteed prediction system.",
            "Re-check closer to travel or operational time because conditions can change quickly.",
        ],
        data_sources=data_sources,
    )


async def geocode_first(settings: Settings, place: str) -> tuple[float, float, str]:
    response = await geocode_place(settings, place, 1)
    results = response.data.get("results", [])
    if not results:
        raise ValueError(f"Could not geocode place: {place}")
    first = results[0]
    return float(first["lat"]), float(first["lon"]), first.get("display_name", place)
