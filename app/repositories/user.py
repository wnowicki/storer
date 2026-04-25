from sqlmodel import Session

from app.models import User, UserCreate, UserUpdate

from .base import BaseRepository


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_email(self, email: str) -> User:
        return self._get_by("email", email)
