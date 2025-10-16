# `python-base` configura todas as variáveis de ambiente compartilhadas
FROM python:3.13.1-slim AS python-base

    # python
ENV PYTHONUNBUFFERED=1 \
    # impede que o Python crie arquivos .pyc
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    # desativa o cache do pip
    PIP_NO_CACHE_DIR=off \
    # desativa a verificação de versão do pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    # define o tempo limite padrão das operações do pip
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=2.1.4 \
    # define o local onde o poetry será instalado
    POETRY_HOME="/opt/poetry" \
    # faz o poetry criar o ambiente virtual dentro do diretório do projeto
    # o ambiente virtual será nomeado `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # impede que o poetry faça perguntas interativas
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # define onde ficarão as dependências e o ambiente virtual
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


# adiciona o poetry e o ambiente virtual ao PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # dependências necessárias para instalar o poetry
        curl \
        # dependências para compilar pacotes Python nativos
        build-essential

# instala o poetry — respeita as variáveis $POETRY_VERSION e $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    # instala o driver psycopg2 (PostgreSQL) via pip
    && pip install psycopg2

# copia os arquivos de dependências do projeto para garantir cache nas builds
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# instalação mais rápida, pois dependências de runtime já estão instaladas
RUN poetry install --no-root

# define o diretório de trabalho principal da aplicação
WORKDIR /app

# copia o restante do código do projeto para dentro do container
COPY . /app/

# expõe a porta 8000 (onde o servidor rodará)
EXPOSE 8000

# comando padrão que roda o servidor Django no container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
