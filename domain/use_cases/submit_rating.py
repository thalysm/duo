from domain.entities.rating import Rating
from infrastructure.repositories.rating_repository import RatingRepository

class SubmitRatingUseCase:
    def __init__(self, repository: RatingRepository):
        self.repository = repository

    def execute(self, rating: Rating):
        return self.repository.save_rating(rating)
