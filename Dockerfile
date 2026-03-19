FROM python:3.13.6-slim

RUN pip install poetry

WORKDIR /code/

COPY ./pyproject.toml ./poetry.lock* /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY /app /code/app/

COPY ./alembic.ini /code/

COPY ./.env /code/

COPY ./scripts/start.sh /code/

RUN sed -i 's/\r$//' /code/start.sh && chmod +x /code/start.sh

ENV PYTHONPATH=/app

CMD ["/code/start.sh"]

