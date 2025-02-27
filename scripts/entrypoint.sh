#!/bin/bash
set -e

# Function to display messages
info() {
    echo "[INFO] $@"
}

warning() {
    echo "[WARNING] $@"
}

error() {
    echo "[ERROR] $@"
    exit 1
}

# Wait for database if DB settings are configured
if [ -n "$DATABASE_URL" ] || [ -n "$DB_HOST" ]; then
    DB_HOST=${DB_HOST:-postgres}
    DB_PORT=${DB_PORT:-5432}
    
    info "Waiting for database at $DB_HOST:$DB_PORT..."
    /app/scripts/wait-for.sh $DB_HOST:$DB_PORT -t 60
    info "Database is up!"
fi

# Apply database migrations
# if [ "$DJANGO_APPLY_MIGRATIONS" = "1" ]; then
info "Applying database migrations..."
poetry run python manage.py migrate --noinput
# fi

# Create superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    info "Creating superuser..."
    poetry run python manage.py createsuperuser --noinput || warning "Superuser may already exist"
fi

# poetry run python manage.py collectstatic --clear --no-input

# Start Gunicorn
info "Starting application..."
exec "$@"