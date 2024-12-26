from api.choices import ReviewStatus
from api.services.schemas.base import (
    BaseServiceSchema,
    IdCreatedDeletedServiceSchemaMixin,
)
import uuid
from api.services.schemas.user import User
from pydantic import BaseModel


class Review(BaseServiceSchema, IdCreatedDeletedServiceSchemaMixin):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    content: str
    rating: float
    status: ReviewStatus
    user: User


class ReviewCreate(BaseServiceSchema):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    content: str
    rating: float
    status: ReviewStatus = ReviewStatus.pending


class ReviewStatusUpdate(BaseServiceSchema):
    review_id: uuid.UUID
    movie_id: uuid.UUID
    status: ReviewStatus
