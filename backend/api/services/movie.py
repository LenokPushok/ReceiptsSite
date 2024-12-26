from api.repo.movie import MovieRepo
from api.orm import models
from api.services.schemas import movie as schemas
from api.services.base import BaseService
from api.repo import exceptions as repo_exc
from api.services import exceptions as service_exc
from tempfile import SpooledTemporaryFile
import uuid


class MovieService(BaseService[models.Movie, schemas.Movie, MovieRepo]):
    model = models.Movie
    service_schema = schemas.Movie
    repo = MovieRepo

    def create_movie(
        self, payload: schemas.MovieCreate, logo_file: SpooledTemporaryFile
    ) -> None:
        try:
            self.repo(self.session).get_resource_by_filters(title=payload.title)
        except repo_exc.NotFoundError:
            file_id = uuid.uuid4()
            logo_file_path = f"movies_imgs/movie_{str(file_id)}.jpg"
            with open(logo_file_path, "wb") as file:
                file.write(logo_file.read())
            file_orm = models.File(path=logo_file_path, id=file_id)
            self.session.add(file_orm)

            movie_orm = models.Movie(
                title=payload.title,
                description=payload.description,
                imdb_rating=payload.imdb_rating,
                logo_file_id=file_id,
            )

            self.session.add(movie_orm)
            self.session.commit()
            return
        raise service_exc.AlreadyExistError(
            detail=f"Movie {payload.title} already exist"
        )
