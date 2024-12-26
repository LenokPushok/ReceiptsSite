from typing import Annotated
from api.utils.token_validator import TokenValidator
from api.utils.dto import TokenData
from fastapi import APIRouter, status, Security, Depends
import uuid
from api.orm.session import get_session
from api.services.user import UserService
from api.routes.schemas import user as api_schemas
from api.utils.token_validator import TokenValidator
from api import choices

router = APIRouter(prefix="/api/user", tags=["user"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create user with login and password / Registration",
)
def create_user(payload: api_schemas.UserCreate):
    with get_session() as session:
        return UserService(session).create_user(payload.to_service_schema())


@router.get(
    "/",
    response_model=api_schemas.User,
    status_code=status.HTTP_200_OK,
    summary="Get information of current authenticated user",
)
def get_user(token_data: Annotated[TokenData, Depends(TokenValidator())]):
    with get_session() as session:
        user = UserService(session).get_resource_by_filters(id=token_data.id)
        return api_schemas.User.from_service_schema(user)


@router.get(
    "/{resource_id}",
    response_model=api_schemas.User,
    status_code=status.HTTP_200_OK,
    summary="[Admin] Get information of user by id",
    dependencies=[Security(TokenValidator(role_name=choices.Role.admin))],
)
def get_user_by_id(resource_id: uuid.UUID):
    with get_session() as session:
        user = UserService(session).get_resource_by_filters(id=resource_id)
        return api_schemas.User.from_service_schema(user)
