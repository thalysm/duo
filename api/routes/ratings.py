from fastapi import APIRouter
from domain.entities.rating import Rating
from infrastructure.repositories.rating_repository import RatingRepository

router = APIRouter()
rating_repo = RatingRepository()

@router.post("/ratings", tags=["Ratings"])
def add_rating(rating: Rating):
    return rating_repo.add_rating(rating.model_dump())

@router.get("/ratings/movie/{movie_id}", tags=["Ratings"])
def get_ratings_for_movie(movie_id: int):
    return rating_repo.get_ratings_for_movie(movie_id)


