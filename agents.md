AGENTS.md file

## Repository layout
The repository has two top-level application folders:
- `backend/` contains the Django REST Framework backend.
- `frontend/` contains the Next.js React frontend.

## Dev environment tips
Run backend commands from `backend/` and frontend commands from `frontend/`.

Run backend tests through the active interpreter to avoid global pytest/plugin conflicts:
`cd backend && python -m pytest -vv`

Run a specific backend test file:
`cd backend && python -m pytest -vv apps/PATH_TO_TEST_FILE`

## Coding instructions
- Use `snake_case` for variables and functions.
- Keep code focused, readable, and consistent with the surrounding app.
- Put business logic and database access in service classes or service functions, not in API views or Celery tasks.
- If a user supplies a durable repository-specific rule, update this `agents.md`.

## Backend feature implementation rules

### 1. Classify the request before implementing it
Every backend feature must first be classified as either synchronous or background work.

Use a synchronous request when the API can promptly return the completed result. Typical examples are database reads, filtering, pagination, and small database writes. The API view validates the request and permissions, calls a service, and returns the service result.

Use a background request when the work can exceed a normal HTTP request window (roughly 20–30 seconds), calls several or slow external APIs, performs substantial processing, or needs retries independent of the client connection. Do not keep an HTTP request open for work that may take minutes.

When uncertain, consider expected and worst-case latency, external API reliability, retry requirements, and whether the caller needs the final result immediately. Do not classify work as background merely because it calls one external API if it reliably completes within the synchronous request budget.

### 2. Follow the required control flow
Synchronous flow:
1. The API view authenticates and authorizes the caller.
2. A serializer validates all inputs.
3. The view calls a service class or service function.
4. The service performs business logic and ORM access.
5. The view serializes and returns the result in the standard response envelope.

Background flow:
1. The API view authenticates and authorizes the caller and validates the input.
2. The service creates any required domain or job record.
3. The API enqueues a task from the app's `tasks.py`.
4. The API immediately returns HTTP `202 Accepted` with a stable task/job or object ID and the initial status.
5. The Celery task calls the service layer to do the actual work; business logic must not live in the task.
6. A protected status/detail API lets the caller retrieve progress and the final result using the returned ID.

Background jobs should be idempotent where practical. Define retry behavior for transient failures, store useful status/error information, and ensure callers can only access jobs they are authorized to see.

### 3. Keep API contracts consistent and documented
- Keep views thin: authentication, authorization, validation, service invocation, and response construction only.
- Return API payloads through `APIResponse.get_response` from `utils.response.resp`; use the appropriate HTTP status on DRF's `Response`.
- Use serializers for request validation and explicit response shapes rather than undocumented dictionaries.
- Document every endpoint in Swagger/OpenAPI. Its operation description must explain what the endpoint does, authentication requirements, important side effects, whether processing is synchronous or queued, and how a background result is retrieved.
- Document request bodies, path/query parameters, response serializers, and important success and error status codes so a caller can understand the contract without reading the implementation.

### 4. Secure endpoints by default
The project-wide default is `IsAuthenticated`. Add narrower object, role, or staff permissions where the feature requires them.

Use `AllowAny` only when anonymous access is a deliberate product requirement, such as login, signup, health checks, or a verified third-party webhook. Document why the endpoint is public and add the applicable protection (for example throttling, signature validation, or strict input validation). Never make job submission, job status, or user data endpoints public by convenience.

### 5. Design ORM access to avoid N+1 queries
- Use `select_related` for foreign-key and one-to-one relationships.
- Use `prefetch_related` (and `Prefetch` when filtering is needed) for reverse and many-to-many relationships.
- Prefer database filtering, aggregation, and annotation over per-row Python queries.
- Paginate collection endpoints and avoid loading unbounded querysets.
- For query-sensitive code, add a query-count test or otherwise verify that query count does not grow once per returned row.

### 6. Let Django generate migrations
When a model changes, generate migrations with Django's `manage.py makemigrations` command and inspect the generated migration. Never hand-write or fabricate a migration file. Apply migrations with `manage.py migrate` when validating the real database flow, and commit the generated migration with the model change.

