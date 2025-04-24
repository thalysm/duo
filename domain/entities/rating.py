from pydantic import BaseModel, Field
from typing import List

class Rating(BaseModel):
    movie_id: int
    rating: float = Field(..., ge=0, le=10)  # Avaliação entre 0 e 10
    movies_associated: List[float]
    similarity: float = 0.0
