# Docker Setup Guide for Trans Mobility App

## Overview
This document provides detailed information about the Docker configuration for the Trans Mobility application.

## Files Structure

### Docker Configuration Files

1. **Dockerfile** - Development Docker image configuration
   - Based on Python 3.11-slim
   - Includes PostgreSQL client tools
   - Auto-runs migrations on startup
   - Uses Django development server

2. **Dockerfile.production** - Production-optimized image
   - Non-root user for security
   - Uses Gunicorn WSGI server
   - Optimized for performance
   - Smaller attack surface

3. **docker-compose.yml** - Multi-container orchestration
   - Web service (Django app)
   - Database service (PostgreSQL 15)
   - Volume management
   - Network configuration

4. **docker-entrypoint.sh** - Container startup script
   - Waits for database availability
   - Runs migrations automatically
   - Starts the application server

5. **.dockerignore** - Files excluded from Docker build
   - Virtual environments
   - Cache files
   - Test files
   - Git history

6. **.env.example** - Environment variables template
   - Database credentials
   - Django settings
   - Security configurations

## Quick Start

### Development Setup
```bash
# Build and start all services
docker-compose up --build

# Access the application
open http://localhost:8000

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Production Setup
```bash
# Use production Dockerfile
docker-compose -f docker-compose.prod.yml up --build

# Or build manually
docker build -f Dockerfile.production -t transnet-mobility:prod .
docker run -p 8000:8000 --env-file .env transnet-mobility:prod
```

## Container Architecture

### Service: web (Django Application)
- **Image**: Built from Dockerfile
- **Ports**: 8000 (host) → 8000 (container)
- **Volumes**:
  - `.:/app` - Source code (hot reload in dev)
  - `static_volume:/app/staticfiles` - Static files
  - `media_volume:/app/media` - User uploads
- **Dependencies**: Waits for `db` service health check
- **Environment**: Uses env vars from docker-compose.yml

### Service: db (PostgreSQL)
- **Image**: postgres:15 (official)
- **Ports**: 5432 (host) → 5432 (container)
- **Volumes**: `postgres_data:/var/lib/postgresql/data`
- **Health Check**: Ensures database is ready before starting web
- **Environment**:
  - POSTGRES_DB
  - POSTGRES_USER
  - POSTGRES_PASSWORD

## Volume Management

### Persistent Volumes
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect trans_mobility_app_postgres_data

# Backup database volume
docker run --rm -v trans_mobility_app_postgres_data:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/postgres-backup.tar.gz /data

# Restore database volume
docker run --rm -v trans_mobility_app_postgres_data:/data -v $(pwd):/backup \
  ubuntu tar xzf /backup/postgres-backup.tar.gz -C /
```

### Volume Locations
- **postgres_data**: `/var/lib/docker/volumes/trans_mobility_app_postgres_data/_data`
- **static_volume**: `/var/lib/docker/volumes/trans_mobility_app_static_volume/_data`
- **media_volume**: `/var/lib/docker/volumes/trans_mobility_app_media_volume/_data`

## Environment Variables

### Required Variables
| Variable | Description | Default |
|----------|-------------|---------|
| DEBUG | Enable debug mode | True |
| SECRET_KEY | Django secret key | (provided) |
| DATABASE_HOST | PostgreSQL host | db |
| DATABASE_PORT | PostgreSQL port | 5432 |
| DATABASE_NAME | Database name | mobility_transnet |
| DATABASE_USER | Database user | postgres |
| DATABASE_PASSWORD | Database password | (provided) |

### Setting Environment Variables

**Method 1: docker-compose.yml**
```yaml
environment:
  - DEBUG=False
  - SECRET_KEY=your-secret-key
```

**Method 2: .env file**
```bash
# Create .env file
cp .env.example .env

# Edit values
nano .env

# Docker Compose automatically loads .env
docker-compose up
```

**Method 3: Command line**
```bash
docker-compose run -e DEBUG=False web python manage.py shell
```

## Common Tasks

### Database Operations

**Access PostgreSQL shell:**
```bash
docker-compose exec db psql -U postgres -d mobility_transnet
```

**Run migrations:**
```bash
docker-compose exec web python manage.py migrate
```

**Create migrations:**
```bash
docker-compose exec web python manage.py makemigrations
```

**Database backup:**
```bash
docker-compose exec db pg_dump -U postgres mobility_transnet > backup.sql
```

**Database restore:**
```bash
docker-compose exec -T db psql -U postgres mobility_transnet < backup.sql
```

### Django Management Commands

**Create superuser:**
```bash
docker-compose exec web python manage.py createsuperuser
```

