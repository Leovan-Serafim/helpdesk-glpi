# Copilot / AI agent instructions — helpdesk-glpi

Purpose: give AI coding agents the minimal, actionable knowledge to be productive in this repository.

- **Big picture**: The project is a thin React frontend + FastAPI Python backend that acts as a middleware for GLPI. The backend (in `backend/`) hosts templates and static files, exposes endpoints in [backend/main.py](backend/main.py), and runs an analytics pipeline before calling an LLM. The analytics orchestrator is `InsightEngine.run()` in [backend/analytics/insight_engine2.py](backend/analytics/insight_engine2.py).

- **Where to start**: open [backend/main.py](backend/main.py) — it shows the request flow: HTTP → DB read (`database/config.py` → `get_db_connection()` in [backend/db_connection.py](backend/db_connection.py)) → analytics (`backend/analytics/*`) → prompt construction → LLM client (`backend/attendance/llm_client.py`).

- **Key files and responsibilities**:
  - [backend/main.py](backend/main.py): FastAPI app, routes `/`, `/ask`, `/chamados` and prompt rules in `/ask`.
  - [backend/attendance/llm_client.py](backend/attendance/llm_client.py): centralized LLM calls (Ollama by default). Use this client instead of ad-hoc requests.
  - [backend/analytics/insight_engine2.py](backend/analytics/insight_engine2.py): orchestrates historical analysis -> returns `decision_object` used in prompts.
  - [backend/database/config.py](backend/database/config.py): defines `DB_PATH` (SQLite `mock_glpi.db`).
  - [backend/recriar_banco.bat](backend/recriar_banco.bat): Windows helper that recreates DB, seeds data, and runs extraction.
  - `templates/` and `static/`: Jinja2 templates and static assets mounted by FastAPI.

- **Development workflows**:
  - Dev server (from `backend/`): run the included script or the uvicorn command:

```powershell
cd backend
python -m uvicorn main:app --reload
# or double-click start_serve.bat on Windows
```

  - Recreate local DB and seed mock data (Windows): run `backend/recriar_banco.bat`. Equivalent Python steps are also present in the script (create tables, `python -m database.seed`, `python -m extraction.run_extraction`).

  - LLM requirement: the code expects an Ollama-like HTTP API at `http://localhost:11434/api/generate`. Start your LLM server before calling `/ask` (example: `ollama serve`). `LLMClient` default model is `mistral`.

- **Testing**: tests live under `backend/tests/` (e.g. `test_phase5.py`) and use the analytics and responder flows. Run tests from repository root or `backend/` with `pytest`:

```bash
cd backend
pytest -q
```

- **Project-specific conventions**:
  - Analytics pipeline returns a `decision_object` dictionary; tests and the LLM prompt expect its shape (see `insight_engine2.py`). Preserve keys like `status`, `priority`, `suggested_actions`, and `insights` when modifying outputs.
  - Prompting rules are enforced in `main.py`: the deployed prompt explicitly instructs the LLM to `USE ONLY the provided data`, answer in Portuguese, and be concise. When altering prompt composition, keep these constraints.
  - Use the central `LLMClient.generate()` for all model calls to keep retry/timeout behavior consistent.

- **Common edits an AI may be asked to perform**:
  - Add endpoint: follow pattern in [backend/main.py](backend/main.py), use `get_db_connection()` for DB access, and return `JSONResponse` on errors.
  - Extend analytics: add helpers under `backend/analytics/` and return enrichments inside `insight_engine2.py` final object.
  - Template changes: update `templates/index.html` or `templates/chamados.html` and keep field names same as produced by queries in `main.py`.

- **Integration and boundaries**:
  - External systems: GLPI data is mocked into `mock_glpi.db` and read by `extraction/run_extraction.py` and `extraction/glpi_reader.py`.
  - LLM: external HTTP service (Ollama) — network failures surface as exceptions from `LLMClient`; prefer graceful error messages like those already in `main.py`.

- **What NOT to change without careful review**:
  - `LLMClient` retry/timeouts and endpoint defaults — changing these affects UX and tests.
  - The shape of `decision_object` returned by `InsightEngine.run()` — many components and tests rely on those keys.

If anything here is unclear or you'd like me to expand examples (for example: a small PR that changes the prompt safely, or an example unit test), tell me which area to iterate on.
