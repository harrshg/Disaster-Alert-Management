# Data Source Connectors

Task 3 adds API connector endpoints for public disaster-monitoring data sources.

## Connector Status

```text
GET /api/v1/data-sources/status
```

Returns configured connector status and whether an API key is required.

## Open-Meteo Forecast

```text
GET /api/v1/data-sources/open-meteo/forecast?latitude=28.6139&longitude=77.2090&forecast_days=3
```

Purpose:

- Temperature.
- Humidity.
- Rain and precipitation probability.
- Snowfall.
- Wind speed.
- Weather codes.

API key required: No.

## USGS Earthquakes

```text
GET /api/v1/data-sources/usgs/earthquakes?latitude=28.6139&longitude=77.2090&radius_km=500&min_magnitude=2.5&limit=50
```

Purpose:

- Recent seismic events.
- Magnitude.
- Event time.
- Location geometry.

API key required: No.

## NASA POWER Daily Climate

```text
GET /api/v1/data-sources/nasa-power/climate/daily?latitude=28.6139&longitude=77.2090&start=20240101&end=20240107
```

Purpose:

- Historical temperature.
- Corrected precipitation.
- Relative humidity.
- Wind speed.

API key required: No.

## OpenStreetMap Nominatim Geocoding

```text
GET /api/v1/data-sources/openstreetmap/geocode?query=Delhi&limit=5
```

```text
GET /api/v1/data-sources/openstreetmap/reverse?latitude=28.6139&longitude=77.2090
```

Purpose:

- Convert place names to coordinates.
- Convert coordinates to readable locations.

API key required: No.

## Current Scope

These connectors fetch raw source data and return metadata with the request URL and parameters. Normalized schemas and storage should be added in Task 4 and Task 5.
