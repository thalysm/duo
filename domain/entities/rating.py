from pydantic import BaseModel, Field

class Rating(BaseModel):
    movie_id: int
    user_id: str
    rating: float = Field(..., ge=0, le=10)  # Avaliação entre 0 e 10
    comment: str | None = None
