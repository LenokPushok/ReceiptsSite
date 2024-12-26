import uuid
from pydantic import Field
from api.routes.schemas.base import (
    BaseApiSchema,
    IdApiSchemaMixin,
    ServiceSchema,
    ApiSchema,
)
from api.services.schemas import review as service_schemas
from api.choices import ReviewStatus


class Review(BaseApiSchema[service_schemas.Review], IdApiSchemaMixin):
    username: str
    movie_id: uuid.UUID
    content: str
    rating: float = Field(..., ge=1, le=5)

    @classmethod
    def from_service_schema(cls, service_schema: service_schemas.Review) -> "Review":
        return cls(
            id=service_schema.id,
            username=service_schema.user.username,
            movie_id=service_schema.movie_id,
            content=service_schema.content,
            rating=service_schema.rating,
        )


class ReviewCreate(BaseApiSchema[service_schemas.ReviewCreate]):
    content: str
    rating: float = Field(..., ge=1, le=5)

    def to_service_schema(self, **kwargs) -> service_schemas.ReviewCreate:
        return service_schemas.ReviewCreate.model_validate(self.model_dump() | kwargs)


class ReviewStatusUpdate(BaseApiSchema[service_schemas.ReviewStatusUpdate]):
    status: ReviewStatus

    def to_service_schema(self, **kwargs) -> service_schemas.ReviewStatusUpdate:
        return service_schemas.ReviewStatusUpdate.model_validate(
            self.model_dump() | kwargs
        )
