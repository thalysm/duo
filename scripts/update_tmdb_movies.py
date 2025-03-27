import requests
import gzip
import os
import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient
import concurrent.futures
from dotenv import load_dotenv
from core.database import get_collection

load_dotenv()

movies_collection = get_collection('movies')

# Conexão com o MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
API_TMDB = os.getenv("API_TMDB")
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
movies_collection = db['movies']  # Coleção onde os filmes serão atualizados

# Função para baixar os arquivos
def getIdTMDB():
    base_url = 'https://files.tmdb.org'
    path = '/p/exports/'
    
    # Pasta de destino para salvar os arquivos baixados
    current_date = (datetime.now() - timedelta(days=1)).strftime('%m_%d_%Y')
    output_folder = f'{current_date}'
    os.makedirs(output_folder, exist_ok=True)
    
    # Definir os itens que queremos baixar
    data_list = [
        {'Type': 'Movies', 'Link': f'movie_ids_{ current_date }.json.gz'}
    ]
    
    # Baixar o arquivo 'movies.json.gz'
    for entry in data_list:
        type_name = entry['Type']
        link = entry['Link']
        full_url = base_url + path + link
        output_path = os.path.join(output_folder, f"{type_name.lower().replace(' ', '_')}.json.gz")
        
        response = requests.get(full_url)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f'{type_name} baixado e salvo em {output_path}')
    
    return output_folder  # Retorna a pasta onde o arquivo foi salvo

# Função para descompactar e ler o arquivo movies.json
def process_movies_json(output_folder):
    movies_path = os.path.join(output_folder, 'movies.json.gz')
    
    # Descompactar o arquivo .gz
    with gzip.open(movies_path, 'rb') as f_in:
        with open(movies_path.replace('.gz', ''), 'wb') as f_out:
            f_out.write(f_in.read())
    
    # Ler o arquivo JSON descompactado
    movies_df = pd.read_json(movies_path.replace('.gz', ''), lines=True)
    
    return movies_df

# Função para atualizar o MongoDB para um filme específico
def update_movie(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    params = {'api_key': API_TMDB}
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            movie_data = response.json()
            
            # Usar o 'id' do TMDB para comparar e garantir que estamos atualizando corretamente
            movies_collection.update_one({'id': movie_data['id']}, {'$set': movie_data}, upsert=True)
            print(f"Filme {movie_data['title']} atualizado no MongoDB")
        else:
            print(f"Erro ao obter dados para o filme ID {movie_id}, Status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao processar o filme ID {movie_id}: {e}")

# Função para atualizar filmes em paralelo usando multithreading
def update_movies_in_mongo(df):
    movie_ids = df["id"].tolist()  # Extraindo os IDs dos filmes
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # Criando um pool de threads para atualizar os filmes
        executor.map(update_movie, movie_ids)  # Passa cada ID de filme para a função update_movie

# Função principal para coordenar o processo
output_folder = getIdTMDB()  # Baixar os arquivos
movies_df = process_movies_json(output_folder)  # Processar o arquivo movies.json
update_movies_in_mongo(movies_df)  # Atualizar os dados no MongoDB
