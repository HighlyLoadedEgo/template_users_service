import os
from enum import Enum

PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH", default="./private.key")
PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY_PATH", default="./public.key")


class Roles(str, Enum):
    ADMIN = "admin"
    USER = "user"
    STAFF = "staff"


class TokenTypes(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
