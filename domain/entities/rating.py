from pydantic import BaseModel, Field

class Rating(BaseModel):
    movie_id: int
    rating: float = Field(..., ge=0, le=10)  # Avaliação entre 0 e 10
    movies_associated: list = []
    similarity: float = 0.0
