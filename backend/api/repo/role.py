from api.orm import models
from api.repo.base import BaseRepo


class RoleRepo(BaseRepo[models.Role]):
    model = models.Role
