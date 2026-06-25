# Disaster Alert Management

AI-assisted disaster monitoring and alerting platform.

## Goal

Build a service that can run on devices, edge servers, or cloud servers to continuously monitor disaster-related signals, analyze sensor and public data, predict risks, and alert users.

## Core Capabilities

- Monitor climate, weather, seismic, ocean, and terrain risk signals.
- Analyze historical and live public datasets where free access is available.
- Predict disaster risk for events such as floods, heatwaves, snowfall, landslides, storms, earthquakes, and ocean-related hazards.
- Provide a natural-language travel safety bot.
- Send alerts through SMS or other notification channels.

## Current Status

Task 1 scaffold only. This branch should be used as the initial `master` / `main` baseline.

## Planned Components

- `apps/api` - backend API service.
- `apps/web` - web dashboard.
- `apps/bot` - natural-language assistant service.
- `services/ingestion` - data ingestion workers.
- `services/ml` - analytics and ML prediction services.
- `services/alerting` - SMS and notification service.
- `packages/shared` - shared schemas, types, and utilities.
- `docs` - planning, architecture, API, and task documents.

## Quick Start

Implementation will be added incrementally through separate pull requests.

For now, copy `.env.example` to `.env` when starting local development.

## Safety Note

This project can support disaster-risk awareness, but it must not claim guaranteed prediction or replace official government alerts. Every alert should cite data sources, confidence, timestamp, and recommended official resources.
