import uuid

from api.repo.review import ReviewRepo
from api.orm import models
from api.repo.movie import MovieRepo
from api.services.schemas import review as schemas
from api.services.base import BaseService
from api.repo import exceptions as repo_exc
from api.services import exceptions as service_exc
from api.choices import ReviewStatus


class ReviewService(BaseService[models.Review, schemas.Review, ReviewRepo]):
    model = models.Review
    service_schema = schemas.Review
    repo = ReviewRepo

    def create_movie_review(self, payload: schemas.ReviewCreate) -> None:
        try:
            MovieRepo(self.session).get_resource_by_filters(id=payload.movie_id)
        except repo_exc.NotFoundError:
            raise service_exc.NotFoundError(
                detail=f"Movie {payload.movie_id} not found"
            )
        try:
            self.repo(self.session).get_resource_by_filters(
                user_id=payload.user_id,
                movie_id=payload.movie_id,
                status__in=[ReviewStatus.pending.value, ReviewStatus.approved.value],
            )
        except repo_exc.NotFoundError:
            review_orm = models.Review(
                user_id=payload.user_id,
                movie_id=payload.movie_id,
                content=payload.content,
                rating=payload.rating,
                status=payload.status.value,
            )

            self.session.add(review_orm)
            self.session.commit()
            return
        raise service_exc.AlreadyExistError(
            detail=f"User {payload.user_id} already left review for movie {payload.movie_id}"
        )

    def change_movie_review_status(self, payload: schemas.ReviewStatusUpdate) -> None:
        try:
            review_orm = self.repo(self.session).get_resource_by_filters(
                id=payload.review_id, movie_id=payload.movie_id
            )
        except repo_exc.NotFoundError:
            raise service_exc.NotFoundError(
                detail=f"Review {payload.review_id} not found for movie {payload.movie_id}"
            )
        review_orm.status = payload.status.value
        self.session.commit()
