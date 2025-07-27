FROM python:3.12-slim

WORKDIR /oniria-back

RUN apt-get update && apt-get install -y build-essential libpq-dev curl

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=2.1.3 python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY . .

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "start"]

