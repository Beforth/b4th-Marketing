# Docker Setup Guide for Marketing App

This guide explains how to set up and run the Marketing App using Docker Compose.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 1.29 or higher)

## Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd b4th-Marketing
   ```

2. **Build and start the containers:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Direct Django app: http://localhost:8000
   - Through Nginx: http://localhost:8080

## Docker Compose Services

### Web Service
- **Container Name:** `marketing_web`
- **Port:** 8000 (mapped to host port 8000)
- **Description:** Runs the Django application with Gunicorn

### Nginx Service
- **Container Name:** `marketing_nginx`
- **Ports:** 8080 (HTTP), 8443 (HTTPS)
- **Description:** Reverse proxy server for static files and load balancing

## Common Commands

### Start services
```bash
docker-compose up
```

### Start services in background
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

### View logs for specific service
```bash
docker-compose logs -f web
docker-compose logs -f nginx
```

### Rebuild containers
```bash
docker-compose up --build
```

### Run Django management commands
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
```

### Access Django shell
```bash
docker-compose exec web python manage.py shell
```

### Run custom management commands
```bash
docker-compose exec web python manage.py populate_marketing_permissions
```

## Environment Variables

The HRMS API URL can be configured via environment variable. You can set it in `docker-compose.yml`:

```yaml
environment:
  - HRMS_RBAC_API_URL=https://hrms.aureolegroup.com/api/rbac
```

Or create a `.env` file in the project root to configure:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `HRMS_RBAC_API_URL`: HRMS API base URL

## Database

By default, the app uses SQLite. The database file (`db.sqlite3`) is stored in the project directory and is persisted via Docker volumes.

To use PostgreSQL instead:

1. Add a PostgreSQL service to `docker-compose.yml`:
   ```yaml
   db:
     image: postgres:15
     container_name: marketing_db
     environment:
       POSTGRES_DB: marketing_db
       POSTGRES_USER: marketing_user
       POSTGRES_PASSWORD: marketing_password
     volumes:
       - postgres_data:/var/lib/postgresql/data
     networks:
       - backend
   ```

2. Update `settings.py` to use PostgreSQL:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': os.getenv('DB_NAME', 'marketing_db'),
           'USER': os.getenv('DB_USER', 'marketing_user'),
           'PASSWORD': os.getenv('DB_PASSWORD', 'marketing_password'),
           'HOST': os.getenv('DB_HOST', 'db'),
           'PORT': os.getenv('DB_PORT', '5432'),
       }
   }
   ```

## Static and Media Files

Static files are collected to `/app/staticfiles` and served by Nginx.
Media files are stored in `/app/media` and served by Nginx.

Both directories are mounted as volumes, so files persist between container restarts.

## SSL/HTTPS Configuration

To enable HTTPS:

1. Obtain SSL certificates (e.g., using Let's Encrypt)
2. Mount certificate directory in `docker-compose.yml`:
   ```yaml
   volumes:
     - /etc/letsencrypt:/etc/letsencrypt
   ```
3. Uncomment HTTPS server block in `nginx.conf`
4. Update `server_name` with your domain
5. Restart containers

## Troubleshooting

### Container won't start
- Check logs: `docker-compose logs web`
- Verify Docker is running: `docker ps`
- Check port availability: `netstat -tuln | grep 8000`

### HRMS API Connection Issues (502 Bad Gateway)

If you see "Invalid response format. Status: 502" or connection errors when logging in:

1. **Test connectivity from the container:**
   ```bash
   docker-compose exec web ./test_hrms_connectivity.sh
   ```

2. **Check if HRMS API is accessible:**
   - Verify the HRMS server is running
   - Test from your host machine: `curl https://hrms.aureolegroup.com/api/rbac/login/`
   - Check if the URL is correct in `settings.py` or environment variables

3. **Network configuration:**
   - If HRMS is on the same network, you might need to use internal IP
   - If HRMS is on localhost, use `host.docker.internal` (Mac/Windows) or host network mode
   - For Linux, you may need to add `network_mode: "host"` to the web service (not recommended for production)

4. **Override HRMS URL in Docker:**
   ```yaml
   environment:
     - HRMS_RBAC_API_URL=http://host.docker.internal:8001/api/rbac  # For local development
   ```

5. **Check Docker logs for detailed errors:**
   ```bash
   docker-compose logs -f web | grep -i "hrms\|rbac\|502\|connection"
   ```

### Database migration errors
```bash
docker-compose exec web python manage.py migrate --run-syncdb
```

### Permission denied errors
```bash
docker-compose exec web chmod -R 755 /app/staticfiles
docker-compose exec web chmod -R 755 /app/media
```

### Clear all data and start fresh
```bash
docker-compose down -v
docker-compose up --build
```

## Production Deployment

For production:

1. Set `DEBUG=False` in `.env`
2. Set a strong `SECRET_KEY`
3. Configure proper `ALLOWED_HOSTS`
4. Use PostgreSQL instead of SQLite
5. Enable HTTPS in Nginx
6. Set up proper logging
7. Configure backup strategy for database
8. Use environment-specific settings file

## Development vs Production

### Development
- Use SQLite for simplicity
- Enable DEBUG mode
- Run on localhost

### Production
- Use PostgreSQL
- Disable DEBUG
- Use proper domain names
- Enable HTTPS
- Set up monitoring and logging

