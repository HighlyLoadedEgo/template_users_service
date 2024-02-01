from pydantic import TypeAdapter

from src.modules.users.dtos import FullUserSchema

full_user_adapter = TypeAdapter(list[FullUserSchema])
