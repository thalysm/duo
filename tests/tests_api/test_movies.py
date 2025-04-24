import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Teste: GET /movies
def test_get_all_movies():
    response = client.get("/movies?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Teste: GET /movies/{movie_id}
def test_get_movie_by_id():
    response = client.get("/movies/1")  
    assert response.status_code == 200

# Teste: GET /movies/name/{movie_name}
def test_get_movie_by_name():
    response = client.get("/movies/name/Matrix")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)

# Teste: GET /movies/title_embeddings/{movie_name}
# def test_get_movie_by_title_embeddings():
#     response = client.get("/movies/title_embeddings/Matrix")
#     assert response.status_code == 200
#     result = response.json()
#     assert isinstance(result, list)




