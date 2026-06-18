from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password
from app.db.database import Base, engine
from app.models import User


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    settings = get_settings()
    with Session(engine) as db:
        existing_admin = db.scalar(
            select(User).where(User.username == settings.initial_admin_username)
        )
        if existing_admin:
            return
        db.add(
            User(
                username=settings.initial_admin_username,
                email=settings.initial_admin_email,
                full_name="Administrator",
                password_hash=hash_password(settings.initial_admin_password),
                role="admin",
                is_active=True,
            )
        )
        db.commit()
