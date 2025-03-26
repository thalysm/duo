from domain.entities.recommendation import Recommendation
from infrastructure.services.recommendation_engine import RecommendationEngine

class GetRecommendationsUseCase:
    def __init__(self, recommendation_engine: RecommendationEngine):
        self.recommendation_engine = recommendation_engine

    def execute(self, input_vectors):
        recommended_movies = self.recommendation_engine.get_recommendations(input_vectors)
        return Recommendation(input_vectors=input_vectors, recommended_movies=recommended_movies)
