from api.orm import models
from api.repo.base import BaseRepo


class ReviewRepo(BaseRepo[models.Review]):
    model = models.Review
