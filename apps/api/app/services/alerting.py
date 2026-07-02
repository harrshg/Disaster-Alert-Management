from datetime import UTC, datetime

from app.core.config import Settings
from app.schemas.alert import Alert, AlertChannel, AlertMessage, AlertRecipient, AlertStatus
from app.schemas.mvp import AlertPreviewRequest, AlertPreviewResponse, RiskAssessmentRequest
from app.services.assessment import assess_location_risk


async def build_alert_preview(settings: Settings, request: AlertPreviewRequest) -> AlertPreviewResponse:
    assessment = await assess_location_risk(
        settings,
        RiskAssessmentRequest(
            latitude=request.latitude,
            longitude=request.longitude,
            forecast_days=3,
        ),
    )
    sms_enabled = bool(settings.twilio_account_sid and settings.twilio_auth_token and settings.twilio_from_number)
    alerts: list[Alert] = []
    for risk in assessment.risk_scores:
        if risk.score < request.min_score:
            continue
        channels = [AlertChannel.dashboard]
        if request.phone_number:
            channels.append(AlertChannel.sms)
        alerts.append(
            Alert(
                hazard_type=risk.hazard_type,
                severity=risk.severity,
                status=AlertStatus.queued if sms_enabled and request.phone_number else AlertStatus.draft,
                channels=channels,
                recipients=[AlertRecipient(phone_number=request.phone_number, location=assessment.location)],
                message=AlertMessage(
                    title=f"{risk.hazard_type.value.replace('_', ' ').title()} risk alert",
                    body=risk.explanation,
                    recommended_action="Check official advisories and avoid unnecessary exposure to the affected area.",
                ),
                risk_score_id=risk.id,
                created_at=datetime.now(UTC),
            )
        )
    return AlertPreviewResponse(
        alerts=alerts,
        sms_enabled=sms_enabled,
        delivery_mode="twilio_ready" if sms_enabled else "preview_only_no_sms_key_configured",
    )
