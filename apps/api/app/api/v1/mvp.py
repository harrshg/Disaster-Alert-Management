from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import Settings, get_settings
from app.schemas.mvp import (
    AlertPreviewRequest,
    AlertPreviewResponse,
    NaturalLanguageTravelRequest,
    RiskAssessmentRequest,
    RiskAssessmentResponse,
    TravelAssessmentResponse,
)
from app.services.alerting import build_alert_preview
from app.services.assessment import assess_location_risk
from app.services.travel_bot import assess_travel

router = APIRouter(prefix="/mvp", tags=["mvp"])


@router.post("/risk/assess", response_model=RiskAssessmentResponse)
async def assess_risk(
    request: RiskAssessmentRequest,
    settings: Settings = Depends(get_settings),
) -> RiskAssessmentResponse:
    return await assess_location_risk(settings, request)


@router.post("/travel/assess", response_model=TravelAssessmentResponse)
async def assess_travel_plan(
    request: NaturalLanguageTravelRequest,
    settings: Settings = Depends(get_settings),
) -> TravelAssessmentResponse:
    try:
        return await assess_travel(settings, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.post("/alerts/preview", response_model=AlertPreviewResponse)
async def preview_alerts(
    request: AlertPreviewRequest,
    settings: Settings = Depends(get_settings),
) -> AlertPreviewResponse:
    return await build_alert_preview(settings, request)
