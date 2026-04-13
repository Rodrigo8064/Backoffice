#!/bin/sh

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Iniciando aplicação..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "► Aplicando migrations..."
python manage.py migrate --noinput

echo "► Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Iniciando Gunicorn..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exec gunicorn app.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --threads 2 \
    --access-logfile - \
    --error-logfile - \
    --timeout 120