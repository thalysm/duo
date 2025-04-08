from core.database import get_collection
from rapidfuzz import fuzz

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
    

