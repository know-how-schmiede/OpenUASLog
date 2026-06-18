import csv
import io

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models import Flight, User

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/flights.csv")
def export_flights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:
    statement = (
        select(Flight)
        .options(joinedload(Flight.drone), joinedload(Flight.pilot))
        .order_by(Flight.date, Flight.start_time)
    )
    if current_user.role != "admin":
        statement = statement.where(Flight.pilot_user_id == current_user.id)
    flights = db.scalars(statement).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "Datum",
            "Startzeit",
            "Endzeit",
            "Dauer (Minuten)",
            "Pilot",
            "Drohne",
            "Ort",
            "Flugart",
            "Status",
            "Zweck",
            "Vorkommnisse",
            "Notizen",
        ]
    )
    for flight in flights:
        writer.writerow(
            [
                flight.date.isoformat(),
                flight.start_time.isoformat(timespec="minutes"),
                flight.end_time.isoformat(timespec="minutes") if flight.end_time else "",
                flight.duration_minutes,
                flight.pilot.full_name,
                flight.drone.name,
                flight.location_name,
                flight.flight_type,
                flight.status,
                flight.purpose or "",
                flight.incidents or "",
                flight.notes or "",
            ]
        )
    content = "\ufeff" + output.getvalue()
    return StreamingResponse(
        iter([content]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="openuaslog-flights.csv"'},
    )
