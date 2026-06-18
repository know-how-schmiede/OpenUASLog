from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models import Drone, DroneType, User
from app.schemas.drone import DroneCreate, DroneRead, DroneUpdate, ResolvedDrone
from app.services.drone_value_resolver import resolve_drone

router = APIRouter(prefix="/drones", tags=["drones"])


def _get_visible_drone(db: Session, drone_id: int, user: User) -> Drone:
    drone = db.scalar(
        select(Drone)
        .options(joinedload(Drone.drone_type))
        .where(Drone.id == drone_id)
    )
    if not drone:
        raise HTTPException(status_code=404, detail="Drohne nicht gefunden.")
    if user.role != "admin" and drone.owner_user_id != user.id:
        raise HTTPException(status_code=403, detail="Keine Berechtigung für diese Drohne.")
    return drone


@router.get("", response_model=list[DroneRead])
def list_drones(
    status_filter: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Drone]:
    statement = select(Drone).order_by(Drone.name)
    if current_user.role != "admin":
        statement = statement.where(Drone.owner_user_id == current_user.id)
    if status_filter:
        statement = statement.where(Drone.status == status_filter)
    return list(db.scalars(statement))


@router.post("", response_model=DroneRead, status_code=status.HTTP_201_CREATED)
@router.post("/from-template", response_model=DroneRead, status_code=status.HTTP_201_CREATED)
def create_drone(
    payload: DroneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Drone:
    drone_type = db.get(DroneType, payload.drone_type_id)
    if not drone_type or not drone_type.is_active:
        raise HTTPException(status_code=422, detail="Aktiver Drohnen-Typ nicht gefunden.")
    owner_user_id = (
        payload.owner_user_id
        if current_user.role == "admin" and payload.owner_user_id
        else current_user.id
    )
    if not db.get(User, owner_user_id):
        raise HTTPException(status_code=422, detail="Eigentümer nicht gefunden.")
    drone = Drone(
        **payload.model_dump(exclude={"owner_user_id"}),
        owner_user_id=owner_user_id,
    )
    db.add(drone)
    db.commit()
    db.refresh(drone)
    return drone


@router.get("/{drone_id}", response_model=DroneRead)
def get_drone(
    drone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Drone:
    return _get_visible_drone(db, drone_id, current_user)


@router.get("/{drone_id}/resolved", response_model=ResolvedDrone)
def get_resolved_drone(
    drone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResolvedDrone:
    return resolve_drone(_get_visible_drone(db, drone_id, current_user))


@router.patch("/{drone_id}", response_model=DroneRead)
def update_drone(
    drone_id: int,
    payload: DroneUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Drone:
    drone = _get_visible_drone(db, drone_id, current_user)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(drone, field, value)
    db.commit()
    db.refresh(drone)
    return drone


@router.delete("/{drone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_drone(
    drone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    drone = _get_visible_drone(db, drone_id, current_user)
    if drone.flights:
        raise HTTPException(
            status_code=409,
            detail="Drohnen mit Flügen können nur archiviert werden.",
        )
    db.delete(drone)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
