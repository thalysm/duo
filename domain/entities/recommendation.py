from pydantic import BaseModel
from typing import List

class Recommendation(BaseModel):
    input_vectors: List[float]
    recommended_movies: List[str]  # Lista de IDs dos filmes recomendados
