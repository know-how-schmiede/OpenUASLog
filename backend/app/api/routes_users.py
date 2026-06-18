from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.core.security import hash_password
from app.db.database import get_db
from app.models import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])
admin_only = require_roles("admin")


@router.get("", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
) -> list[User]:
    return list(db.scalars(select(User).order_by(User.username)))


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
) -> User:
    if payload.role not in {"admin", "pilot"}:
        raise HTTPException(status_code=422, detail="Im MVP sind nur Admin und Pilot zulässig.")
    duplicate = db.scalar(
        select(User).where(or_(User.username == payload.username, User.email == payload.email))
    )
    if duplicate:
        raise HTTPException(status_code=409, detail="Benutzername oder E-Mail existiert bereits.")
    user = User(
        **payload.model_dump(exclude={"password"}),
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden.")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden.")
    values = payload.model_dump(exclude_unset=True)
    password = values.pop("password", None)
    if values.get("role") not in {None, "admin", "pilot"}:
        raise HTTPException(status_code=422, detail="Im MVP sind nur Admin und Pilot zulässig.")
    for field, value in values.items():
        setattr(user, field, value)
    if password:
        user.password_hash = hash_password(password)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
) -> Response:
    if current_user.id == user_id:
        raise HTTPException(status_code=409, detail="Das eigene Konto kann nicht gelöscht werden.")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden.")
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
