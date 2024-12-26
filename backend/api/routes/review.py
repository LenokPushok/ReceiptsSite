from fastapi import APIRouter, status, Depends, Security
from api import choices
from api.orm.session import get_session
from api.services.review import ReviewService
from api.routes.schemas import review as api_schemas
from api.utils.token_validator import TokenValidator

router = APIRouter(prefix="/api/review", tags=["review"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[api_schemas.Review],
    summary="[Admin] Get list of pending reviews",
    dependencies=[Security(TokenValidator(role_name=choices.Role.admin))],
)
def get_pending_reviews():
    with get_session() as session:
        pending_reviews = ReviewService(session).get_resources(
            status=choices.ReviewStatus.pending.value
        )
        return [
            api_schemas.Review.from_service_schema(pending_review)
            for pending_review in pending_reviews
        ]
