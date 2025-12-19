#!/bin/bash

# Docker startup script for Marketing App
# This script helps you get started with Docker Compose

set -e

echo "=========================================="
echo "Marketing App - Docker Setup"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cat > .env << EOF
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# HRMS RBAC API Configuration
HRMS_RBAC_API_URL=https://hrms.aureolegroup.com/api/rbac
EOF
    echo "✅ Created .env file. Please update SECRET_KEY before production use."
    echo ""
fi

# Build and start containers
echo "Building and starting containers..."
echo ""

if docker compose version &> /dev/null; then
    docker compose up --build -d
else
    docker-compose up --build -d
fi

echo ""
echo "=========================================="
echo "✅ Marketing App is starting!"
echo "=========================================="
echo ""
echo "Access the application at:"
echo "  - Direct Django: http://localhost:8000"
echo "  - Through Nginx: http://localhost:8080"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop:"
echo "  docker-compose down"
echo ""

