from fastapi import APIRouter
from infrastructure.repositories.movie_repository import MovieRepository

router = APIRouter()
movie_repo = MovieRepository()

@router.get("/movies", tags=["Movies"])
def get_all_movies(limit: int = 50):
    return movie_repo.get_all_movies(limit)

@router.get("/movies/{movie_id}", tags=["Movies"])
def get_movie_by_id(movie_id: int):
    movie = movie_repo.get_movie_by_id(movie_id)
    if movie:
        return movie
    return {"error": "Movie not found"}


@router.get("/movies/name/{movie_name}", tags=["Movies"])
def get_movie_by_name(movie_name: str):
    movie = movie_repo.get_movie_by_name(movie_name)
    if movie:
        return movie
    return {"error": "Movie not found"}

@router.get("/movies/title_embeddings/{movie_name}", tags=["Movies"])
def get_movie_by_title_embeddings(movie_name: str):
    movie = movie_repo.get_movie_by_title_embeddings(movie_name)
    if movie:
        return movie
    return {"error": "Movie not found"}
