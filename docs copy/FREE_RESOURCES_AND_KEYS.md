# Free Resources and API Keys

## Can Be Used Without API Key

### Open-Meteo

- Purpose: Weather forecasts, historical weather, climate data.
- Cost: Free for non-commercial / fair-use workloads.
- Key required: No.
- URL: https://open-meteo.com/

### USGS Earthquake API

- Purpose: Earthquake event monitoring.
- Cost: Free.
- Key required: No.
- URL: https://earthquake.usgs.gov/fdsnws/event/1/

### NASA POWER

- Purpose: Climate, solar, temperature, humidity, wind, precipitation indicators.
- Cost: Free.
- Key required: No.
- URL: https://power.larc.nasa.gov/

### OpenStreetMap Nominatim

- Purpose: Geocoding places and route points.
- Cost: Free with usage policy limits.
- Key required: No.
- URL: https://nominatim.openstreetmap.org/

## May Need Free Account / API Key

### OpenWeather

- Purpose: Weather forecast and alerts where available.
- Cost: Has free tier.
- Key required: Yes.
- Environment variable: `OPENWEATHER_API_KEY`.

### Twilio SMS

- Purpose: SMS alert delivery.
- Cost: Trial credits may be free, but production SMS is usually paid.
- Key required: Yes.
- Environment variables: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`.

## SMS Free-Service Reality

Reliable SMS is rarely permanently free. Free options usually have limits, trial credits, ads, region restrictions, or require verified numbers. For production-grade disaster alerts, plan for a paid SMS provider or integrate official channels later.

## AI / LLM Options

### Local LLM

- Purpose: Travel-risk bot and explanation generation.
- Cost: Free if running locally.
- Key required: No.
- Options: Ollama, llama.cpp, local Hugging Face models.

### Hosted AI API

- Purpose: Better natural-language understanding.
- Cost: Usually paid or limited free tier.
- Key required: Yes.
- Environment variable: `AI_API_KEY`.
