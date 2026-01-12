# Trans Mobility App

A Django-based logistics and scheduling platform for managing locomotives, wagons, drivers, and assignments.

## Features
- Locomotive and wagon management
- Driver assignments and scheduling
- Maintenance scheduling
- REST API for integration
- Admin dashboard with analytics

## Prerequisites

### Option 1: Docker (Recommended)
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose

### Option 2: Local Setup
- Python 3.8+
- pip (Python package manager)
- (Recommended) Virtual environment tool: `venv` or `virtualenv`
- PostgreSQL 12+ (with database created and credentials ready)

## Quick Start with Docker 🐳

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Trans_mobility_app
```

### 2. Build and Run with Docker Compose
```bash
docker-compose up --build
```

This single command will:
- Build the Docker image for the Django application
- Start a PostgreSQL database container
- Run database migrations automatically
- Start the development server

The app will be available at http://localhost:8000/

### 3. Create a Superuser (Admin)
Open a new terminal and run:
```bash
docker-compose exec web python manage.py createsuperuser
```

### 4. Stop the Application
```bash
docker-compose down
```

### 5. Stop and Remove All Data (including database)
```bash
docker-compose down -v
```

## Docker Commands Reference

| Command | Description |
|---------|-------------|
| `docker-compose up` | Start the application |
| `docker-compose up --build` | Rebuild and start the application |
| `docker-compose up -d` | Start in detached mode (background) |
| `docker-compose down` | Stop the application |
| `docker-compose down -v` | Stop and remove volumes (database data) |
| `docker-compose logs web` | View web application logs |
| `docker-compose logs db` | View database logs |
| `docker-compose exec web bash` | Access web container shell |
| `docker-compose exec web python manage.py <command>` | Run Django management commands |

## Local Setup Instructions (Without Docker)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Trans_mobility_app
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Migration Commands
Run the following commands to set up the database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

The app will be available at http://127.0.0.1:8000/

## Database Connection Strings

The app uses PostgreSQL as its primary database. Update the `DATABASES` setting in `mobility/settings.py` with your PostgreSQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'trans_mobility_db',  # Your database name
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',  # Default PostgreSQL port
    }
}
```

**Note:** Ensure you have the PostgreSQL adapter installed:
```bash
pip install psycopg2-binary
```

After updating, re-run the migration commands:
```bash
python manage.py migrate
```

## Additional Management Commands
- **Auto-update driver status** (runs automatically via middleware on each request):
  The system automatically checks and updates driver status from 'on_leave' or 'emergency' to 'available' when their leave/emergency period has ended (based on date and time).

- **Manual driver status update** (can be run via cron job or manually):
  ```bash
  python manage.py update_driver_status
  ```
  This command checks all drivers and updates their status to 'available' if their leave/emergency period has ended.

## Automated Status Updates
The application includes middleware (`AutoUpdateDriverStatusMiddleware`) that automatically:
- Checks driver status on every request
- Updates drivers from 'on_leave' or 'emergency' to 'available' when their `on_leave_until` datetime has passed
- Ensures real-time status updates without manual intervention

For scheduled/background updates, set up a cron job to run `python manage.py update_driver_status` periodically (e.g., every hour).

## Notes
- Static and media files are served automatically in development.
- For production, configure static/media file serving and use a production-ready database.

## Docker Architecture

The application uses Docker Compose to orchestrate two services:

### Services
1. **web**: Django application container
   - Built from the Dockerfile
   - Exposes port 8000
   - Auto-runs migrations on startup
   - Mounts the project directory for hot-reload during development

2. **db**: PostgreSQL database container
   - Uses PostgreSQL 15 official image
   - Persistent data storage using Docker volumes
   - Automatically configured with the credentials from docker-compose.yml

### Volumes
- `postgres_data`: Persistent database storage
- `static_volume`: Static files (CSS, JS, images)
- `media_volume`: User-uploaded files (profiles, driver requests)

### Networking
- Both containers are on the same Docker network
- The web container can access the database using hostname `db`
- Port 8000 is exposed for accessing the web application
- Port 5432 is exposed for direct database access (optional)

## Environment Variables

You can customize the application by modifying environment variables in `docker-compose.yml`:

- `DEBUG`: Enable/disable debug mode (True/False)
- `DATABASE_HOST`: Database host (default: db)
- `DATABASE_PORT`: Database port (default: 5432)
- `DATABASE_NAME`: Database name
- `DATABASE_USER`: Database user
- `DATABASE_PASSWORD`: Database password

## Troubleshooting

### Docker Issues

**Container won't start:**
```bash
docker-compose down
docker-compose up --build
```

**Database connection errors:**
```bash
# Check if database container is running
docker-compose ps

# View database logs
docker-compose logs db
```

**Permission errors on Linux:**
```bash
# Fix permissions for media and static files
sudo chown -R $USER:$USER media/ staticfiles/
```

**Reset everything:**
```bash
# Stop containers and remove volumes
docker-compose down -v

# Remove all images
docker-compose rm -f

# Rebuild from scratch
docker-compose up --build
```

### Common Issues

**Port already in use:**
If port 8000 or 5432 is already in use, modify the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Map to different host port
```

**Database migrations not running:**
```bash
docker-compose exec web python manage.py migrate
```

**Static files not loading:**
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

## Production Deployment

For production deployment, consider:

1. **Use environment variables for sensitive data**
   - Never commit passwords or secret keys
   - Use Docker secrets or environment variable files

2. **Use a production WSGI server**
   - Replace `runserver` with Gunicorn or uWSGI
   - Example: `gunicorn mobility.wsgi:application --bind 0.0.0.0:8000`

3. **Configure ALLOWED_HOSTS**
   - Update `ALLOWED_HOSTS` in settings.py with your domain

4. **Disable DEBUG mode**
   - Set `DEBUG=False` in production

5. **Use a reverse proxy**
   - Set up Nginx or Apache as a reverse proxy
   - Handle static/media files through the proxy

6. **Database backups**
   - Set up regular PostgreSQL backups
   - Use Docker volume backups

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker: `docker-compose up --build`
5. Submit a pull request

## License

[Add your license here]

## Support

For issues and questions:
- Create an issue in the repository
- Contact the development team

