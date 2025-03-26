from infrastructure.repositories.movie_repository import MovieRepository

class GetMoviesUseCase:
    def __init__(self, repository: MovieRepository):
        self.repository = repository

    def execute(self):
        return self.repository.get_all_movies()
