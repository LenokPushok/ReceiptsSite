from typing_extensions import Annotated

from fastapi import APIRouter, status, Security, Depends, UploadFile, Form
import uuid

from api.orm.session import get_session
from api.services.movie import MovieService
from api.routes.schemas import movie as api_schemas
from api.utils.token_validator import TokenValidator
from api import choices

router = APIRouter(prefix="/api/movie", tags=["movie"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="[Admin] Create movie",
    dependencies=[Security(TokenValidator(role_name=choices.Role.admin))],
)
def create_movie(
    logo_file: UploadFile,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    imdb_rating: Annotated[float, Form()],
):
    with get_session() as session:
        payload = api_schemas.MovieCreate(
            title=title, description=description, imdb_rating=imdb_rating
        )
        return MovieService(session).create_movie(
            payload=payload.to_service_schema(), logo_file=logo_file.file
        )


@router.get(
    "/",
    response_model=list[api_schemas.MovieMulti],
    status_code=status.HTTP_200_OK,
    summary="Get list of movies",
)
def get_movies():
    with get_session() as session:
        movies = MovieService(session).get_resources()
        return [api_schemas.MovieMulti.from_service_schema(movie) for movie in movies]


@router.get(
    "/{resource_id}",
    response_model=api_schemas.MovieDetailed,
    status_code=status.HTTP_200_OK,
    summary="Get detailed movie info by id",
)
def get_movie(resource_id: uuid.UUID):
    with get_session() as session:
        movie = MovieService(session).get_resource_by_filters(id=resource_id)
        return api_schemas.MovieDetailed.from_service_schema(movie)
