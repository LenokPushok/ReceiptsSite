from pydantic import BaseModel
from api.services.schemas.base import BaseServiceSchema
import uuid
from typing import TypeVar, Generic

ServiceSchema = TypeVar("ServiceSchema", bound=BaseServiceSchema)
ApiSchema = TypeVar("ApiSchema", bound="BaseApiSchema")


class BaseApiSchema(BaseModel, Generic[ServiceSchema]):
    @classmethod
    def from_service_schema(cls, service_schema: ServiceSchema) -> ApiSchema:
        raise NotImplemented

    def to_service_schema(self, **kwargs) -> ServiceSchema:
        raise NotImplemented


class IdApiSchemaMixin(BaseModel):
    id: uuid.UUID
