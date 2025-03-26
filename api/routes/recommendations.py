from fastapi import APIRouter, HTTPException
from infrastructure.services.recommendation_engine import RecommendationEngine

router = APIRouter()
engine = RecommendationEngine()

@router.post("/recommend")
def get_recommendations(user1_movies: list[str], user2_movies: list[str]):
    if not user1_movies or not user2_movies:
        raise HTTPException(status_code=400, detail="Ambos os usuários devem selecionar filmes.")
    
    recommendations = engine.recommend(user1_movies, user2_movies)
    return {"recommendations": recommendations}
