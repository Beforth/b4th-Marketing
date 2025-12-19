# Marketing Module - Standalone

This is a complete marketing module with the same beautiful design as the HR system, integrated with HRMS RBAC for authentication and permissions.

## Features
- Campaign Management
- Lead Management  
- Email Templates
- Analytics & Metrics
- Lead Scoring
- Activity Tracking
- HRMS RBAC Integration

## Quick Start with Docker

The easiest way to run the Marketing App is using Docker Compose:

```bash
# Start the application
./docker-start.sh

# Or manually:
docker-compose up --build
```

Access the application at:
- Direct Django: http://localhost:8000
- Through Nginx: http://localhost:8080

For detailed Docker setup instructions, see [DOCKER_SETUP.md](DOCKER_SETUP.md).

## Manual Installation

1. Copy this folder to your project
2. Add 'marketing_app' to INSTALLED_APPS
3. Run migrations: `python manage.py migrate`
4. Add URLs to your main urls.py
5. Configure HRMS RBAC API URL in settings

## Design
Uses the same design system as HR module:
- Tailwind CSS
- Lucide Icons
- Responsive design
- Beautiful animations

## Documentation

- [Docker Setup Guide](DOCKER_SETUP.md)
- [HRMS RBAC Integration](HRMS_RBAC_INTEGRATION.md)
- [Marketing Permissions Guide](MARKETING_PERMISSIONS_GUIDE.md)
- [Workflow Coverage Analysis](WORKFLOW_COVERAGE_ANALYSIS.md)
