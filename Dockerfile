FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="$PATH:/root/.local/bin" \
    TZ="Asia/Yekaterinburg"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry --version && \
    poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction --no-ansi

COPY ./ /app

CMD ["uvicorn", "main:app", "--port", "8000"]
