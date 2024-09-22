# Use a imagem oficial do Python 3.11
FROM python:3.11-slim

# Definir diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo pyproject.toml e poetry.lock
COPY pyproject.toml poetry.lock* /app/

# Instalar o Poetry
RUN pip install poetry

# Instalar as dependências do projeto sem criar um ambiente virtual (porque o contêiner já é isolado)
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Copiar o código da aplicação para o diretório de trabalho
COPY . /app

# Expor a porta da API
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