**Collect static files:**
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

**Django shell:**
```bash
docker-compose exec web python manage.py shell
```

**Run tests:**
```bash
docker-compose exec web python manage.py test
```

**Custom management command:**
```bash
docker-compose exec web python manage.py update_driver_status
```

### Container Management

**View logs:**
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs web
docker-compose logs db

# Follow logs (real-time)
docker-compose logs -f web

# Last 100 lines
docker-compose logs --tail=100 web
```

**Container shell access:**
```bash
# Access web container bash
docker-compose exec web bash

# Access as root
docker-compose exec -u root web bash

# Run single command
docker-compose exec web ls -la /app
```

**Restart services:**
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart web
```

**View container stats:**
```bash
docker stats
```

## Troubleshooting

### Problem: Database connection refused
**Solution:**
```bash
# Check database is running
docker-compose ps

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Problem: Port already in use
**Solution:**
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -i :8000

# Or change port in docker-compose.yml
ports:
  - "8001:8000"
```

### Problem: Permission denied errors
**Solution:**
```bash
# Fix ownership (Linux/Mac)
sudo chown -R $USER:$USER .

# Windows: Run Docker Desktop as administrator
```

### Problem: Out of disk space
**Solution:**
```bash
# Remove unused containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Clean everything
docker system prune -a --volumes
```

### Problem: Migrations not applying
**Solution:**
```bash
# Check migration status
docker-compose exec web python manage.py showmigrations

# Force migrations
docker-compose exec web python manage.py migrate --run-syncdb

# Reset database (DANGER: Deletes all data)
docker-compose down -v
docker-compose up --build
```

### Problem: Static files not loading
**Solution:**
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput --clear

# Check STATIC_ROOT
docker-compose exec web python manage.py diffsettings | grep STATIC
```

## Production Deployment

### Using Docker Compose

1. **Create production compose file:**
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.production
    restart: always
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
    env_file:
      - .env.production
    depends_on:
      - db

  db:
    image: postgres:15
    restart: always
    volumes:
      - postgres_data_prod:/var/lib/postgresql/data
    env_file:
      - .env.production

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web

volumes:
  postgres_data_prod:
  static_volume:
  media_volume:
```

2. **Deploy:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Using Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml transnet

# Scale services
docker service scale transnet_web=3

# View services
docker service ls
```

### Using Kubernetes

```bash
# Create namespace
kubectl create namespace transnet

# Apply configurations
kubectl apply -f k8s/

# Check status
kubectl get pods -n transnet
```

## Security Best Practices

1. **Never commit sensitive data**
   - Use .env files (excluded from git)
   - Use Docker secrets for production
   - Rotate credentials regularly

2. **Use non-root users in production**
   - Dockerfile.production includes non-root user
   - Limits potential damage from vulnerabilities

3. **Keep images updated**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

4. **Scan for vulnerabilities**
   ```bash
   docker scan transnet-mobility:latest
   ```

5. **Use secrets management**
   ```bash
   echo "my-secret" | docker secret create db_password -
   ```

## Performance Optimization

### Image Size Reduction
- Use multi-stage builds
- Minimize layers
- Clean up package manager cache
- Use .dockerignore effectively

### Runtime Optimization
- Use Gunicorn with multiple workers
- Configure connection pooling
- Use Redis for caching
- Enable compression
- Use CDN for static files

### Resource Limits
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## Monitoring

### Container Health
```bash
# Check health status
docker-compose ps

# View resource usage
docker stats

# Check logs
docker-compose logs -f
```

### Application Monitoring
- Configure Django logging
- Use APM tools (New Relic, DataDog)
- Set up Prometheus + Grafana
- Enable health check endpoints

## Backup and Recovery

### Automated Backups
```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Database backup
docker-compose exec -T db pg_dump -U postgres mobility_transnet > \
  $BACKUP_DIR/db_backup_$DATE.sql

# Media files backup
docker run --rm -v trans_mobility_app_media_volume:/data -v $BACKUP_DIR:/backup \
  ubuntu tar czf /backup/media_backup_$DATE.tar.gz /data

# Cleanup old backups (keep last 7 days)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Recovery
```bash
# Restore database
cat backup.sql | docker-compose exec -T db psql -U postgres mobility_transnet

# Restore media files
docker run --rm -v trans_mobility_app_media_volume:/data -v $(pwd):/backup \
  ubuntu tar xzf /backup/media_backup.tar.gz -C /
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)

## Support

For issues related to Docker setup:
1. Check logs: `docker-compose logs`
2. Review this documentation
3. Check Docker and Docker Compose versions
4. Consult the main README.md
5. Create an issue in the repository
