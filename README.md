# Disaster Alert Management

AI-assisted disaster monitoring, risk assessment, travel safety, and alert-preview platform.

## Goal

Build a service that can run on devices, edge servers, or cloud servers to continuously monitor disaster-related signals, analyze sensor and public data, predict risks, and alert users.

## Core Capabilities

- Monitor climate, weather, seismic, ocean, and terrain risk signals.
- Analyze historical and live public datasets where free access is available.
- Predict disaster risk for events such as floods, heatwaves, snowfall, landslides, storms, earthquakes, and ocean-related hazards.
- Provide a natural-language travel safety bot.
- Send alerts through SMS or other notification channels.

## Current Status

Runnable MVP is implemented. The backend can fetch free public disaster-related data, normalize schemas, calculate rule-based risk scores, assess natural-language travel plans, and create alert previews.

## Implemented Components

- `apps/api` - FastAPI backend service.
- `apps/api/app/connectors` - Open-Meteo, USGS, NASA POWER, and OpenStreetMap connectors.
- `apps/api/app/schemas` - normalized disaster data schemas.
- `apps/api/app/services` - risk assessment, travel bot, and alert-preview services.
- `docs` - architecture, connector, schema, and runbook documentation.

## Quick Start

Copy `.env.example` to `.env` when starting local development.

```powershell
copy .env.example .env
```

Install and run the API service.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r apps/api/requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir apps/api
```

Open API docs at `http://localhost:8000/docs`.

See `docs/RUNBOOK.md` for endpoint examples.

## Main MVP Endpoints

- `GET /api/v1/status`
- `GET /api/v1/data-sources/status`
- `POST /api/v1/mvp/risk/assess`
- `POST /api/v1/mvp/travel/assess`
- `POST /api/v1/mvp/alerts/preview`

## Safety Note

This project can support disaster-risk awareness, but it must not claim guaranteed prediction or replace official government alerts. Every alert should cite data sources, confidence, timestamp, and recommended official resources.
