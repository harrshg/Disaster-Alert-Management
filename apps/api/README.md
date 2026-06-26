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
