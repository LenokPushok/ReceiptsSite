from typing import TypeVar, Generic, Type
from pydantic import BaseModel
from api.repo.base import BaseRepo
from sqlalchemy.orm import Session
from api.repo import exceptions as repo_exc
from api.services import exceptions as service_exc

ModelType = TypeVar("ModelType")
ServiceSchema = TypeVar("ServiceSchema", bound=BaseModel)
Repo = TypeVar("Repo", bound=BaseRepo)


class BaseService(Generic[ModelType, ServiceSchema, Repo]):
    model: Type[ModelType]
    service_schema: Type[ServiceSchema]
    repo: Type[Repo]

    def __init__(self, session: Session):
        self.session = session

    def get_resource_by_filters(self, **filters) -> ServiceSchema:
        try:
            result = self.repo(self.session).get_resource_by_filters(**filters)
        except repo_exc.NotFoundError as e:
            raise service_exc.NotFoundError(detail=e.detail) from e
        except repo_exc.MultipleFoundError as e:
            raise service_exc.MultipleFoundError(detail=e.detail) from e
        return self.service_schema.model_validate(result)

    def get_resources(self, **filters) -> list[ServiceSchema]:
        result = self.repo(self.session).get_resources(**filters)
        return [self.service_schema.model_validate(row) for row in result]
