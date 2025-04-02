FROM python:3.12-slim


ENV PYTHONUNBUFFERED=1 \
PYTHONDONTWRITEBYTECODE=1 \
DJANGO_SETTINGS_MODULE=core.settings \
\
# pip
PIP_NO_CACHE_DIR=off \
PIP_DISABLE_PIP_VERSION_CHECK=on \
PIP_DEFAULT_TIMEOUT=100 \
\
# poetry
POETRY_VIRTUALENVS_IN_PROJECT=false \
POETRY_VIRTUALENVS_CREATE=false \
POETRY_NO_INTERACTION=1

# Set work directory
WORKDIR /app


# Install Python dependencies
COPY poetry.lock pyproject.toml /app/

# Install Poetry and dependencies
RUN pip install --upgrade pip && pip install "poetry<1.8" && poetry install --no-ansi

RUN apt update && apt install netcat-openbsd -y

# Copy project
COPY . /app/

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' django_user
RUN chown -R django_user:django_user /app
USER django_user

EXPOSE 8000


# Run entrypoint script
ENTRYPOINT ["/app/scripts/entrypoint.sh"]

# Default command (can be overridden)
CMD ["poetry", "run", "gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
