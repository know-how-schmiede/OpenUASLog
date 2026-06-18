from datetime import date

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models import Drone, Flight, User

router = APIRouter(prefix="/reports", tags=["reports"])


class DashboardReport(BaseModel):
    flights_total: int
    flights_this_month: int
    total_flight_minutes: int
    active_drones: int
    planned_flights: int


@router.get("/dashboard", response_model=DashboardReport)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardReport:
    today = date.today()
    month_start = today.replace(day=1)
    flight_filter = [] if current_user.role == "admin" else [Flight.pilot_user_id == current_user.id]
    drone_filter = [] if current_user.role == "admin" else [Drone.owner_user_id == current_user.id]

    def flight_scalar(expression: object, *extra: object) -> int:
        value = db.scalar(select(expression).where(*flight_filter, *extra))
        return int(value or 0)

    return DashboardReport(
        flights_total=flight_scalar(func.count(Flight.id)),
        flights_this_month=flight_scalar(func.count(Flight.id), Flight.date >= month_start),
        total_flight_minutes=flight_scalar(func.sum(Flight.duration_minutes)),
        active_drones=int(
            db.scalar(
                select(func.count(Drone.id)).where(
                    *drone_filter,
                    Drone.status == "active",
                )
            )
            or 0
        ),
        planned_flights=flight_scalar(func.count(Flight.id), Flight.status == "planned"),
    )


@router.get("/flight-hours")
def flight_hours(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, float | int]:
    statement = select(func.sum(Flight.duration_minutes))
    if current_user.role != "admin":
        statement = statement.where(Flight.pilot_user_id == current_user.id)
    minutes = int(db.scalar(statement) or 0)
    return {"minutes": minutes, "hours": round(minutes / 60, 2)}
