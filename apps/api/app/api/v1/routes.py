from fastapi import APIRouter, Depends

from app.api.v1.data_sources import router as data_sources_router
from app.core.config import Settings, get_settings
from app.schemas.health import ConfigSummaryResponse, HealthResponse, ServiceStatusResponse

router = APIRouter(prefix="/api/v1")
router.include_router(data_sources_router)


@router.get("/health", response_model=HealthResponse, tags=["health"])
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        environment=settings.app_env,
    )


@router.get("/config", response_model=ConfigSummaryResponse, tags=["config"])
def config_summary(settings: Settings = Depends(get_settings)) -> ConfigSummaryResponse:
    return ConfigSummaryResponse(
        app_name=settings.app_name,
        app_env=settings.app_env,
        api_port=settings.api_port,
        web_port=settings.web_port,
        database_configured=bool(settings.database_url),
        redis_configured=bool(settings.redis_url),
        openweather_configured=bool(settings.openweather_api_key),
        twilio_configured=bool(
            settings.twilio_account_sid
            and settings.twilio_auth_token
            and settings.twilio_from_number
        ),
        ai_configured=bool(settings.ai_provider and settings.ai_api_key),
        local_llm_configured=bool(settings.local_llm_base_url),
    )


@router.get("/status", response_model=ServiceStatusResponse, tags=["status"])
def service_status() -> ServiceStatusResponse:
    return ServiceStatusResponse(
        api="ready",
        ingestion="connectors_ready",
        ml="not_implemented",
        alerting="not_implemented",
        bot="not_implemented",
    )
