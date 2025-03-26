from core.database import get_collection

class MovieRepository:
    def __init__(self):
        self.collection = get_collection("movies")

    def get_all_movies(self, limit=50):
        movies = self.collection.find({}, {"_id": 0}).limit(limit)
        return list(movies)

    def get_movie_by_id(self, movie_id: int):
        return self.collection.find_one({"id": movie_id}, {"_id": 0})
    
    def get_movie_by_name(self, movie_name: str):
        return self.collection.find_one({"title": movie_name}, {"_id": 0})
