# Nested Tags Tree — Backend

FastAPI service that stores **recursive tag trees** in PostgreSQL. Each tree is JSON: nodes have a `name`, and either `data` (leaf) or `children` (branch), validated with Pydantic.

## Features

- **REST API** for trees: list (`GET /trees`), create (`POST /trees`), update (`PUT /trees/{id}`).
- **JSON persistence**: tree payloads stored as JSON in the database; responses include `id` and `tree`.
- **Schema validation**: recursive `Tag` model ensures each node is a leaf (`data`) or a branch (`children`), not both and not neither.
- **Automatic tables**: SQLAlchemy creates tables on application startup.
- **Health check**: `GET /health` returns `{"status": "ok"}`.
- **CORS**: configured for broad browser access (wildcard origins; suitable when not using cookie credentials).

## Requirements

- Python 3.12+ (3.14 supported with pinned dependencies in `requirements.txt`).
- PostgreSQL reachable with a URL you put in `DATABASE_URL`.

## Configuration

Copy `.env.example` to `.env` and set the database URL:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

`app.config.Settings` reads `DATABASE_URL` (via the `database_url` field).

## How to run (local)

From this directory (`backend/`):

```bash
python -m venv .venv
```

Activate the virtual environment (Windows PowerShell: `.venv\Scripts\Activate.ps1`; Git Bash: `source .venv/Scripts/activate`), then:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- API base: `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

## Production (e.g. Render)

Use a process that binds to all interfaces and the platform port (no `--reload`):

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set the service **root directory** to `backend` if the repo root is the monorepo, and configure `DATABASE_URL` to your hosted PostgreSQL instance.

## API summary

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness |
| `GET` | `/trees` | List all trees |
| `POST` | `/trees` | Body: `{"tree": { ... }}` — create |
| `PUT` | `/trees/{tree_id}` | Body: `{"tree": { ... }}` — update |

Tree shape (conceptually): `{ "name": "...", "data": "..." }` or `{ "name": "...", "children": [ ... ] }`.
