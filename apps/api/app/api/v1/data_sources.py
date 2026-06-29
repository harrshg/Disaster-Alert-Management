from fastapi import APIRouter, Depends, Query

from app.connectors.nasa_power import get_climate_daily
from app.connectors.open_meteo import get_weather_forecast
from app.connectors.openstreetmap import geocode_place, reverse_geocode
from app.connectors.usgs import get_recent_earthquakes
from app.core.config import Settings, get_settings
from app.schemas.data_sources import ConnectorResponse, DataSourceStatus, DataSourceStatusResponse

router = APIRouter(prefix="/data-sources", tags=["data-sources"])


@router.get("/status", response_model=DataSourceStatusResponse)
def data_source_status(settings: Settings = Depends(get_settings)) -> DataSourceStatusResponse:
    return DataSourceStatusResponse(
        sources=[
            DataSourceStatus(
                name="Open-Meteo",
                type="weather_forecast",
                key_required=False,
                configured=True,
                base_url=settings.open_meteo_base_url,
            ),
            DataSourceStatus(
                name="USGS Earthquake",
                type="seismic_events",
                key_required=False,
                configured=True,
                base_url=settings.usgs_earthquake_base_url,
            ),
            DataSourceStatus(
                name="NASA POWER",
                type="climate_history",
                key_required=False,
                configured=True,
                base_url=settings.nasa_power_base_url,
            ),
            DataSourceStatus(
                name="OpenStreetMap Nominatim",
                type="geocoding",
                key_required=False,
                configured=True,
                base_url=settings.openstreetmap_nominatim_base_url,
            ),
            DataSourceStatus(
                name="OpenWeather",
                type="weather_alerts_optional",
                key_required=True,
                configured=bool(settings.openweather_api_key),
                base_url="provider_configured_by_key",
            ),
        ]
    )


@router.get("/open-meteo/forecast", response_model=ConnectorResponse)
async def open_meteo_forecast(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    forecast_days: int = Query(default=3, ge=1, le=16),
    settings: Settings = Depends(get_settings),
) -> ConnectorResponse:
    return await get_weather_forecast(settings, latitude, longitude, forecast_days)


@router.get("/usgs/earthquakes", response_model=ConnectorResponse)
async def usgs_earthquakes(
    latitude: float | None = Query(default=None, ge=-90, le=90),
    longitude: float | None = Query(default=None, ge=-180, le=180),
    radius_km: float = Query(default=500, gt=0, le=20001.6),
    min_magnitude: float = Query(default=2.5, ge=0, le=10),
    limit: int = Query(default=50, ge=1, le=500),
    settings: Settings = Depends(get_settings),
) -> ConnectorResponse:
    return await get_recent_earthquakes(settings, latitude, longitude, radius_km, min_magnitude, limit)


@router.get("/nasa-power/climate/daily", response_model=ConnectorResponse)
async def nasa_power_daily_climate(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    start: str = Query(pattern=r"^\d{8}$"),
    end: str = Query(pattern=r"^\d{8}$"),
    settings: Settings = Depends(get_settings),
) -> ConnectorResponse:
    return await get_climate_daily(settings, latitude, longitude, start, end)


@router.get("/openstreetmap/geocode", response_model=ConnectorResponse)
async def openstreetmap_geocode(
    query: str = Query(min_length=2, max_length=200),
    limit: int = Query(default=5, ge=1, le=20),
    settings: Settings = Depends(get_settings),
) -> ConnectorResponse:
    return await geocode_place(settings, query, limit)


@router.get("/openstreetmap/reverse", response_model=ConnectorResponse)
async def openstreetmap_reverse_geocode(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    settings: Settings = Depends(get_settings),
) -> ConnectorResponse:
    return await reverse_geocode(settings, latitude, longitude)
