FROM python:3.11-slim-buster AS requirements-stage

RUN apt-get update \ 
    && apt-get install -y \
        curl build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
RUN pip install poetry
COPY pyproject.toml poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11-slim-buster

WORKDIR /lab1
COPY --from=requirements-stage /tmp/requirements.txt /lab1/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /lab1/requirements.txt

COPY ./src /lab1/src
COPY ./tests /lab1/tests

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]








