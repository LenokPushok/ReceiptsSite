from pydantic import BaseModel, ConfigDict
import uuid
import datetime


class BaseServiceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IdCreatedDeletedServiceSchemaMixin(BaseModel):
    id: uuid.UUID
    created_at: datetime.datetime
    deleted: bool
