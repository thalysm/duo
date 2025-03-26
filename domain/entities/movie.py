from pydantic import BaseModel
from typing import List, Optional

class Genre(BaseModel):
    id: int
    name: str

class Movie(BaseModel):
    id: int
    title: str
    original_title: str
    overview: Optional[str]
    release_date: str
    popularity: float
    vote_average: float
    vote_count: int
    genres: List[Genre]
    origin_country: List[str]
    poster_path: Optional[str]
    backdrop_path: Optional[str]
