#!/usr/bin/env bash

set -Eeuo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

if [[ ! -f .env ]]; then
    echo "Missing backend/.env. Copy .env.example to .env and configure it first." >&2
    exit 1
fi

# Keep the deployment checkout current without creating a merge commit.
git pull --ff-only

sudo docker compose build
sudo docker compose run --rm backend python manage.py migrate --noinput
sudo docker compose run --rm backend python manage.py collectstatic --noinput
sudo docker compose up -d backend celery-worker celery-beat

echo "Running Docker image prune..."
sudo docker image prune -f

sudo docker compose ps
