from api.services.schemas.base import (
    BaseServiceSchema,
    IdCreatedDeletedServiceSchemaMixin,
)


class File(BaseServiceSchema, IdCreatedDeletedServiceSchemaMixin):
    path: str
