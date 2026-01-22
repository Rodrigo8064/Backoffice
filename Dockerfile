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

EXPOSE 8000
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--access-logfile", "-"]