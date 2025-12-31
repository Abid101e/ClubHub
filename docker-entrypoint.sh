#!/bin/bash
set -e

echo "========================================"
echo "ClubHub Docker Entrypoint"
echo "========================================"

echo "Waiting for PostgreSQL at ${DB_HOST:-localhost}:${DB_PORT:-5432}..."
for i in {1..30}; do
    if pg_isready -h "${DB_HOST:-localhost}" -p "${DB_PORT:-5432}" -U "${DB_USER:-clubhub_user}" > /dev/null 2>&1; then
        echo "PostgreSQL is up and ready!"
        break
    fi
    echo "Waiting for PostgreSQL... ($i/30)"
    sleep 2
done

if ! pg_isready -h "${DB_HOST:-localhost}" -p "${DB_PORT:-5432}" -U "${DB_USER:-clubhub_user}" > /dev/null 2>&1; then
    echo "ERROR: PostgreSQL is not available after 60 seconds!"
    exit 1
fi

echo "Running database migrations..."
python3 manage.py migrate --noinput

echo "Collecting static files..."
mkdir -p /app/staticfiles
python3 manage.py collectstatic --noinput --clear || true

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Checking/creating superuser account..."
    python3 manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = '$DJANGO_SUPERUSER_USERNAME'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email='${DJANGO_SUPERUSER_EMAIL:-admin@clubhub.local}',
        password='$DJANGO_SUPERUSER_PASSWORD'
    )
    print(f'✓ Superuser "{username}" created successfully!')
else:
    print(f'✓ Superuser "{username}" already exists.')
EOF
fi

echo "========================================"
echo "Starting application..."
echo "Access the app at: http://localhost:8000"
echo "Admin panel at: http://localhost:8000/admin/"
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    echo "Admin username: $DJANGO_SUPERUSER_USERNAME"
fi
echo "========================================"

exec "$@"