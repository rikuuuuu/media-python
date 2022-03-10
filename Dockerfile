FROM python:3.9 as build

WORKDIR /app

EXPOSE 80

COPY ./pyproject.toml ./poetry.lock ./

# Install Python Packages via Poetry
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-root

FROM tiangolo/uvicorn-gunicorn:python3.9-slim

RUN apt-get update && apt-get install -y automake make bash git curl sudo libmariadb-dev libpq-dev default-libmysqlclient-dev

COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY ./.env.* /app/
COPY ./.env /app/
COPY ./app /app/app
# COPY ./prestart.sh /app/prestart.sh

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
