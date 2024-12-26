from pydantic import BaseModel
import uuid
from api import choices


class TokenData(BaseModel):
    id: uuid.UUID
    username: str
    role_name: choices.Role
