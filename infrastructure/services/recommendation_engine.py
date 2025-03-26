import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz

class RecommendationEngine:
    def __init__(self):
        self.df = pd.read_csv("movies_processed.csv")
        self.matrix = load_npz("combined_matrix.npz")

    def recommend(self, user1_movies, user2_movies, top_n=10):
        indices = self.df[self.df["title"].isin(user1_movies + user2_movies)].index.tolist()

        print(user1_movies,user2_movies)
        if not indices:
            return []

        user_vector = np.mean(self.matrix[indices], axis=0)
        user_vector = np.asarray(user_vector).flatten()

        similarities = cosine_similarity([user_vector], self.matrix)[0]
        self.df["similarity"] = similarities

        recommendations = self.df[~self.df["title"].isin(user1_movies + user2_movies)].sort_values(by="similarity", ascending=False).head(top_n)

        return recommendations[["title", "similarity"]].to_dict(orient="records")

if __name__ == "__main__":
    engine = RecommendationEngine()
    user1_movies = ["Anora", "The Nice Guys","Cha Cha Real Smooth","Dune","The Banshees of Inisherin"]
    user2_movies = ["Interstellar", "Tenet","The Martian","The Dark Knight","Avengers: Endgame"]

    recommendations = engine.recommend(user1_movies, user2_movies)
    print(recommendations)
