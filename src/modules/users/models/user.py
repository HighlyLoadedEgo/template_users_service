import uuid

from sqlalchemy import (
    Boolean,
    String,
)
from sqlalchemy.dialects.postgresql import (
    BYTEA,
    UUID,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.core.auth import Roles
from src.core.database.postgres.models import BaseWithDate


class User(BaseWithDate):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(BYTEA, nullable=False)
    email: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(11), unique=True)
    role: Mapped[str] = mapped_column(
        String(24), default=Roles.USER.value, nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
