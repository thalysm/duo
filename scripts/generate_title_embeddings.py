from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from dotenv import load_dotenv
import os

load_dotenv()

# Conexão com o MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
API_TMDB = os.getenv("API_TMDB")
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
movies_collection = db['movies']  # Coleção onde os filmes serão atualizados

# Carrega o modelo
print("Carregando modelo de embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Busca os documentos sem 'title_embedding'
print("Buscando filmes sem embedding...")
movies = list(movies_collection.find(
    {"title_embedding": {"$exists": False}},
    {"_id": 1, "title": 1, "overview": 1, "genres": 1}
))

print(f"Gerando embeddings para {len(movies)} filmes...")

for movie in tqdm(movies):
    title = movie.get("title", "")
    overview = movie.get("overview", "")
    genres = " ".join([g["name"] for g in movie.get("genres", []) if "name" in g])

    full_text = f"{title}. {overview}. Gêneros: {genres}"

    embedding = model.encode(full_text).tolist()

    movies_collection.update_one(
        {"_id": movie["_id"]},
        {"$set": {"title_embedding": embedding}}
    )

print("✅ Embeddings gerados com sucesso!")
