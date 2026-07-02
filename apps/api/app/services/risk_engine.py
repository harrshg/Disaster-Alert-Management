from datetime import UTC, datetime, timedelta
from typing import Any

from app.schemas.common import ConfidenceLevel, HazardType, SeverityLevel, SourceMetadata
from app.schemas.location import Coordinates, Location
from app.schemas.risk import Hazard, RiskScore


def severity_from_score(score: float) -> SeverityLevel:
    if score >= 0.9:
        return SeverityLevel.critical
    if score >= 0.75:
        return SeverityLevel.severe
    if score >= 0.6:
        return SeverityLevel.high
    if score >= 0.35:
        return SeverityLevel.moderate
    return SeverityLevel.low


def build_location(latitude: float, longitude: float, place_name: str | None = None) -> Location:
    return Location(
        name=place_name,
        coordinates=Coordinates(latitude=latitude, longitude=longitude),
    )


def score_open_meteo_forecast(location: Location, payload: dict[str, Any]) -> tuple[list[RiskScore], list[Hazard]]:
    now = datetime.now(UTC)
    daily = payload.get("daily", {})
    max_temperatures = daily.get("temperature_2m_max", []) or []
    rain_sums = daily.get("rain_sum", []) or []
    precipitation_sums = daily.get("precipitation_sum", []) or []
    snowfall_sums = daily.get("snowfall_sum", []) or []
    wind_speeds = daily.get("wind_speed_10m_max", []) or []
    times = daily.get("time", []) or []
    source = SourceMetadata(source_name="Open-Meteo", source_url="https://open-meteo.com/", collected_at=now, quality_score=0.85)
    scores: list[RiskScore] = []
    hazards: list[Hazard] = []

    def add_score(hazard_type: HazardType, score: float, explanation: str, factors: list[str], indicators: dict[str, Any]) -> None:
        severity = severity_from_score(score)
        risk = RiskScore(
            hazard_type=hazard_type,
            location=location,
            score=round(min(max(score, 0), 1), 2),
            severity=severity,
            confidence=ConfidenceLevel.medium,
            calculated_at=now,
            model_name="rule_based_mvp",
            model_version="0.1.0",
            explanation=explanation,
            contributing_factors=factors,
        )
        scores.append(risk)
        if score >= 0.6:
            hazards.append(
                Hazard(
                    hazard_type=hazard_type,
                    severity=severity,
                    title=f"{hazard_type.value.replace('_', ' ').title()} risk detected",
                    description=explanation,
                    location=location,
                    starts_at=now,
                    ends_at=now + timedelta(days=3),
                    source=source,
                    indicators=indicators,
                )
            )

    max_temp = max(max_temperatures) if max_temperatures else None
    max_rain = max([*rain_sums, *precipitation_sums]) if rain_sums or precipitation_sums else None
    max_snow = max(snowfall_sums) if snowfall_sums else None
    max_wind = max(wind_speeds) if wind_speeds else None

    if max_temp is not None:
        add_score(
            HazardType.heatwave,
            (max_temp - 32) / 15,
            f"Maximum forecast temperature is {max_temp}°C.",
            ["temperature_2m_max"],
            {"max_temperature_celsius": max_temp, "forecast_dates": times},
        )
    if max_rain is not None:
        add_score(
            HazardType.heavy_rain,
            max_rain / 100,
            f"Maximum forecast rainfall or precipitation is {max_rain} mm.",
            ["rain_sum", "precipitation_sum"],
            {"max_precipitation_mm": max_rain, "forecast_dates": times},
        )
        add_score(
            HazardType.flood,
            max_rain / 150,
            f"Flood risk estimated from forecast precipitation of {max_rain} mm.",
            ["precipitation_sum"],
            {"max_precipitation_mm": max_rain, "forecast_dates": times},
        )
        add_score(
            HazardType.landslide,
            max_rain / 130,
            f"Landslide risk estimated from heavy rainfall of {max_rain} mm.",
            ["rain_sum", "terrain_proxy_missing"],
            {"max_rain_mm": max_rain, "forecast_dates": times},
        )
    if max_snow is not None:
        add_score(
            HazardType.snowfall,
            max_snow / 50,
            f"Maximum forecast snowfall is {max_snow} cm.",
            ["snowfall_sum"],
            {"max_snowfall_cm": max_snow, "forecast_dates": times},
        )
    if max_wind is not None:
        add_score(
            HazardType.storm,
            max_wind / 100,
            f"Maximum forecast wind speed is {max_wind} km/h.",
            ["wind_speed_10m_max"],
            {"max_wind_speed_kph": max_wind, "forecast_dates": times},
        )

    return scores, hazards


def score_usgs_earthquakes(location: Location, payload: dict[str, Any]) -> tuple[list[RiskScore], list[Hazard]]:
    now = datetime.now(UTC)
    features = payload.get("features", []) or []
    source = SourceMetadata(source_name="USGS Earthquake", source_url="https://earthquake.usgs.gov/", collected_at=now, quality_score=0.9)
    scores: list[RiskScore] = []
    hazards: list[Hazard] = []
    max_magnitude = 0.0
    for feature in features:
        properties = feature.get("properties", {}) or {}
        magnitude = properties.get("mag") or 0
        max_magnitude = max(max_magnitude, float(magnitude))
    score = max_magnitude / 8 if max_magnitude else 0
    severity = severity_from_score(score)
    risk = RiskScore(
        hazard_type=HazardType.earthquake,
        location=location,
        score=round(min(score, 1), 2),
        severity=severity,
        confidence=ConfidenceLevel.high if features else ConfidenceLevel.medium,
        calculated_at=now,
        model_name="rule_based_mvp",
        model_version="0.1.0",
        explanation=f"USGS recent nearby maximum magnitude is {max_magnitude}.",
        contributing_factors=["recent_earthquake_magnitude", "nearby_event_count"],
    )
    scores.append(risk)
    if score >= 0.6:
        hazards.append(
            Hazard(
                hazard_type=HazardType.earthquake,
                severity=severity,
                title="Earthquake activity risk detected",
                description=risk.explanation,
                location=location,
                starts_at=now,
                ends_at=now + timedelta(days=1),
                source=source,
                indicators={"max_magnitude": max_magnitude, "event_count": len(features)},
            )
        )
    return scores, hazards
