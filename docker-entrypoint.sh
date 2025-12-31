#!/bin/bash
set -e

echo "========================================"
echo "ClubHub Docker Entrypoint"
echo "========================================"

echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL is up and ready!"

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || true

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser account..."
    python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='${DJANGO_SUPERUSER_EMAIL:-admin@example.com}',
        password='$DJANGO_SUPERUSER_PASSWORD'
    )
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')
EOF
fi

echo "========================================"
echo "Starting application..."
echo "========================================"

exec "$@"