# Guidance for AI coding agents working on this repo

This file documents the concrete, discoverable patterns and workflows an AI assistant should follow to be productive in this project.

1. Big picture
- **Architecture**: Frontend (Flask) in `frontend/`, API Gateway (FastAPI) in `api-gateway/`, and multiple microservices (FastAPI) under `services/`.
- **Service boundaries**: Each microservice is self-contained in `services/<name>/` and normally exposes a `main.py`, `Dockerfile`, and `requirements.txt`.
- **Data flows**: Frontend calls the API Gateway (`API_GATEWAY_URL`). The gateway forwards requests to services using the `SERVICES` mapping in `api-gateway/main.py`. Services may call other services using `requests` or utilities in `common/helpers/utils.py`.

2. How the repo expects things to be wired (concrete rules)
- **Environment**: Copy `.env.example` to `.env` and set values. The repo uses `common/config.py` (`settings`) to centralize env access.
- **Service naming and docker-compose**: Container/service names in `docker-compose.yml` must match the names used by the gateway (e.g., `auth-service:8001`). If you add/rename a service, update `api-gateway/main.py` `SERVICES` and `docker-compose.yml`.
- **Health endpoints**: Each service should provide a `/health` endpoint (used in examples and for quick checks). The gateway also exposes `/health`.
- **Inter-service calls**: Use `requests` or `common/helpers/utils.py:send_request_to_service`. Example: `requests.get(f"{SERVICES['auth']}/health")` or `send_request_to_service(url)`.

3. Common code patterns to follow (examples)
- **Config access**: Import `from common.config import settings` and use `settings.API_GATEWAY_URL` rather than hardcoding URLs.
- **Gateway forwarding**: The gateway exposes generic routes in `api-gateway/main.py`:
  - `GET /api/v1/{service}/{path}` forwards to the service URL defined in `SERVICES`.
  - `POST /api/v1/{service}/{path}` forwards JSON bodies.
  Example: `GET /api/v1/auth/health` → forwards to `http://auth-service:8001/health`.
- **Service layout**: Services usually include DB helpers: `database_sql.py` uses `DATABASE_URL` from env and `SessionLocal` pattern. When adding DB models, expose `Base` in `models.py` and call `create_db_and_tables()` from a startup task if needed.

4. Run & debug (practical commands)
- Full stack (builds images and starts everything):
  ```bash
  cp .env.example .env
  docker-compose up --build
  ```
- Run a single FastAPI service locally (example for `authentication`):
  ```bash
  cd services/authentication
  uvicorn main:app --reload --host 0.0.0.0 --port 8001
  ```
- Run the frontend locally:
  ```bash
  cd frontend
  python app.py
  ```

5. Repo-specific conventions and TODO signals
- Many files include `# TODO` comments. Treat these as high-value guidance for what students expect the code to implement. Examples: `services/service1/main.py`, `common/config.py`.
- Naming: microservice directories are `service1`, `service2`, `service3` in the template — real projects should rename them to domain-specific names but maintain docker-compose/service identifiers.
- Ports: Example ports are in comments (e.g., `auth-service:8001`); keep explicit container ports stable so `docker-compose.yml` routing works.

6. Safety and non-goals
- Do not add secrets into the repo. If adding example secrets for documentation, mark them as placeholders and recommend setting them in `.env`.
- Do not assume databases are present unless `docker-compose.yml` defines them; prefer guarding DB connections with presence checks and clear error messages.

7. Places to look for authoritative examples
- High-level project description: `README.md` (root).
- Shared config and helpers: `common/config.py`, `common/helpers/utils.py`.
- Gateway forwarding: `api-gateway/main.py`.
- Frontend expectations: `frontend/app.py` (uses `API_GATEWAY_URL`).
- Service template examples: `services/service1/`, `services/authentication/`, including `database_sql.py` and `main.py`.

If anything in this summary is unclear or you want additional examples (e.g., a sample endpoint implementation or a suggested test workflow), tell me which area to expand and I will iterate.
