# Marketing Management System - Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Installation & Setup](#installation--setup)
4. [Configuration](#configuration)
5. [User Guide](#user-guide)
6. [API Documentation](#api-documentation)
7. [Database Schema](#database-schema)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)
11. [Security](#security)
12. [Performance Optimization](#performance-optimization)

## Overview

The Marketing Management System is a comprehensive Django-based web application designed to streamline and automate the entire marketing process flow. The system covers 17 distinct processes from database generation to post-event analysis.

### Key Features
- **Customer Management**: Multi-location customer database with GPS tracking
- **Lead Management**: Automated lead generation and tracking
- **Sales Process**: Complete sales pipeline from URS to PO
- **Production Tracking**: Manufacturing and QC tracking
- **Exhibition Management**: Event planning and vendor management
- **Advanced Features**: Email automation, SMS notifications, real-time alerts
- **Analytics & Reporting**: Comprehensive dashboards and reports

### Technology Stack
- **Backend**: Django 4.2+
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Frontend**: HTML5, CSS3 (Tailwind CSS), JavaScript
- **Icons**: Lucide Icons
- **Authentication**: Django's built-in authentication system

## System Architecture

### Core Components
1. **Models Layer**: 20+ Django models covering all business entities
2. **Views Layer**: 50+ views handling all business logic
3. **Templates Layer**: 30+ HTML templates with responsive design
4. **URL Layer**: RESTful URL patterns
5. **Static Files**: CSS, JavaScript, and media files

### Data Flow
```
User Input → Views → Models → Database
Database → Models → Views → Templates → User Interface
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- Git

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd marketing_standalone
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Open browser and navigate to `http://127.0.0.1:8000`
   - Login with superuser credentials

### Quick Start Scripts
- `setup.bat` (Windows) - Automated setup script
- `run_server.bat` (Windows) - Start development server

## Configuration

### Settings Configuration
The main configuration file is `marketing_project/settings.py`

#### Key Settings
```python
# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static Files Configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media Files Configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email Configuration (for production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Environment Variables
Create a `.env` file for sensitive configuration:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## User Guide

### Dashboard Overview
The dashboard provides a comprehensive overview of all key metrics:
- Total customers and leads
- Recent activities
- Performance indicators
- Quick action buttons

### Customer Management

#### Adding a New Customer
1. Navigate to **Customers** → **Add Customer**
2. Fill in required information:
   - Company name
   - Contact person
   - Email and phone
   - Address details
3. Add multiple locations if needed
4. Click **Save Customer**

#### Managing Customer Locations
1. Select a customer from the list
2. Click **Add Location**
3. Enter address and GPS coordinates
4. Save location

### Lead Management

#### Creating a Lead
1. Navigate to **Leads** → **Add Lead**
2. Select customer from dropdown
3. Choose lead source (cold calling, exhibition, etc.)
4. Set priority and expected value
5. Add notes and save

#### Lead Tracking
- View all leads in the leads list
- Filter by status, source, or priority
- Update lead status as it progresses
- Set follow-up reminders

### Sales Process

#### URS (User Requirements)
1. Navigate to **Sales Process** → **URS**
2. Create new URS for customer
3. Document requirements and specifications
4. Share with internal team

#### Technical Specifications
1. Evaluate URS compliance
2. Prepare technical data sheet
3. Conduct site evaluation
4. Update URS status

#### GA Drawing
1. Create GA drawing based on URS
2. Upload drawing file
3. Share with customer for feedback
4. Maintain version history

#### Quotation
1. Generate quotation with GA drawing
2. Set version numbers
3. Send to customer
4. Track follow-up reminders

### Production Tracking

#### Work Orders
1. Create work order from PO
2. Assign to team members
3. Set start and completion dates
4. Track progress

#### Manufacturing
1. Generate manufacturing cards
2. Plan production schedule
3. Track QC process
4. Record delays and breakdowns

#### Dispatch
1. Complete packing details
2. Generate dispatch checklist
3. Arrange transportation
4. Track delivery status

### Exhibition Management

#### Planning
1. Create exhibition plan
2. Set budget and objectives
3. Plan booth design
4. Schedule vendor meetings

#### Vendor Management
1. Add vendor details
2. Track vendor performance
3. Manage vendor contracts
4. Monitor vendor ratings

#### Visitor Database
1. Collect visitor information
2. Track visitor interests
3. Generate follow-up lists
4. Analyze visitor data

### Advanced Features

#### Email Automation
1. Create email templates
2. Set trigger conditions
3. Configure target audience
4. Monitor performance

#### SMS Notifications
1. Create SMS templates
2. Set notification triggers
3. Configure recipients
4. Track delivery rates

#### Real-time Notifications
- View live notifications
- Filter by priority
- Mark as read/unread
- Set notification preferences

## API Documentation

### Authentication
All API endpoints require authentication. Use Django's session authentication or token authentication.

### Customer API

#### Get All Customers
```http
GET /api/customers/
Authorization: Token <your-token>
```

Response:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/customers/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Test Company",
            "contact_person": "John Doe",
            "email": "john@testcompany.com",
            "phone": "+91-9876543210",
            "created_at": "2024-01-20T10:00:00Z"
        }
    ]
}
```

#### Create Customer
```http
POST /api/customers/
Authorization: Token <your-token>
Content-Type: application/json

{
    "name": "New Company",
    "contact_person": "Jane Smith",
    "email": "jane@newcompany.com",
    "phone": "+91-9876543211"
}
```

### Lead API

#### Get All Leads
```http
GET /api/leads/
Authorization: Token <your-token>
```

#### Create Lead
```http
POST /api/leads/
Authorization: Token <your-token>
Content-Type: application/json

{
    "customer": 1,
    "source": "cold_calling",
    "status": "new",
    "priority": "high",
    "expected_value": "50000.00"
}
```

### Visit API

#### Get All Visits
```http
GET /api/visits/
Authorization: Token <your-token>
```

#### Create Visit
```http
POST /api/visits/
Authorization: Token <your-token>
Content-Type: application/json

{
    "customer": 1,
    "visit_date": "2024-01-25",
    "purpose": "Sales Meeting",
    "outcome": "Positive",
    "next_follow_up": "2024-02-01"
}
```

## Database Schema

### Core Models

#### Customer
```sql
CREATE TABLE marketing_standalone_customer (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    created_by_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
```

#### CustomerLocation
```sql
CREATE TABLE marketing_standalone_customerlocation (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    gps_latitude DECIMAL(10,8),
    gps_longitude DECIMAL(11,8)
);
```

#### Lead
```sql
CREATE TABLE marketing_standalone_lead (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    source VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    expected_value DECIMAL(10,2),
    created_by_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL
);
```

#### Visit
```sql
CREATE TABLE marketing_standalone_visit (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    visit_date DATE NOT NULL,
    visit_time TIME NOT NULL,
    purpose TEXT NOT NULL,
    outcome VARCHAR(50) NOT NULL,
    next_follow_up DATE,
    created_by_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL
);
```

### Relationships
- Customer → CustomerLocation (One-to-Many)
- Customer → Lead (One-to-Many)
- Customer → Visit (One-to-Many)
- Customer → Quotation (One-to-Many)
- User → Expense (One-to-Many)
- User → Exhibition (One-to-Many)

## Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test marketing_standalone.tests.ModelTests

# Run specific test method
python manage.py test marketing_standalone.tests.ModelTests.test_customer_creation

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test Categories
1. **Model Tests**: Test all model creation and validation
2. **View Tests**: Test all view responses and templates
3. **Integration Tests**: Test complete workflows
4. **Performance Tests**: Test system performance under load
5. **Security Tests**: Test security vulnerabilities

### Test Data
The test suite includes comprehensive test data:
- 100 test customers
- 500 test leads
- Various test scenarios
- Performance benchmarks

## Deployment

### Production Setup

#### 1. Server Requirements
- Ubuntu 20.04+ or CentOS 8+
- Python 3.8+
- Nginx
- PostgreSQL
- Redis (optional, for caching)

#### 2. Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Install Nginx
sudo apt install nginx

# Install Redis (optional)
sudo apt install redis-server
```

#### 3. Database Setup
```bash
# Create database user
sudo -u postgres createuser --interactive

# Create database
sudo -u postgres createdb marketing_db

# Set password
sudo -u postgres psql
ALTER USER marketing_user PASSWORD 'your_password';
\q
```

#### 4. Application Setup
```bash
# Clone repository
git clone <repository-url>
cd marketing_standalone

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY='your-secret-key'
export DEBUG=False
export DATABASE_URL='postgresql://user:password@localhost/marketing_db'

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser
```

#### 5. Gunicorn Setup
```bash
# Install Gunicorn
pip install gunicorn

# Create Gunicorn service file
sudo nano /etc/systemd/system/marketing.service
```

Service file content:
```ini
[Unit]
Description=Marketing Management System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/marketing_standalone
Environment="PATH=/path/to/marketing_standalone/venv/bin"
ExecStart=/path/to/marketing_standalone/venv/bin/gunicorn --workers 3 --bind unix:/path/to/marketing_standalone/marketing.sock marketing_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 6. Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/marketing
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/marketing_standalone;
    }

    location /media/ {
        root /path/to/marketing_standalone;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/marketing_standalone/marketing.sock;
    }
}
```

#### 7. Start Services
```bash
# Enable and start services
sudo systemctl enable marketing
sudo systemctl start marketing
sudo systemctl enable nginx
sudo systemctl start nginx

# Enable site
sudo ln -s /etc/nginx/sites-available/marketing /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx
```

### SSL Configuration
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check database connection
sudo -u postgres psql -l

# Reset database password
sudo -u postgres psql
ALTER USER marketing_user PASSWORD 'new_password';
\q
```

#### 2. Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --clear

# Check Nginx configuration
sudo nginx -t

# Check file permissions
sudo chown -R www-data:www-data /path/to/marketing_standalone/static
```

#### 3. Permission Issues
```bash
# Set correct permissions
sudo chown -R www-data:www-data /path/to/marketing_standalone
sudo chmod -R 755 /path/to/marketing_standalone
```

#### 4. Gunicorn Issues
```bash
# Check Gunicorn status
sudo systemctl status marketing

# Check logs
sudo journalctl -u marketing

# Restart service
sudo systemctl restart marketing
```

### Performance Issues

#### 1. Slow Database Queries
- Add database indexes
- Optimize queries
- Use database caching

#### 2. Memory Issues
- Increase Gunicorn workers
- Add Redis caching
- Optimize static files

#### 3. High CPU Usage
- Monitor processes
- Optimize code
- Add load balancing

## Security

### Security Best Practices

#### 1. Environment Variables
- Never commit sensitive data to version control
- Use environment variables for secrets
- Rotate secrets regularly

#### 2. Database Security
- Use strong passwords
- Limit database access
- Regular backups
- Encrypt sensitive data

#### 3. Application Security
- Keep Django updated
- Use HTTPS in production
- Implement rate limiting
- Regular security audits

#### 4. Server Security
- Firewall configuration
- SSH key authentication
- Regular system updates
- Monitor logs

### Security Headers
```python
# Add to settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Performance Optimization

### Database Optimization

#### 1. Indexes
```python
# Add to models.py
class Customer(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

#### 2. Query Optimization
```python
# Use select_related for foreign keys
customers = Customer.objects.select_related('created_by').all()

# Use prefetch_related for many-to-many
customers = Customer.objects.prefetch_related('locations').all()

# Use only() to limit fields
customers = Customer.objects.only('name', 'email').all()
```

### Caching

#### 1. Redis Caching
```python
# Add to settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

#### 2. View Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def dashboard(request):
    # View logic here
    pass
```

### Static Files Optimization

#### 1. Compression
```python
# Add to settings.py
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
```

#### 2. CDN Configuration
```python
# Add to settings.py
STATIC_URL = 'https://your-cdn.com/static/'
MEDIA_URL = 'https://your-cdn.com/media/'
```

### Monitoring

#### 1. Application Monitoring
- Use Django Debug Toolbar in development
- Monitor database queries
- Track response times

#### 2. Server Monitoring
- Monitor CPU and memory usage
- Track disk space
- Monitor network traffic

#### 3. Error Tracking
- Use Sentry for error tracking
- Monitor application logs
- Set up alerts for critical errors

---

## Support

For technical support and questions:
- Email: support@marketing-system.com
- Documentation: https://docs.marketing-system.com
- GitHub Issues: https://github.com/your-repo/issues

## License

This project is licensed under the MIT License - see the LICENSE file for details.
