from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Drone(Base):
    __tablename__ = "drones"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    drone_type_id: Mapped[int] = mapped_column(ForeignKey("drone_types.id"), index=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    serial_number: Mapped[str | None] = mapped_column(String(160))
    registration_mark: Mapped[str | None] = mapped_column(String(100))
    inventory_number: Mapped[str | None] = mapped_column(String(100))
    sticker_label: Mapped[str | None] = mapped_column(String(160))
    design_notes: Mapped[str | None] = mapped_column(Text)
    firmware_version: Mapped[str | None] = mapped_column(String(100))
    purchase_date: Mapped[date | None] = mapped_column(Date)
    insurance_info: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="active", index=True)
    notes: Mapped[str | None] = mapped_column(Text)

    custom_manufacturer: Mapped[str | None] = mapped_column(String(120))
    custom_model: Mapped[str | None] = mapped_column(String(120))
    custom_variant: Mapped[str | None] = mapped_column(String(120))
    custom_category: Mapped[str | None] = mapped_column(String(80))
    custom_drone_class: Mapped[str | None] = mapped_column(String(40))
    custom_weight_g: Mapped[int | None] = mapped_column(Integer)
    custom_max_flight_time_min: Mapped[int | None] = mapped_column(Integer)
    custom_max_speed_kmh: Mapped[float | None] = mapped_column(Float)
    custom_battery_type: Mapped[str | None] = mapped_column(String(160))
    custom_camera_info: Mapped[str | None] = mapped_column(Text)
    custom_sensor_info: Mapped[str | None] = mapped_column(Text)
    custom_remote_controller: Mapped[str | None] = mapped_column(String(160))

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    owner = relationship("User", back_populates="drones", foreign_keys=[owner_user_id])
    drone_type = relationship("DroneType", back_populates="drones")
    flights = relationship("Flight", back_populates="drone")
