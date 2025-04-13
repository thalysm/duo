from pymongo import MongoClient
from imdb import Cinemagoer
from dotenv import load_dotenv
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import os

# Carregar variáveis de ambiente
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Conectar ao MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
movies_collection = db["movies"]

# Inicializa a API do IMDb
ia = Cinemagoer()

# Arquivo de log
LOG_FILE = "imdb_update_errors.log"

def log_error(movie_id, imdb_id, error_msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] _id: {movie_id}, imdb_id: tt{imdb_id}, error: {error_msg}\n")

# Consulta
query = {
    "imdb_id": {"$exists": True},
    "$or": [
        {"overview": {"$exists": False}},
        {"overview": None},
        {"overview": ""},
        {"tagline": {"$exists": False}},
        {"tagline": None},
        {"tagline": ""},
    ]
}

projection = {
    "_id": 1,
    "imdb_id": 1,
    "overview": 1,
    "tagline": 1
}

# Processa um único filme
def process_movie(movie):
    imdb_id = movie.get("imdb_id", "").replace("tt", "")
    try:
        imdb_movie = ia.get_movie(imdb_id)
        ia.update(imdb_movie, info=["main", "plot"])

        update_data = {
            "vote_average": imdb_movie.get("rating"),
            "vote_count": imdb_movie.get("votes"),
            "popularity": float(imdb_movie.get("votes") or 0) / 1000
        }

        if not movie.get("overview"):
            plot = imdb_movie.get("plot")
            if plot:
                update_data["overview"] = plot[0].split("::")[0]

        if not movie.get("tagline"):
            tagline = imdb_movie.get("tagline") or imdb_movie.get("plot outline")
            if tagline:
                update_data["tagline"] = tagline

        update_data = {k: v for k, v in update_data.items() if v is not None}

        if update_data:
            movies_collection.update_one({"_id": movie["_id"]}, {"$set": update_data})
        return True
    except Exception as e:
        log_error(movie["_id"], imdb_id, str(e))
        return False

# Processar por lotes
batch_size = 500
total = movies_collection.count_documents(query)
print(f"Total a processar: {total}")

start_batch = 0
start_index = start_batch * batch_size

for i in range(start_index, total, batch_size):
    cursor = movies_collection.find(query, projection).skip(i).limit(batch_size)
    batch = list(cursor)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_movie, movie) for movie in batch]
        for _ in tqdm(as_completed(futures), total=len(futures), desc=f"Batch {i//batch_size + 1}"):
            pass

print("Atualização finalizada.")
