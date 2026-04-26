from pwdlib import PasswordHash

from app.core import get_db_session
from app.models import User
from app.repositories import NotFoundError, UserRepository

password_hash = PasswordHash.recommended()


class Unauthorised(Exception):  # noqa
    pass


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def authenticate_user(login: str, password: str) -> User:
    repo = UserRepository(next(get_db_session()))

    try:
        user = repo.get_by_email(login)
    except NotFoundError as err:
        raise Unauthorised("User not found") from err

    if not verify_password(password, user.password):
        raise Unauthorised("Wrong password")

    if not user.is_active:
        raise Unauthorised(f"User {user.id} is not active")

    return user
