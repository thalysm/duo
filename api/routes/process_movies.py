from fastapi import APIRouter, BackgroundTasks
from infrastructure.services.movie import MovieService

router = APIRouter()

@router.post("/update_movies")
def update_movies(background_tasks: BackgroundTasks):
    """Atualiza os filmes no banco e processa as recomendações em segundo plano."""
    background_tasks.add_task(MovieService.update_movies)
    return {"status": "Atualização iniciada! Os filmes estão sendo processados em background."}
