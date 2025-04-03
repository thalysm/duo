from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.movies import router as movies_router
from api.routes.process_movies import router as process_movies_router
from api.routes.recommendations import router as recommendations_router
from api.routes.ratings import router as ratings_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo todas as rotas existentes
app.include_router(movies_router, tags=["Movies"])
app.include_router(process_movies_router, prefix="/process", tags=["Processing"])
app.include_router(recommendations_router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(ratings_router, tags=["Ratings"])
