from typing import Annotated

from fastapi import APIRouter, status, Depends
from api.orm.session import get_session
from api.services.user import UserService
from api.routes.schemas import user as api_schemas
from api.utils.dto import TokenData
from api.utils.token_validator import TokenValidator

router = APIRouter(prefix="/api/token", tags=["token"])


@router.post(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create token with login and password / Authentication",
)
def create_token(payload: api_schemas.TokenCreate):
    with get_session() as session:
        return UserService(session).auth_user(payload.to_service_schema())


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Invalidate current authenticated user token / Logout",
)
def delete_token(token_data: Annotated[TokenData, Depends(TokenValidator())]):
    # todo
    return status.HTTP_204_NO_CONTENT
