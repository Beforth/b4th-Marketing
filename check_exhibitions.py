#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketing_system.settings')
django.setup()

from marketing_app.models import Exhibition

# Check exhibitions
exhibitions = Exhibition.objects.all().order_by('-created_at')
print(f"Total exhibitions in database: {exhibitions.count()}")

print("\nRecent exhibitions:")
for exhibition in exhibitions[:5]:  # Show last 5
    print(f"  - {exhibition.name} | {exhibition.venue} | Status: {exhibition.status} | Created: {exhibition.created_at}")

print(f"\nExhibitions by status:")
for status_code, status_name in Exhibition.STATUS_CHOICES:
    count = exhibitions.filter(status=status_code).count()
    print(f"  - {status_name}: {count}")