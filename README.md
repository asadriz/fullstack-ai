# Full Stack Boilerplate

This repository is organized as a two-folder full-stack starter:

- `backend/` contains the existing Django REST Framework backend boilerplate.
- `frontend/` contains a React frontend built with Next.js.

## Frontend framework choice

The frontend uses Next.js because the current React framework landscape favors it
for application-style products with authentication flows, a large ecosystem, and
strong AI-agent support through opinionated conventions and extensive docs. The
research also showed Astro is strongest for content-first sites, while Vite is a
lean choice for simple SPAs. This project needs auth pages and backend
integration, so Next.js is the most practical React-based default.

## Run locally

### Backend

```bash
cd backend
cp .env.example .env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Frontend

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Open http://localhost:3000 and use:

- `/login` for the backend `/auth/token/` endpoint.
- `/signup` for the backend `/auth/signup/` endpoint.
- `/health` for the backend `/healthcheck/` endpoint.

## Deploy

The backend Docker deployment and Cloudflare frontend deployment are
independent.

```bash
cd backend
cp .env.example .env
# Configure backend/.env, then:
./start.sh
```

Cloudflare builds and serves `frontend/` separately. See
[deployment.md](deployment.md) for both release procedures, verification,
updates, and rollback.
