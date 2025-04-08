from core.database import get_collection
from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

class MovieRepository:
    def __init__(self):
        self.collection = get_collection("movies")

    def get_all_movies(self, limit=50):
        movies = self.collection.find({}, {"_id": 0}).limit(limit)
        return list(movies)

    def get_movie_by_id(self, movie_id: int):
        return self.collection.find_one({"id": movie_id}, {"_id": 0})
    
    def get_movie_by_name(self, movie_name: str):
        movies_cursor = self.collection.find(
            {"title": {"$regex": movie_name, "$options": "i"}}, {"_id": 0}
        )
        
        movies = list(movies_cursor)

        if not movies:
            return []

        # Calcula a similaridade e filtra por score mínimo
        scored_movies = [
            (movie, fuzz.partial_ratio(movie.get("original_title", ""), movie_name))
            for movie in movies
        ]
        filtered = [movie for movie, score in scored_movies if score >= 70]

        # Ordena por maior similaridade e limita a 12 resultados
        ranked = sorted(
            filtered,
            key=lambda movie: fuzz.partial_ratio(movie.get("title", ""), movie_name),
            reverse=True
        )

        return ranked[:12]
    

    def get_movie_by_title_embeddings(self, movie_name: str):
        query_embedding = model.encode([movie_name])  # (1, 384)

        # Pega só os filmes que já têm embedding
        movies = list(self.collection.find(
            {"title_embedding": {"$exists": True}}, {"_id": 0}
        ))

        if not movies:
            return []

        # Pega vetores e calcula similaridade
        movie_embeddings = np.array([m["title_embedding"] for m in movies])
        similarities = cosine_similarity(query_embedding, movie_embeddings)[0]

        # Junta com os filmes
        movies_with_score = [
            (movie, float(similarity))
            for movie, similarity in zip(movies, similarities)
            if similarity >= 0.7  
        ]

        # Ordena por similaridade e limita a 12
        ranked = sorted(movies_with_score, key=lambda x: x[1], reverse=True)
        result = [movie for movie, _ in ranked[:12]]

        # Fallback com busca fuzzy se nada for encontrado via embedding
        if not result:
            result = self.get_movie_by_name(movie_name)

        return result

