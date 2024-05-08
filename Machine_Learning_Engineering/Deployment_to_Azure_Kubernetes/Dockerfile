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

WORKDIR /lab4
COPY --from=requirements-stage /tmp/requirements.txt /lab4/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /lab4/requirements.txt

COPY ./src /lab4/src
COPY ./tests /lab4/tests
COPY ./model_pipeline.pkl /lab4/model_pipeline.pkl

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "httpx", "http://localhost:8000/health"]


