from api.services.schemas.base import (
    BaseServiceSchema,
    IdCreatedDeletedServiceSchemaMixin,
)
from api.services.schemas.role import Role
import uuid


class User(BaseServiceSchema, IdCreatedDeletedServiceSchemaMixin):
    username: str
    password: str
    role_id: uuid.UUID
    role: Role


class TokenCreate(BaseServiceSchema):
    username: str
    password: str


class UserCreate(TokenCreate):
    pass
