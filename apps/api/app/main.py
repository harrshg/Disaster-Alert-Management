from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import router as v1_router
from app.core.config import Settings, get_settings
from app.schemas.health import HealthResponse

settings = get_settings()

app = FastAPI(
    title="Disaster Alert Management API",
    description="Backend API foundation for disaster monitoring, risk analysis, and alerting.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.is_development else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "status": "ready",
        "docs": "/docs",
        "health": "/health",
        "api_v1": "/api/v1",
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        environment=settings.app_env,
    )
