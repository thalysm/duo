from domain.use_cases.process_movies import ProcessMoviesUseCase

class MovieService:
    @staticmethod
    def update_movies():
        ProcessMoviesUseCase.execute()
        return {"message": "Processamento iniciado!"}
