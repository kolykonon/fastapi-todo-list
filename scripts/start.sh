#!/bin/bash
set -e

echo "================================="
echo "Запуск миграций"
echo "================================="
alembic revision --autogenerate -m 'Initial'
alembic upgrade head

echo "================================="
echo "Запуск приложения"
echo "================================="
exec uvicorn app.main:app --host 0.0.0.0 --port 8000