import uuid

from api.choices import ReviewStatus
from api.orm import models


def generate_movie_logo_file_path(file_id: uuid.UUID) -> str:
    return f"/api/file/{file_id}"


def calculate_ratereel_rating(reviews: list[models.Review]) -> float:
    approved_reviews_ratings = [
        review.rating for review in reviews if review.status == ReviewStatus.approved
    ]
    if not approved_reviews_ratings:
        return 0
    return round(sum(approved_reviews_ratings) / len(approved_reviews_ratings), 1)
