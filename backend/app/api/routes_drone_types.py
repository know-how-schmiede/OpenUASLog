from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, require_roles
from app.db.database import get_db
from app.models import DroneType, User
from app.schemas.drone_type import DroneTypeCreate, DroneTypeRead, DroneTypeUpdate

router = APIRouter(prefix="/drone-types", tags=["drone-types"])


@router.get("", response_model=list[DroneTypeRead])
def list_drone_types(
    active_only: bool = False,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[DroneType]:
    statement = select(DroneType).order_by(DroneType.manufacturer, DroneType.model)
    if active_only:
        statement = statement.where(DroneType.is_active.is_(True))
    return list(db.scalars(statement))


@router.post("", response_model=DroneTypeRead, status_code=status.HTTP_201_CREATED)
def create_drone_type(
    payload: DroneTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
) -> DroneType:
    drone_type = DroneType(**payload.model_dump(), created_by_user_id=current_user.id)
    db.add(drone_type)
    db.commit()
    db.refresh(drone_type)
    return drone_type


@router.get("/{drone_type_id}", response_model=DroneTypeRead)
def get_drone_type(
    drone_type_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> DroneType:
    drone_type = db.get(DroneType, drone_type_id)
    if not drone_type:
        raise HTTPException(status_code=404, detail="Drohnen-Typ nicht gefunden.")
    return drone_type


@router.patch("/{drone_type_id}", response_model=DroneTypeRead)
def update_drone_type(
    drone_type_id: int,
    payload: DroneTypeUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
) -> DroneType:
    drone_type = db.get(DroneType, drone_type_id)
    if not drone_type:
        raise HTTPException(status_code=404, detail="Drohnen-Typ nicht gefunden.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(drone_type, field, value)
    db.commit()
    db.refresh(drone_type)
    return drone_type


@router.delete("/{drone_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_drone_type(
    drone_type_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
) -> Response:
    drone_type = db.get(DroneType, drone_type_id)
    if not drone_type:
        raise HTTPException(status_code=404, detail="Drohnen-Typ nicht gefunden.")
    if drone_type.drones:
        raise HTTPException(
            status_code=409,
            detail="Verwendete Drohnen-Typen können nur deaktiviert werden.",
        )
    db.delete(drone_type)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
