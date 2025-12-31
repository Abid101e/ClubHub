# Docker Setup Guide

## Quick Start

Run the entire application with one command:

```bash
docker compose up --build
```

The application will be available at:
- **App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **Default Admin Credentials**:
  - Username: `admin`
  - Password: `admin123`

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

Check your versions:
```bash
docker --version
docker compose version
```

## Configuration

### Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Key environment variables in `.env`:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Settings
DB_NAME=clubhub_db
DB_USER=clubhub_user
DB_PASSWORD=changeme123
DB_HOST=db
DB_PORT=5432

# Superuser (created automatically on first run)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin123
DJANGO_SUPERUSER_EMAIL=admin@clubhub.local
```

**⚠️ Important**: Change `SECRET_KEY` and passwords before deploying to production!

## Docker Commands

### Start the Application

**Development mode** (with hot reload):
```bash
docker compose up
```

**Build and start** (rebuild images):
```bash
docker compose up --build
```

**Run in background** (detached mode):
```bash
docker compose up -d
```

### Stop the Application

```bash
docker compose down
```

**Stop and remove volumes** (⚠️ deletes database data):
```bash
docker compose down -v
```

### View Logs

**All services**:
```bash
docker compose logs -f
```

**Web service only**:
```bash
docker compose logs -f web
```

**Database service only**:
```bash
docker compose logs -f db
```

### Execute Commands Inside Container

**Open Django shell**:
```bash
docker compose exec web python3 manage.py shell
```

**Run migrations**:
```bash
docker compose exec web python3 manage.py migrate
```

**Create a superuser manually**:
```bash
docker compose exec web python3 manage.py createsuperuser
```

**Run tests**:
```bash
docker compose exec web python3 manage.py test
```

**Collect static files**:
```bash
docker compose exec web python3 manage.py collectstatic
```

### Database Management

**Access PostgreSQL CLI**:
```bash
docker compose exec db psql -U clubhub_user -d clubhub_db
```

**Backup database**:
```bash
docker compose exec db pg_dump -U clubhub_user clubhub_db > backup.sql
```

**Restore database**:
```bash
docker compose exec -T db psql -U clubhub_user clubhub_db < backup.sql
```

## What Happens on First Run?

The Docker entrypoint script automatically:

1. ✅ Waits for PostgreSQL to be ready
2. ✅ Runs database migrations
3. ✅ Collects static files
4. ✅ Creates a superuser account (if credentials provided)
5. ✅ Starts the Django development server

## Troubleshooting

### Port Already in Use

If port 8000 or 5433 is already in use, change them in `docker-compose.yml`:

```yaml
services:
  web:
    ports:
      - "8001:8000"  # Change 8001 to any available port
  db:
    ports:
      - "5434:5432"  # Change 5434 to any available port
```

### Database Connection Errors

If you see "connection refused" errors:

1. Check if PostgreSQL container is running:
   ```bash
   docker compose ps
   ```

2. Check PostgreSQL logs:
   ```bash
   docker compose logs db
   ```

3. Restart the services:
   ```bash
   docker compose down
   docker compose up
   ```

### Permission Errors

If you encounter permission errors with volumes:

```bash
docker compose down -v
docker compose up --build
```

### Fresh Start

To completely reset everything:

```bash
# Stop and remove everything
docker compose down -v

# Remove all images
docker compose down --rmi all

# Rebuild and start fresh
docker compose up --build
```

## File Structure

```
clubhub/
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile             # Docker image definition
├── docker-entrypoint.sh   # Startup script
├── .env                   # Environment variables (not in git)
├── .env.example          # Example environment file
└── requirements.txt      # Python dependencies
```

## Production Deployment

For production, you should:

1. Change `SECRET_KEY` to a secure random value
2. Set `DEBUG=False`
3. Update `ALLOWED_HOSTS` with your domain
4. Use strong database passwords
5. Use a proper WSGI server (Gunicorn is already in requirements.txt)
6. Set up HTTPS/SSL
7. Configure proper logging
8. Use environment-specific .env files

Example production command in `docker-compose.yml`:
```yaml
web:
  command: gunicorn clubhub.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## Volumes

The setup uses Docker volumes for data persistence:

- `postgres_data`: PostgreSQL database files
- `staticfiles`: Collected static files
- `media`: User-uploaded media files

To inspect volumes:
```bash
docker volume ls
docker volume inspect clubhub_postgres_data
```

## Development Tips

### Live Code Reload

The current setup mounts your code as a volume, so changes are reflected immediately without rebuilding.

### Access Container Shell

```bash
docker compose exec web bash
```

### Run Management Commands

```bash
docker compose exec web python3 manage.py <command>
```

### Check Container Resource Usage

```bash
docker stats
```

## Support

For issues or questions:
1. Check container logs: `docker compose logs -f`
2. Verify environment variables in `.env`
3. Ensure Docker and Docker Compose are up to date
4. Try a fresh start: `docker compose down -v && docker compose up --build`
