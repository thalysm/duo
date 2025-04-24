import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Teste: POST /process/update_movies
def test_update_movies():
    response = client.post("/process/update_movies")
    assert response.status_code == 200
    assert "status" in response.json()