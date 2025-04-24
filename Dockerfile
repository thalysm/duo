# Imagem base
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia requirements.txt e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Copia o .env (caso precise acessar dentro do container)
COPY .env .env

# Expõe a porta da API
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
