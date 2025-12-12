#!/usr/bin/env bash
set -o errexit

echo "=== Upgrade pip ==="
pip install --upgrade pip

echo "=== Install requirements ==="
pip install -r requirements.txt

echo "=== Collect static files ==="
python manage.py collectstatic --noinput

echo "=== Apply database migrations ==="
python manage.py migrate