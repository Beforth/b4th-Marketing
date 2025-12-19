FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn for production
RUN pip install --no-cache-dir gunicorn

# Copy project files
COPY . .

# Create directories for static files and media
RUN mkdir -p /app/staticfiles /app/media

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=marketing_system.settings

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn -c gunicorn.conf.py marketing_system.wsgi:application"]

