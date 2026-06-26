from datetime import UTC, datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
    service: str
    environment: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ConfigSummaryResponse(BaseModel):
    app_name: str
    app_env: str
    api_port: int
    web_port: int
    database_configured: bool
    redis_configured: bool
    openweather_configured: bool
    twilio_configured: bool
    ai_configured: bool
    local_llm_configured: bool


class ServiceStatusResponse(BaseModel):
    api: str
    ingestion: str
    ml: str
    alerting: str
    bot: str