### 7. Test every backend change
- Add readable tests whose names state the behavior being verified and whose arrange/act/assert flow is easy to follow.
- Test service business logic independently, including validation and failure cases.
- Test the complete API flow: authentication/permissions, validation, response envelope, HTTP status, and persisted result.
- For background features, test submission, returned job ID, service invocation by the task, status polling, success, and failure behavior.
- Mock external APIs in unit tests. Test retry/error handling explicitly.
- Add regression tests for fixes and query-count tests for N+1 risks.
- Keep test files focused, with no more than five tests per file; split larger suites by behavior.
- Run the relevant tests while developing, then run the full backend suite to detect regressions.
- Maintain at least 90% coverage for new or changed backend code. Use `python -m pytest --cov=apps --cov=utils --cov-report=term-missing` to find untested paths; coverage percentage does not replace meaningful assertions.

## Cursor Cloud specific instructions
This is a **Django REST Framework backend boilerplate** (project package `core`, apps under `backend/apps/`) plus a **Next.js React frontend** under `frontend/`. The backend intentionally ships with only two apps: `apps/users` (custom `User` + `Organization` models and admin APIs) and `apps/authentications` (JWT signup/login/password endpoints). Everything else is generic infra under `utils/` and `core/`. Build new backend features by adding apps (see below). The startup update script creates/refreshes the backend `venv` and installs `backend/requirements.txt`; use that interpreter directly (`backend/venv/bin/python`, `backend/venv/bin/ruff`, `backend/venv/bin/pytest`). The conda instructions above are for the original author's Mac and do not apply here.

- Env vars: `backend/core/settings.py` reads `backend/.env` (via `django-environ`). Required with no default: `SECRET_KEY`, `DATABASE_URL`, `FRONTEND_URL`, `BACKEND_URL`. A local `.env` (SQLite + dev values) may exist in the workspace snapshot; if it is ever missing, `cd backend && cp .env.example .env`. Without `.env`, even `manage.py`/`pytest` fail to import settings.
- Database: `backend/.env` points `DATABASE_URL` at local SQLite (`db.sqlite3`) for dev. Run `cd backend && ./venv/bin/python manage.py migrate` after first setup.
- Run backend server: `cd backend && ./venv/bin/python manage.py runserver 0.0.0.0:8000`. Health: `GET /healthcheck/` -> `{"status":"OK"}`. Swagger UI at `/docs/` requires an admin session (login via `/admin/`) since it uses `IsAdminUser`.
- Run frontend server: `cd frontend && npm run dev`. The frontend defaults to `NEXT_PUBLIC_BACKEND_URL=http://localhost:8000` and includes `/login`, `/signup`, and `/health`.
- Auth: JWT via `/auth/token/` (body `{"email","password"}`) and `/auth/signup/`. User/org admin APIs under `/api/admin/...` require `is_staff`. `AUTH_USER_MODEL` is `users.User` (email is the login field; `createsuperuser` has no `--name` arg, so create staff users via shell if needed).
- Backend tests: `cd backend && ./venv/bin/python -m pytest` (settings module `unit_test_settings`, forces SQLite + `--nomigrations`). Backend lint: `cd backend && ./venv/bin/ruff check .`; format check: `cd backend && ./venv/bin/black .`.
- Frontend checks: `cd frontend && npm run lint` and `cd frontend && npm run build`.
- Deployment: backend and frontend deploy independently. Run `backend/start.sh` from `backend/` for the existing backend Compose workflow; Cloudflare builds and serves `frontend/`. Follow root `deployment.md`; do not introduce a coupled root Compose stack or a frontend container.
- Celery/Redis: `backend/docker-compose.yml` runs Redis, Celery worker, and Celery beat; they are not required for the HTTP API or tests (tests run Celery eagerly). `core/celery.py` has an empty `beat_schedule` — add periodic tasks there as apps are created.
- Adding apps: use the `conf/app_template` scaffold — `mkdir apps/<name> && ./venv/bin/python manage.py startapp <name> apps/<name> --template conf/app_template --extension py`. Then add `"apps.<name>"` to `LOCAL_APPS` in `core/settings.py` and wire routes into `api_urlpatterns` in `core/urls.py`.