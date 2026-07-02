# API Service

Backend API foundation for Disaster Alert Management.

## Stack

- FastAPI
- Uvicorn
- Pydantic Settings

## Setup

Create a virtual environment from the repository root or inside `apps/api`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r apps/api/requirements.txt
```

Copy the environment template from the repository root.

```powershell
copy .env.example .env
```

## Run

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir apps/api
```

## Endpoints

- `GET /` - service metadata.
- `GET /health` - basic health check.
- `GET /api/v1/health` - versioned health check.
- `GET /api/v1/config` - safe runtime configuration summary.
- `GET /api/v1/status` - placeholder service readiness status.
- `GET /api/v1/data-sources/status` - data source connector status.
- `GET /api/v1/data-sources/open-meteo/forecast` - weather forecast from Open-Meteo.
- `GET /api/v1/data-sources/usgs/earthquakes` - recent earthquake events from USGS.
- `GET /api/v1/data-sources/nasa-power/climate/daily` - daily climate history from NASA POWER.
- `GET /api/v1/data-sources/openstreetmap/geocode` - place geocoding from OpenStreetMap Nominatim.
- `GET /api/v1/data-sources/openstreetmap/reverse` - reverse geocoding from OpenStreetMap Nominatim.
- `GET /api/v1/schemas/metadata` - normalized schema names and enum values.
- `GET /api/v1/schemas/example` - complete normalized disaster record example.
- `POST /api/v1/mvp/risk/assess` - run live public-data risk assessment for a location.
- `POST /api/v1/mvp/travel/assess` - assess a natural-language travel plan.
- `POST /api/v1/mvp/alerts/preview` - generate alert previews and SMS-readiness status.
