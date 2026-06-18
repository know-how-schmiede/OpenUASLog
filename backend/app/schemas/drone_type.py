from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DroneTypeBase(BaseModel):
    manufacturer: str = Field(min_length=1, max_length=120)
    model: str = Field(min_length=1, max_length=120)
    variant: str | None = None
    category: str | None = None
    drone_class: str | None = None
    weight_g: int | None = Field(default=None, ge=0)
    max_flight_time_min: int | None = Field(default=None, ge=0)
    max_speed_kmh: float | None = Field(default=None, ge=0)
    battery_type: str | None = None
    camera_info: str | None = None
    sensor_info: str | None = None
    remote_controller: str | None = None
    typical_use: str | None = None
    description: str | None = None
    image_url: str | None = None
    is_active: bool = True


class DroneTypeCreate(DroneTypeBase):
    pass


class DroneTypeUpdate(BaseModel):
    manufacturer: str | None = Field(default=None, min_length=1, max_length=120)
    model: str | None = Field(default=None, min_length=1, max_length=120)
    variant: str | None = None
    category: str | None = None
    drone_class: str | None = None
    weight_g: int | None = Field(default=None, ge=0)
    max_flight_time_min: int | None = Field(default=None, ge=0)
    max_speed_kmh: float | None = Field(default=None, ge=0)
    battery_type: str | None = None
    camera_info: str | None = None
    sensor_info: str | None = None
    remote_controller: str | None = None
    typical_use: str | None = None
    description: str | None = None
    image_url: str | None = None
    is_active: bool | None = None


class DroneTypeRead(DroneTypeBase):
    id: int
    created_by_user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
