from sqlalchemy import sql
from sqlalchemy.orm import joinedload
from api.orm import models
from api.repo.base import BaseRepo


class MovieRepo(BaseRepo[models.Movie]):
    model = models.Movie

    def _apply_relations(self, stmt: sql.Select) -> sql.Select:
        for relation in (self.model.reviews, self.model.logo_file):
            stmt = stmt.options(joinedload(relation))
        return stmt
