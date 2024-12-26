from typing import Annotated

from fastapi import APIRouter, status, Depends, Security
from api import choices
from api.orm.session import get_session
from api.services.review import ReviewService
from api.routes.schemas import review as api_schemas
from api.utils.dto import TokenData
from api.utils.token_validator import TokenValidator

router = APIRouter(prefix="/api/user/review", tags=["user-review"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[api_schemas.Review],
    summary="Get approved reviews of current authenticated user",
)
def get_user_reviews(token_data: Annotated[TokenData, Depends(TokenValidator())]):
    with get_session() as session:
        user_reviews = ReviewService(session).get_resources(
            status=choices.ReviewStatus.approved.value, user_id=token_data.id
        )
        return [
            api_schemas.Review.from_service_schema(user_review)
            for user_review in user_reviews
        ]
