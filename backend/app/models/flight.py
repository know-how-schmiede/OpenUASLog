from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, Time, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Flight(Base):
    __tablename__ = "flights"

    id: Mapped[int] = mapped_column(primary_key=True)
    drone_id: Mapped[int] = mapped_column(ForeignKey("drones.id"), index=True)
    pilot_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    observer_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time | None] = mapped_column(Time)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=0)
    location_name: Mapped[str] = mapped_column(String(200))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    flight_type: Mapped[str] = mapped_column(String(80), index=True)
    purpose: Mapped[str | None] = mapped_column(Text)
    weather: Mapped[str | None] = mapped_column(String(160))
    wind: Mapped[str | None] = mapped_column(String(100))
    temperature_c: Mapped[float | None] = mapped_column(Float)
    incidents: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="planned", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    drone = relationship("Drone", back_populates="flights")
    pilot = relationship("User", back_populates="piloted_flights", foreign_keys=[pilot_user_id])
    observer = relationship("User", foreign_keys=[observer_user_id])
