# minimal-layered-app

Minimal layered architecture demo: FastAPI + Streamlit + SQL.

## Install required packages

```bash
uv sync --project backend
uv sync --project frontend
```

## Launch applications

Open two terminals:

- Backend FastApi: `uv run --project backend python backend/src/main.py`
- Frontend Streamlit: `cd frontend` and `uv run --project . streamlit run src/app.py`

## Urls

- Backend: <http://localhost:5000>
- Frontend: <http://localhost:8000>