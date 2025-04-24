import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Teste: POST /ratings
def test_add_rating():
    payload = {"movie_id": 123, "rating": 8, "similarity": 0.9, "movies_associated": [1,2,3,4,5,6,7,8,9,10]}
    response = client.post("/ratings", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Rating added successfully"

# Teste: GET /ratings/movie/{movie_id}
def test_get_ratings_for_movie():
    response = client.get("/ratings/movie/123")
    assert response.status_code == 200
    assert isinstance(response.json(), list)