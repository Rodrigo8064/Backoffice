FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /backoffice

RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config installer.max-workers 10
RUN poetry install \
        --no-root \
        --no-ansi \
        --without dev

COPY . .

EXPOSE 8000
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000