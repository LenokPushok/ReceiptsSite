from api.orm import models
from api.repo.base import BaseRepo


class FileRepo(BaseRepo[models.File]):
    model = models.File
