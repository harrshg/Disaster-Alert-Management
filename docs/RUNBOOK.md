# Runbook

## What This MVP Does

The project runs as a FastAPI backend service. It can:

- Fetch live free weather forecast data from Open-Meteo.
- Fetch recent earthquake data from USGS.
- Geocode places using OpenStreetMap Nominatim.
- Produce rule-based MVP disaster risk scores.
- Assess natural-language travel plans.
- Generate alert previews for dashboard/SMS workflows.

## What Requires API Keys

No key is required for the default MVP endpoints.

SMS delivery requires Twilio credentials:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER`

Without Twilio credentials, alerts run in preview-only mode.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r apps/api/requirements.txt
copy .env.example .env
```

## Run

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir apps/api
```

## Open

```text
http://localhost:8000/docs
```

## Key Endpoints

### Health

```text
GET /health
GET /api/v1/status
```

### Raw Data Sources

```text
GET /api/v1/data-sources/status
GET /api/v1/data-sources/open-meteo/forecast?latitude=28.6139&longitude=77.2090&forecast_days=3
GET /api/v1/data-sources/usgs/earthquakes?latitude=28.6139&longitude=77.2090&radius_km=500&min_magnitude=2.5&limit=50
GET /api/v1/data-sources/openstreetmap/geocode?query=Delhi&limit=1
```

### Risk Assessment

```text
POST /api/v1/mvp/risk/assess
```

Example body:

```json
{
  "latitude": 28.6139,
  "longitude": 77.2090,
  "place_name": "Delhi",
  "forecast_days": 3
}
```

### Travel Bot

```text
POST /api/v1/mvp/travel/assess
```

Example body:

```json
{
  "message": "I am planning to travel from Delhi to Leh by car tomorrow"
}
```

### Alert Preview

```text
POST /api/v1/mvp/alerts/preview
```

Example body:

```json
{
  "latitude": 28.6139,
  "longitude": 77.2090,
  "phone_number": "+910000000000",
  "min_score": 0.65
}
```

## Accuracy Limitation

This MVP uses free public sources and rule-based scoring. It is useful for early warning support and demonstrations, but it is not a certified disaster prediction system and must not replace official advisories.
