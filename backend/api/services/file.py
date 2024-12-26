from api.repo.file import FileRepo
from api.orm import models
from api.services.schemas import file as schemas
from api.services.base import BaseService


class FileService(BaseService[models.File, schemas.File, FileRepo]):
    model = models.File
    service_schema = schemas.File
    repo = FileRepo
