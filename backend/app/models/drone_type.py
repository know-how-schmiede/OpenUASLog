from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class DroneType(Base):
    __tablename__ = "drone_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    manufacturer: Mapped[str] = mapped_column(String(120), index=True)
    model: Mapped[str] = mapped_column(String(120), index=True)
    variant: Mapped[str | None] = mapped_column(String(120))
    category: Mapped[str | None] = mapped_column(String(80))
    drone_class: Mapped[str | None] = mapped_column(String(40))
    weight_g: Mapped[int | None] = mapped_column(Integer)
    max_flight_time_min: Mapped[int | None] = mapped_column(Integer)
    max_speed_kmh: Mapped[float | None] = mapped_column(Float)
    battery_type: Mapped[str | None] = mapped_column(String(160))
    camera_info: Mapped[str | None] = mapped_column(Text)
    sensor_info: Mapped[str | None] = mapped_column(Text)
    remote_controller: Mapped[str | None] = mapped_column(String(160))
    typical_use: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    drones = relationship("Drone", back_populates="drone_type")
