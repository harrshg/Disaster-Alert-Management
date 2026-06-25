# Architecture

## High-Level Flow

1. Data sources provide weather, climate, seismic, ocean, terrain, and user travel information.
2. Ingestion workers normalize data into shared schemas.
3. Analytics and ML services calculate hazard-specific risk scores.
4. API service exposes risk, forecast, alert, and travel-assistant endpoints.
5. Alerting service sends notifications when risk thresholds are crossed.
6. Web dashboard and bot consume API results.

## Services

### API Service

Responsible for authenticated access, REST endpoints, request validation, and coordination between services.

### Ingestion Service

Responsible for polling public APIs, validating sensor feeds, storing observations, and tracking source quality.

### ML Service

Responsible for feature engineering, model inference, risk scoring, confidence calculation, and explainability metadata.

### Alerting Service

Responsible for alert rules, deduplication, escalation, SMS delivery, and audit logs.

### Bot Service

Responsible for natural-language travel-risk queries such as route, date, vehicle, and destination analysis.

## Data Categories

- Weather forecasts.
- Historical climate.
- Earthquake events.
- Rainfall and flood indicators.
- Heatwave indicators.
- Snowfall indicators.
- Landslide risk indicators.
- Ocean and coastal signals.
- User route and travel plans.

## Accuracy and Safety Requirements

- Every prediction must include confidence and data timestamp.
- Alerts must avoid unsupported certainty.
- Official sources should be linked wherever possible.
- High-risk warnings should recommend checking official disaster management authorities.
- Model outputs should be logged for review and improvement.
