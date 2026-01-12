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

