from bitaware import BitAware, BitFlag
from sqlmodel import Field, SQLModel

from .base import TimeStampModel


class Permission(BitFlag):
    """User permissions for the system"""

    USER = 1
    ADMIN = 2


class UserRole(BitAware[Permission]):
    """User role for the system"""

    USER = Permission.USER
    ADMIN = Permission.ADMIN

    def __init__(self, value: int):
        super().__init__(value, Permission)


class UserBase(SQLModel):
    name: str | None = None
    email: str
    password: str
    is_active: bool = True
    role: UserRole = Field(default=UserRole(UserRole.USER))


class User(UserBase, TimeStampModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    pass
