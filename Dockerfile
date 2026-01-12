# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . /app/

# Create media directory for user uploads
RUN mkdir -p /app/media/driver_requests /app/media/profiles

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port 8000
EXPOSE 8000

# Create a script to run migrations and start server
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]
