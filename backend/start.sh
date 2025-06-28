#!/bin/bash

# Wait for database to be ready
echo "Waiting for database to be ready..."
while ! pg_isready -h db -p 5432 -U rex_user; do
  sleep 2
done

echo "Database is ready!"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application
echo "Starting the application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 