# Shared Data Schemas

Task 4 defines normalized disaster-management schemas used by ingestion, analytics, ML, alerting, dashboard, and bot services.

## Core Schemas

- `Location` - named place with coordinates and optional administrative metadata.
- `Observation` - timestamped raw or normalized sensor/public-source reading.
- `Forecast` - future weather or hazard-related forecast periods.
- `Hazard` - detected or predicted hazard event.
- `RiskScore` - normalized risk score between 0 and 1 with severity, confidence, and explanation.
- `Alert` - alert message, recipients, channels, status, and linked risk score.
- `TravelPlan` - origin, destination, waypoints, timing, and vehicle type.
- `TravelRiskAssessment` - route-specific risk summary and recommendations.
- `NormalizedDisasterRecord` - aggregate container for normalized records.

## Enums

### Hazard Types

- earthquake
- flood
- heatwave
- heavy_rain
- landslide
- snowfall
- storm
- wildfire
- coastal
- unknown

### Severity Levels

- low
- moderate
- high
- severe
- critical

### Confidence Levels

- low
- medium
- high

## API Endpoints

```text
GET /api/v1/schemas/metadata
```

Returns schema names and enum values.

```text
GET /api/v1/schemas/example
```

Returns a complete example `NormalizedDisasterRecord`.

## Design Notes

- All coordinates are validated against valid latitude and longitude ranges.
- Risk scores are normalized from `0` to `1`.
- Confidence and severity are separate fields.
- Source metadata is included so every derived record can be traced to its data source.
- Raw payloads are allowed on observations and forecasts for later auditability.
