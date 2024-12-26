from api.repo.role import RoleRepo
from api.orm import models
from api.services.schemas import user as schemas
from api.services.base import BaseService


class RoleService(BaseService[models.Role, schemas.Role, RoleRepo]):
    model = models.Role
    service_schema = schemas.Role
    repo = RoleRepo
