from __future__ import annotations

from datetime import date as DateType
from datetime import datetime
from datetime import time as TimeType

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FlightBase(BaseModel):
    drone_id: int
    observer_user_id: int | None = None
    date: DateType
    start_time: TimeType
    end_time: TimeType | None = None
    location_name: str = Field(min_length=1, max_length=200)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    flight_type: str = Field(min_length=1, max_length=80)
    purpose: str | None = None
    weather: str | None = None
    wind: str | None = None
    temperature_c: float | None = None
    incidents: str | None = None
    notes: str | None = None
    status: str = "planned"

    @model_validator(mode="after")
    def validate_times(self) -> "FlightBase":
        if self.end_time and self.end_time < self.start_time:
            raise ValueError("Die Endzeit darf nicht vor der Startzeit liegen.")
        return self


class FlightCreate(FlightBase):
    pilot_user_id: int | None = None


class FlightUpdate(BaseModel):
    drone_id: int | None = None
    observer_user_id: int | None = None
    date: DateType | None = None
    start_time: TimeType | None = None
    end_time: TimeType | None = None
    location_name: str | None = Field(default=None, min_length=1, max_length=200)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    flight_type: str | None = Field(default=None, min_length=1, max_length=80)
    purpose: str | None = None
    weather: str | None = None
    wind: str | None = None
    temperature_c: float | None = None
    incidents: str | None = None
    notes: str | None = None
    status: str | None = None


class FlightRead(FlightBase):
    id: int
    pilot_user_id: int
    duration_minutes: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
