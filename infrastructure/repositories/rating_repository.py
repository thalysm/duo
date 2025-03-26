from core.database import get_collection

class RatingRepository:
    def __init__(self):
        self.collection = get_collection("ratings")

    def add_rating(self, rating_data: dict):
        self.collection.insert_one(rating_data)
        return {"message": "Rating added successfully"}

    def get_ratings_for_movie(self, movie_id: int):
        return list(self.collection.find({"movie_id": movie_id}, {"_id": 0}))

    def get_user_ratings(self, user_id: str):
        return list(self.collection.find({"user_id": user_id}, {"_id": 0}))
