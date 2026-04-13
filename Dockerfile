FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /backoffice

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip poetry gunicorn

COPY pyproject.toml poetry.lock ./

RUN poetry config installer.max-workers 10
RUN poetry install \
        --no-root \
        --no-ansi \
        --without dev

COPY . .

RUN chmod +x entrypoint.sh
EXPOSE 8000
CMD ["./entrypoint.sh"]