import pytest
from infrastructure.services.recommendation_engine import RecommendationEngine

# Teste básico com dois IDs reais

def test_recommendation_returns_n_results():
    engine = RecommendationEngine()

    user1_ids = [engine.df.iloc[0]["id"]]
    user2_ids = [engine.df.iloc[1]["id"]]

    recommendations = engine.recommend(user1_ids, user2_ids, top_n=5)

    assert isinstance(recommendations, list)
    assert len(recommendations) <= 5
    for item in recommendations:
        assert "original_title" in item
        assert "id" in item

# Teste com listas vazias (deve retornar vazio)
def test_recommendation_empty_input():
    engine = RecommendationEngine()
    recommendations = engine.recommend([], [], top_n=5)
    assert recommendations == []

# Teste com ID inexistente (deve retornar vazio)
def test_recommendation_invalid_id():
    engine = RecommendationEngine()
    recommendations = engine.recommend([999999999], [888888888], top_n=5)
    assert recommendations == []
