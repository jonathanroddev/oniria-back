# 🧙 Oniria Backend

Backend for the **Oniria** project built with **FastAPI**, following **Hexagonal Architecture**, and configured for both local development and production deployment using **Poetry**, **Docker**, and **PostgreSQL**.

---

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)
- [Black](https://black.readthedocs.io/)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-user/oniria-backend.git
cd oniria-backend
```

### 2. Install dependencies with Poetry

```bash
poetry install
```

### 3. Create a `.env` file

Use `.env.example` as a reference:

```bash
cp .env.example .env
```

---

## 🐳 Local Development (with database)

The local dev setup uses **Docker Compose** to run both the FastAPI app and a PostgreSQL database.

```bash
docker-compose up --build
```

This will:

- Start FastAPI at http://localhost:8000
- Start a local PostgreSQL instance at port 5432

🧪 You can test DB connectivity using `psql` or a GUI like DBeaver or PGAdmin.

---

## 🧪 Local Dev (only PostgreSQL container)

If you are developing with Poetry on host and only want the **database container**:

```bash
docker-compose up -d db
```

Then run your app via:

```bash
poetry run dev
```

or

```bash
RELOAD=true poetry run start
```

---

## 🔧 Available Scripts

Defined in `pyproject.toml`:

```toml
[tool.poetry.scripts]
start = "oniria.__main__:start"
dev = "oniria.__main__:dev"
prod = "oniria.__main__:prod"
```

You can run:

```bash
poetry run start    # Honor env vars like HOST, PORT, RELOAD
poetry run dev      # Run with reload=True
poetry run prod     # Run in production mode
```

Set env variables if needed:

```bash
# Unix/macOS
HOST=0.0.0.0 PORT=9000 RELOAD=true poetry run start

# Windows PowerShell
$env:HOST="0.0.0.0"; $env:PORT="9000"; $env:RELOAD="true"; poetry run start
```

---

## 🧼 Code Quality

Run the following tools to maintain formatting and typing:

```bash
poetry run black .
```

We recommend setting up pre-commit hooks using [pre-commit](https://pre-commit.com/).

---

## 🐘 Production Deployment

For production (e.g., Railway, Render, Fly.io):

- Use only the **Dockerfile**
- Or the minimal `docker-compose.yml` (without override)
- Set `DATABASE_URL` in the deployment environment (from Railway)

Build and run:

```bash
docker build -t oniria-app .
docker run -e DATABASE_URL=your-db-url -p 8000:8000 oniria-app
```

---

## ☁️ Railway Deployment

1. Create a new **service** with the GitHub repo
2. Add a **PostgreSQL plugin** via Railway dashboard
3. Set the `DATABASE_URL` variable in Railway (auto-generated from plugin)
4. Railway will auto-build from your Dockerfile and expose it on a URL

❗ You **do not** need the PostgreSQL container in production (do not include the `override`).

---

## 🧾 docker-compose.override.yml Notes

This file is:

- Meant **only for local development**
- Used to **add a PostgreSQL container**
- Automatically picked up by Docker Compose when running locally

### Should I include it in production?

No. **Never include `docker-compose.override.yml` when deploying**.

Use only:

```bash
docker-compose -f docker-compose.yml up --build
```

If needed, you can:

- `.gitignore` it to keep it personal, or
- Keep it versioned with clear documentation that it’s for dev only

---

## 🧱 Dockerfiles and Compose

### Dockerfile

```Dockerfile
FROM python:3.12-slim

WORKDIR /oniria-back

RUN apt-get update && apt-get install -y build-essential libpq-dev curl

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=2.1.3 python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY . .

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "start"]
```

---

### docker-compose.yml (production safe)

```yaml
version: '3.9'

services:
  web:
    build: .
    env_file:
      - .env
    ports:
      - "8000:8000"
    restart: unless-stopped
```

---

### docker-compose.override.yml (local only)

```yaml
version: '3.9'

services:
  db:
    image: postgres:17
    container_name: oniria_db
    environment:
      POSTGRES_USER: devuser
      POSTGRES_PASSWORD: devpass
      POSTGRES_DB: devdb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  web:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql+psycopg2://devuser:devpass@db:5432/devdb
      DB_HOST: db
      HOST: 0.0.0.0
      PORT: 8000
      RELOAD: "true"
    depends_on:
      - db
    ports:
      - "8000:8000"
    volumes:
      - ./:/oniria-back

volumes:
  pgdata:
```

---

### `.env.example`

```env
# For development (override.yml)
POSTGRES_USER=devuser
POSTGRES_PASSWORD=devpass
POSTGRES_DB=devdb
DB_HOST=localhost
DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DB_HOST}:5432/${POSTGRES_DB}
```

---

## 📂 Project Structure (Hexagonal Architecture)

```
oniria/
├── auth/
    ├── domain/
    ├── application/
    ├── infrastructure/
    ├── interfaces/
├── db/
├── __main__.py
```

Routers are loaded modularly and mounted in `__main__.py` based on the hexagonal architecture.

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feat/my-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feat/my-feature`)
5. Open a Pull Request

---

## 🧪 Testing (Coming Soon)

Unit and integration tests will be added with `pytest`.

---

## 📜 License

MIT