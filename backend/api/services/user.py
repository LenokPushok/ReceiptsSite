from passlib.context import CryptContext

from api.repo.user import UserRepo
from api.repo.role import RoleRepo
from api.orm import models
from api.services.schemas import user as schemas
from api.services.base import BaseService
from api.repo import exceptions as repo_exc
from api.services import exceptions as service_exc
from api import choices
from api.utils.jwt_tool import jwt_tool

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(BaseService[models.User, schemas.User, UserRepo]):
    model = models.User
    service_schema = schemas.User
    repo = UserRepo

    def create_user(self, payload: schemas.UserCreate) -> None:
        try:
            self.repo(self.session).get_resource_by_filters(username=payload.username)
        except repo_exc.NotFoundError:
            hashed_password = pwd_context.hash(payload.password)
            role = RoleRepo(self.session).get_resource_by_filters(
                title=choices.Role.user
            )
            user = models.User(
                username=payload.username, password=hashed_password, role_id=role.id
            )
            self.session.add(user)
            self.session.commit()
            return
        raise service_exc.AlreadyExistError(
            detail=f"User {payload.username} already exist"
        )

    def auth_user(self, payload: schemas.TokenCreate) -> str:
        try:
            user = self.repo(self.session).get_resource_by_filters(
                username=payload.username
            )
        except repo_exc.NotFoundError as e:
            raise service_exc.NotFoundError(
                detail=f"User {payload.username} does not exist"
            ) from e

        if pwd_context.verify(payload.password, user.password):
            return jwt_tool.generate_token(
                id=str(user.id), username=user.username, role_name=user.role.title
            )
        raise service_exc.UnauthorizedError(
            detail=f"Wrong password for user {payload.username}"
        )
