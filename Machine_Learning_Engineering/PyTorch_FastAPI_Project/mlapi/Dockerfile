FROM python:3.11-slim-buster AS requirements-stage

RUN apt-get update \
    && apt-get install -y \
         curl \
         build-essential \
         libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
RUN pip install poetry
COPY pyproject.toml poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim-buster

WORKDIR /mlapi
COPY --from=requirements-stage /tmp/requirements.txt /mlapi/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /mlapi/requirements.txt

COPY ./src /mlapi/src
COPY ./tests /mlapi/tests
COPY ./distilbert-base-uncased-finetuned-sst2 /mlapi/distilbert-base-uncased-finetuned-sst2

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]