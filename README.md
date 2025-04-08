# Duo

Duo é uma API para recomendação de filmes baseada em Machine Learning.

## 🚀 Tecnologias Utilizadas

- **Python 3.9+**
- **FastAPI** - Framework web para a API
- **Uvicorn** - Servidor ASGI para rodar a API
- **MongoDB** - Banco de dados para armazenar os filmes
- **Pandas, NumPy, Scikit-learn, SciPy** - Para processamento dos dados



## ⚡ Como Rodar a API

### 1️⃣ Clonar o Repositório
```bash
git clone https://github.com/thalysm/duo
cd duo
```

### 2️⃣ Criar um Ambiente Virtual e Instalar Dependências
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3️⃣ Configurar as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto e defina as variáveis:
```env
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=duo
API_TMDB= https://www.themoviedb.org/settings/api
```

### 4️⃣ Rodar a API
```bash
uvicorn main:app --reload
```
A API estará rodando em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🔥 Endpoints Disponíveis

### 🎬 Filmes
- **`GET /movies/movies`** - Retorna a lista de filmes
- **`GET /movies/movies/{id}`** - Retorna um filme específico
- **`GET /movies/movies/name/{movie_name}`** - Retorna um filme pelo nome

### 🔄 Processamento
- **`POST /process/update_movies`** - Processa os filmes para recomendação

### 🍿 Recomendação
- **`POST /recommendations/recommend`** - Gera a recomendação dos filmes

### ⭐ Avaliações
- **`POST /ratings/ratings`** - Processa a avaliação da recomendação
- **`GET /ratings/ratings/movie/{movie_id}`** - Processa a avaliação da recomendação

### 🤖 Scripts
- **`Update TMDB movies`** - Baixa arquivo movies.json que contem ID e Nome dos filmes. Utiliza o movies.json para atualizar o banco de dados.
- **`Gerar title embedding`** - Percorre o banco para gerar o title_embeding baseado no overview e generos. (melhorar a busca)

## 📌 Contribuição
Se quiser contribuir, faça um fork, crie uma branch e envie um pull request! 😊

## 📝 Licença
Este projeto está sob a licença MIT.

