import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Teste: POST /recommendations/recommend (entrada inválida)
def test_recommend_invalid():
    response = client.post("/recommendations/recommend", json={"user1_movies": [], "user2_movies": []})
    assert response.status_code == 400
    assert response.json()["detail"] == "Ambos os usuários devem selecionar filmes."