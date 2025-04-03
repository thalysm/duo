import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from scipy.sparse import hstack, save_npz
import scipy.sparse

from core.database import get_collection  

class ProcessMoviesUseCase:
    @staticmethod
    def execute():
        collection = get_collection("movies")  
        
        cursor = collection.find(
            {
                "status": "Released",
                "vote_average": {"$ne": 0},
                "vote_count": {"$gte": 100},
                "popularity": {"$gte": 2},
                "runtime": {"$ne": 0}
            },
            {
                "id": 1, "original_title": 1, "overview": 1, "genres": 1, "title":1,
                "original_language": 1, "popularity": 1,"poster_path":1,
                "production_companies": 1, "release_date": 1
            }
        )

        df = pd.DataFrame(list(cursor))

        # Preenchendo valores nulos
        df["overview"] = df["overview"].fillna("")
        df["genres"] = df["genres"].apply(lambda x: " ".join([g["name"] for g in x]) if isinstance(x, list) else "Unknown")
        df["original_language"] = df["original_language"].fillna("unknown")
        df["popularity"] = df["popularity"].fillna(0)
        df["production_companies"] = df["production_companies"].apply(lambda x: " ".join([g["name"] for g in x]) if isinstance(x, list) else "Unknown")
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year.fillna(0).astype(int)

        # Vetorização com TF-IDF
        tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
        tfidf_matrix = tfidf.fit_transform(df["overview"])

        tfidf_genres = TfidfVectorizer()
        genres_matrix = tfidf_genres.fit_transform(df["genres"])

        tfidf_companies = TfidfVectorizer()
        companies_matrix = tfidf_companies.fit_transform(df["production_companies"])

        # One-Hot Encoding para idioma
        encoder = OneHotEncoder(sparse_output=False)
        languages_encoded = encoder.fit_transform(df[["original_language"]])

        # Normalização
        scaler = MinMaxScaler()
        popularity_normalized = scaler.fit_transform(df[["popularity"]])
        release_date_normalized = scaler.fit_transform(df[["release_date"]])

        # Combinação das features em uma matriz final
        combined_matrix = hstack((
            tfidf_matrix,
            genres_matrix,
            companies_matrix,
            scipy.sparse.csr_matrix(languages_encoded),
            scipy.sparse.csr_matrix(popularity_normalized),
            scipy.sparse.csr_matrix(release_date_normalized),
        ))

        # Salvando arquivos processados
        save_npz("combined_matrix.npz", combined_matrix)
        df.to_csv("movies_processed.csv", index=False)

        print(f"Treinamento concluído! {len(df)} filmes/séries processados.")
