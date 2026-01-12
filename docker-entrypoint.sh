#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist (optional)
# Uncomment the following lines and set your desired credentials
# python manage.py shell << END
# from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(email='admin@transnet.com').exists():
#     User.objects.create_superuser(email='admin@transnet.com', password='admin123', first_name='Admin', last_name='User')
# END

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
