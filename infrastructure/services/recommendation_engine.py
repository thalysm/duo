import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz
import random

class RecommendationEngine:
    def __init__(self):
        self.df = pd.read_csv("movies_processed.csv")
        self.matrix = load_npz("combined_matrix.npz")


    def recommend(self, user1_movies, user2_movies, top_n=5):
        indices = self.df[self.df["original_title"].isin(user1_movies + user2_movies)].index.tolist()

        print(user1_movies, user2_movies)
        if not indices:
            return []

        user_vector = np.mean(self.matrix[indices], axis=0)
        user_vector = np.asarray(user_vector).flatten()

        similarities = cosine_similarity([user_vector], self.matrix)[0]
        self.df["similarity"] = similarities

        # Remove os filmes já vistos
        unseen_df = self.df[~self.df["original_title"].isin(user1_movies + user2_movies)]

        # Pega os top 25 mais similares
        top_candidates = unseen_df.sort_values(by="similarity", ascending=False).head(50)

        # Embaralha levemente
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
