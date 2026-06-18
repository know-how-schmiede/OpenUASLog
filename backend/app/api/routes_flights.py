from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models import Drone, Flight, User
from app.schemas.flight import FlightCreate, FlightRead, FlightUpdate
from app.services.flight_duration import calculate_duration_minutes

router = APIRouter(prefix="/flights", tags=["flights"])


def _get_visible_flight(db: Session, flight_id: int, user: User) -> Flight:
    flight = db.get(Flight, flight_id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flug nicht gefunden.")
    if user.role != "admin" and flight.pilot_user_id != user.id:
        raise HTTPException(status_code=403, detail="Keine Berechtigung für diesen Flug.")
    return flight


def _validate_drone_access(db: Session, drone_id: int, user: User) -> Drone:
    drone = db.get(Drone, drone_id)
    if not drone:
        raise HTTPException(status_code=422, detail="Drohne nicht gefunden.")
    if user.role != "admin" and drone.owner_user_id != user.id:
        raise HTTPException(status_code=403, detail="Keine Berechtigung für diese Drohne.")
    return drone


@router.get("", response_model=list[FlightRead])
def list_flights(
    date_from: date | None = None,
    date_to: date | None = None,
    drone_id: int | None = None,
    flight_status: str | None = None,
    flight_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Flight]:
    statement = select(Flight).order_by(Flight.date.desc(), Flight.start_time.desc())
    if current_user.role != "admin":
        statement = statement.where(Flight.pilot_user_id == current_user.id)
    if date_from:
        statement = statement.where(Flight.date >= date_from)
    if date_to:
        statement = statement.where(Flight.date <= date_to)
    if drone_id:
        statement = statement.where(Flight.drone_id == drone_id)
    if flight_status:
        statement = statement.where(Flight.status == flight_status)
    if flight_type:
        statement = statement.where(Flight.flight_type == flight_type)
    return list(db.scalars(statement))


@router.post("", response_model=FlightRead, status_code=status.HTTP_201_CREATED)
def create_flight(
    payload: FlightCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Flight:
    _validate_drone_access(db, payload.drone_id, current_user)
    pilot_user_id = (
        payload.pilot_user_id
        if current_user.role == "admin" and payload.pilot_user_id
        else current_user.id
    )
    pilot = db.get(User, pilot_user_id)
    if not pilot or pilot.role not in {"admin", "pilot"}:
        raise HTTPException(status_code=422, detail="Pilot nicht gefunden.")
    if payload.observer_user_id and not db.get(User, payload.observer_user_id):
        raise HTTPException(status_code=422, detail="Observer nicht gefunden.")
    flight = Flight(
        **payload.model_dump(exclude={"pilot_user_id"}),
        pilot_user_id=pilot_user_id,
        duration_minutes=calculate_duration_minutes(payload.start_time, payload.end_time),
    )
    db.add(flight)
    db.commit()
    db.refresh(flight)
    return flight


@router.get("/{flight_id}", response_model=FlightRead)
def get_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Flight:
    return _get_visible_flight(db, flight_id, current_user)


@router.patch("/{flight_id}", response_model=FlightRead)
def update_flight(
    flight_id: int,
    payload: FlightUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Flight:
    flight = _get_visible_flight(db, flight_id, current_user)
    values = payload.model_dump(exclude_unset=True)
    if "drone_id" in values:
        _validate_drone_access(db, values["drone_id"], current_user)
    for field, value in values.items():
        setattr(flight, field, value)
    if flight.end_time and flight.end_time < flight.start_time:
        raise HTTPException(status_code=422, detail="Endzeit liegt vor der Startzeit.")
    flight.duration_minutes = calculate_duration_minutes(flight.start_time, flight.end_time)
    db.commit()
    db.refresh(flight)
    return flight


@router.delete("/{flight_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    flight = _get_visible_flight(db, flight_id, current_user)
    db.delete(flight)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
