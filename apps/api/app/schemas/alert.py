from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from app.schemas.common import HazardType, SeverityLevel
from app.schemas.location import Location


class AlertChannel(StrEnum):
    sms = "sms"
    email = "email"
    push = "push"
    webhook = "webhook"
    dashboard = "dashboard"


class AlertStatus(StrEnum):
    draft = "draft"
    queued = "queued"
    sent = "sent"
    failed = "failed"
    cancelled = "cancelled"


class AlertRecipient(BaseModel):
    user_id: str | None = None
    phone_number: str | None = None
    email: str | None = None
    location: Location | None = None


class AlertMessage(BaseModel):
    title: str
    body: str
    language: str = "en"
    official_source_url: str | None = None
    recommended_action: str | None = None


class Alert(BaseModel):
    id: str | None = None
    hazard_type: HazardType
    severity: SeverityLevel
    status: AlertStatus = AlertStatus.draft
    channels: list[AlertChannel]
    recipients: list[AlertRecipient]
    message: AlertMessage
    risk_score_id: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    scheduled_for: datetime | None = None
    sent_at: datetime | None = None
