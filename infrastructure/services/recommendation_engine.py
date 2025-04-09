import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz
import random

class RecommendationEngine:
    def __init__(self):
        self.df = pd.read_csv("movies_processed.csv")
        self.matrix = load_npz("combined_matrix.npz")


    def recommend(self, user1_movie_ids, user2_movie_ids, top_n=5):
        # Junta todos os IDs
        selected_ids = user1_movie_ids + user2_movie_ids

        # Filtra pelos índices usando os IDs
        indices = self.df[self.df["id"].isin(selected_ids)].index.tolist()

        print("User 1:", user1_movie_ids, "User 2:", user2_movie_ids)
        if not indices:
            return []

        # Vetor médio do usuário
        user_vector = np.mean(self.matrix[indices], axis=0)
        user_vector = np.asarray(user_vector).flatten()

        # Similaridade com todos os filmes
        similarities = cosine_similarity([user_vector], self.matrix)[0]
        self.df["similarity"] = similarities

        # Remove os filmes que já foram assistidos pelos usuários
        unseen_df = self.df[~self.df["id"].isin(selected_ids)]

        # Top 50 mais similares
        top_candidates = unseen_df.sort_values(by="similarity", ascending=False).head(50)

        # Embaralha um pouco para variar as recomendações
        top_candidates = top_candidates.sample(frac=1.0, random_state=random.randint(0, 9999))

        # Seleciona os top_n finais
        recommendations = top_candidates.head(top_n)

        return recommendations[["original_title", "similarity", "id", "poster_path"]].to_dict(orient="records")


if __name__ == "__main__":
    engine = RecommendationEngine()
    user1_movies = ["Anora", "The Nice Guys","Cha Cha Real Smooth","Dune","The Banshees of Inisherin"]
    user2_movies = ["Interstellar", "Tenet","The Martian","The Dark Knight","Avengers: Endgame"]

    recommendations = engine.recommend(user1_movies, user2_movies)
    print(recommendations)
