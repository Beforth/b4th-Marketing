#!/bin/bash

# Script to populate Marketing permissions in HRMS system
# This script runs the Django management command to create marketing permissions

echo "=========================================="
echo "Marketing Permissions Population Script"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found. Please run this script from the HRMS project root directory."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the management command
echo "Running populate_marketing_permissions command..."
python manage.py populate_marketing_permissions

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Marketing permissions populated successfully!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Review the permissions in HRMS Admin panel"
    echo "2. Assign permissions to specific roles as needed"
    echo "3. Assign roles to users"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "Error: Failed to populate permissions"
    echo "=========================================="
    exit 1
fi

