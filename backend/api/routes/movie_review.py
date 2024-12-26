import uuid
from typing import Annotated

from fastapi import APIRouter, status, Depends, Security
from api.utils.dto import TokenData
from api import choices
from api.orm.session import get_session
from api.services.review import ReviewService
from api.routes.schemas import review as api_schemas
from api.utils.token_validator import TokenValidator

router = APIRouter(prefix="/api/movie/{movie_id}/review", tags=["movie-review"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, summary="Create review for movie"
)
def create_movie_review(
    movie_id: uuid.UUID,
    payload: api_schemas.ReviewCreate,
    token_data: Annotated[TokenData, Depends(TokenValidator())],
):
    with get_session() as session:
        return ReviewService(session).create_movie_review(
            payload.to_service_schema(movie_id=movie_id, user_id=token_data.id)
        )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[api_schemas.Review],
    summary="Get list of reviews for movie",
)
def get_movie_reviews(movie_id: uuid.UUID):
    with get_session() as session:
        movie_reviews = ReviewService(session).get_resources(
            movie_id=movie_id, status=choices.ReviewStatus.approved.value
        )
        return [
            api_schemas.Review.from_service_schema(movie_review)
            for movie_review in movie_reviews
        ]


@router.patch(
    "/{review_id}",
    status_code=status.HTTP_201_CREATED,
    summary="[Admin] Change review status",
    dependencies=[Security(TokenValidator(role_name=choices.Role.admin))],
)
def change_movie_review_status(
    movie_id: uuid.UUID, review_id: uuid.UUID, payload: api_schemas.ReviewStatusUpdate
):
    with get_session() as session:
        return ReviewService(session).change_movie_review_status(
            payload.to_service_schema(movie_id=movie_id, review_id=review_id)
        )
