from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = Field(default="development", alias="APP_ENV")
    app_name: str = Field(default="disaster-alert-management", alias="APP_NAME")
    api_port: int = Field(default=8000, alias="API_PORT")
    web_port: int = Field(default=3000, alias="WEB_PORT")

    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    redis_url: str | None = Field(default=None, alias="REDIS_URL")

    openweather_api_key: str | None = Field(default=None, alias="OPENWEATHER_API_KEY")
    nasa_power_base_url: str = Field(default="https://power.larc.nasa.gov/api", alias="NASA_POWER_BASE_URL")
    usgs_earthquake_base_url: str = Field(
        default="https://earthquake.usgs.gov/fdsnws/event/1",
        alias="USGS_EARTHQUAKE_BASE_URL",
    )
    open_meteo_base_url: str = Field(default="https://api.open-meteo.com/v1", alias="OPEN_METEO_BASE_URL")
    noaa_base_url: str = Field(default="https://www.ncei.noaa.gov/access/services/data/v1", alias="NOAA_BASE_URL")
    openstreetmap_nominatim_base_url: str = Field(
        default="https://nominatim.openstreetmap.org",
        alias="OPENSTREETMAP_NOMINATIM_BASE_URL",
    )

    twilio_account_sid: str | None = Field(default=None, alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str | None = Field(default=None, alias="TWILIO_AUTH_TOKEN")
    twilio_from_number: str | None = Field(default=None, alias="TWILIO_FROM_NUMBER")

    ai_provider: str | None = Field(default=None, alias="AI_PROVIDER")
    ai_api_key: str | None = Field(default=None, alias="AI_API_KEY")
    local_llm_base_url: str | None = Field(default=None, alias="LOCAL_LLM_BASE_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
