#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketing_system.settings')
django.setup()

from marketing_app.models import PurchaseOrder
from django.contrib.auth.models import User

# Test the exact same query as the workorder_create view
purchase_orders = PurchaseOrder.objects.filter(status__in=['received', 'verified', 'approved']).order_by('-created_at')
users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')

print(f"Purchase Orders found: {purchase_orders.count()}")
for po in purchase_orders:
    print(f"  - {po.po_number} | {po.customer.name} | Status: {po.status}")

print(f"\nUsers found: {users.count()}")
for user in users[:3]:  # Show first 3
    print(f"  - {user.username} | {user.get_full_name()}")

# Test if the view function works
from marketing_app.views import workorder_create
print(f"\nworkorder_create function exists: {callable(workorder_create)}")