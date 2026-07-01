from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    elevation_meters: float | None = None


class Location(BaseModel):
    id: str | None = None
    name: str | None = None
    coordinates: Coordinates
    country: str | None = None
    region: str | None = None
    district: str | None = None
    timezone: str | None = None
    geohash: str | None = None
