from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class DroneBase(BaseModel):
    drone_type_id: int
    name: str = Field(min_length=1, max_length=160)
    serial_number: str | None = None
    registration_mark: str | None = None
    inventory_number: str | None = None
    sticker_label: str | None = None
    design_notes: str | None = None
    firmware_version: str | None = None
    purchase_date: date | None = None
    insurance_info: str | None = None
    status: str = "active"
    notes: str | None = None
    custom_manufacturer: str | None = None
    custom_model: str | None = None
    custom_variant: str | None = None
    custom_category: str | None = None
    custom_drone_class: str | None = None
    custom_weight_g: int | None = Field(default=None, ge=0)
    custom_max_flight_time_min: int | None = Field(default=None, ge=0)
    custom_max_speed_kmh: float | None = Field(default=None, ge=0)
    custom_battery_type: str | None = None
    custom_camera_info: str | None = None
    custom_sensor_info: str | None = None
    custom_remote_controller: str | None = None


class DroneCreate(DroneBase):
    owner_user_id: int | None = None


class DroneUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    serial_number: str | None = None
    registration_mark: str | None = None
    inventory_number: str | None = None
    sticker_label: str | None = None
    design_notes: str | None = None
    firmware_version: str | None = None
    purchase_date: date | None = None
    insurance_info: str | None = None
    status: str | None = None
    notes: str | None = None
    custom_manufacturer: str | None = None
    custom_model: str | None = None
    custom_variant: str | None = None
    custom_category: str | None = None
    custom_drone_class: str | None = None
    custom_weight_g: int | None = Field(default=None, ge=0)
    custom_max_flight_time_min: int | None = Field(default=None, ge=0)
    custom_max_speed_kmh: float | None = Field(default=None, ge=0)
    custom_battery_type: str | None = None
    custom_camera_info: str | None = None
    custom_sensor_info: str | None = None
    custom_remote_controller: str | None = None


class DroneRead(DroneBase):
    id: int
    owner_user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResolvedValue(BaseModel):
    value: Any | None
    source: Literal["template", "custom", "unset"]


class ResolvedDrone(BaseModel):
    id: int
    owner_user_id: int
    drone_type_id: int
    name: str
    status: str
    manufacturer: ResolvedValue
    model: ResolvedValue
    variant: ResolvedValue
    category: ResolvedValue
    drone_class: ResolvedValue
    weight_g: ResolvedValue
    max_flight_time_min: ResolvedValue
    max_speed_kmh: ResolvedValue
    battery_type: ResolvedValue
    camera_info: ResolvedValue
    sensor_info: ResolvedValue
    remote_controller: ResolvedValue
