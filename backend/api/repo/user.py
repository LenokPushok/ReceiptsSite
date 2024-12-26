from sqlalchemy import sql
from sqlalchemy.orm import joinedload

from api.orm import models
from api.repo.base import BaseRepo


class UserRepo(BaseRepo[models.User]):
    model = models.User

    def _apply_relations(self, stmt: sql.Select) -> sql.Select:
        for relation in (self.model.role, self.model.reviews):
            stmt = stmt.options(joinedload(relation))
        return stmt
