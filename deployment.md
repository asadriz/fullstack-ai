# Separate Docker deployment methodology

The backend and frontend are intentionally independent deployments:

- `backend/` uses its existing `docker-compose.yml` and `start.sh`.
- `frontend/` is deployed by the Cloudflare project connected to the repository.
- There is no repository-root Compose stack and neither deployment starts the
  other.

This separation allows the API and web application to use different hosts,
release schedules, scaling policies, and rollback procedures.

## Backend deployment

### Services

The backend Compose project runs:

- Django/ASGI on port 8000
- Redis on port 6379
- a Celery worker
- Celery beat
- optional OnLogs on port 8798

The application database is selected by `DATABASE_URL`. SQLite is suitable for
local validation only. Use PostgreSQL for shared or production deployments.

### First deployment

Install Docker Engine, the Docker Compose v2 plugin, and Git. Clone the
repository and enter the backend directory:

```bash
git clone <repository-url>
cd <repository>/backend
cp .env.example .env
```

Set at least:

```dotenv
SECRET_KEY=<long-random-secret>
DEBUG=False
DATABASE_URL=postgres://<user>:<password>@<database-host>:5432/<database>
FRONTEND_URL=https://app.example.com
BACKEND_URL=https://api.example.com
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

Generate `SECRET_KEY` with:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

The PostgreSQL host must be reachable from Docker containers. Prefer a managed
database or a private-network hostname. Back up the database before deploying
migrations.

Run the existing deployment entrypoint:

```bash
./start.sh
```

The script:

1. requires `backend/.env`;
2. fast-forwards the current Git branch;
3. builds the existing backend image once;
4. applies migrations and collects static assets before application startup;
5. starts Django, Redis, Celery worker, and Celery beat;
6. prints the final Compose status.

Run OnLogs separately only when its Docker-socket access is explicitly
accepted:

```bash
docker compose up -d onlogs
```

Set `ONLOGS_ADMIN_USERNAME` and `ONLOGS_ADMIN_PASSWORD` in `.env` first. Do not
expose port 8798 publicly without authentication and firewall controls.

### Backend verification

```bash
docker compose ps
curl --fail --show-error http://127.0.0.1:8000/healthcheck/
```

The response must be:

```json
{"status":"OK"}
```

Verify the background-job path:

```bash
TASK_ID="$(curl --fail --silent --show-error \
  -H 'Content-Type: application/json' \
  -d '{"name":"deployment-check"}' \
  http://127.0.0.1:8000/api/jobs/trigger/ | \
  python3 -c 'import json,sys; print(json.load(sys.stdin)["data"]["task_id"])')"
sleep 2
curl --fail --show-error "http://127.0.0.1:8000/api/jobs/${TASK_ID}/"
```

The task status must be `SUCCESS`. Review logs for startup errors:

```bash
docker compose logs --since 10m backend celery-worker celery-beat redis
```

### Backend updates and rollback

Deploy an update from `backend/`:

```bash
git checkout <release-branch-or-tag>
./start.sh
```

`start.sh` only accepts a fast-forward pull. It exits instead of silently
creating a deployment merge commit.

To roll back:

1. restore the pre-deployment database backup if migrations are incompatible;
2. check out the previous release;
3. run `./start.sh`;
4. repeat the backend verification.

Do not run `docker compose down -v` unless deleting all Compose-managed data is
intentional.

## Frontend deployment through Cloudflare

The frontend is not a Docker service in this repository. Cloudflare owns its
build, edge runtime, TLS certificate, CDN, and custom domain.

In the Cloudflare project:

1. connect the Git repository and select the production branch;
2. set the project root to `frontend`;
3. use the project's supported Next.js build configuration;
4. set the build variable
   `NEXT_PUBLIC_BACKEND_URL=https://api.example.com`;
5. attach the frontend custom domain and deploy.

For a new Cloudflare Next.js project, use Cloudflare Workers with the current
OpenNext adapter. The older `@cloudflare/next-on-pages` adapter is deprecated.
Follow Cloudflare's current Next.js Workers guide rather than adding a frontend
container or host reverse proxy to this repository.

`NEXT_PUBLIC_BACKEND_URL` is embedded into the browser bundle during the
Cloudflare build. Changing it requires a new Cloudflare deployment.

After deployment, open `https://app.example.com/health` and select
**Check backend health**. It must return `{"status":"OK"}` from the separately
deployed backend.

Cloudflare provides frontend deployment history and rollback. Promote or roll
back the desired frontend deployment from the Cloudflare dashboard.

## Backend exposure

Cloudflare terminates frontend TLS and serves the frontend directly, so no
frontend host proxy is required. Expose the backend at the URL configured in
`BACKEND_URL` and `NEXT_PUBLIC_BACKEND_URL`, using the backend host's existing
ingress or a Cloudflare Tunnel if that is the chosen backend ingress.

Do not publicly expose Redis or OnLogs. Restrict ports 6379 and 8798 with host
and provider firewalls.

## Troubleshooting

### `./start.sh` reports that `.env` is missing

Run `cp .env.example .env`, configure all production values, and retry.

### A container repeatedly restarts

```bash
docker compose ps -a
docker compose logs <service>
```

Missing Django settings, an unreachable database, or migrations run after
Celery beat starts are common causes. The deployment script intentionally runs
migrations before starting the long-running services.

### Celery cannot reach Redis

```bash
docker compose exec redis redis-cli ping
docker compose logs celery-worker celery-beat
```

The Redis response must be `PONG`.

### The frontend calls the wrong API

Update `NEXT_PUBLIC_BACKEND_URL` in the Cloudflare build variables and trigger
a new deployment; changing a runtime variable does not rewrite an already-built
browser bundle.
