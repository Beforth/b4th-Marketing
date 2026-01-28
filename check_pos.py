#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketing_system.settings')
django.setup()

from marketing_app.models import PurchaseOrder, Customer

# Check POs
pos = PurchaseOrder.objects.all()
print(f"Total POs in database: {pos.count()}")

for po in pos:
    print(f"PO: {po.po_number} - Customer: {po.customer.name} - Status: {po.status} - Created: {po.created_at}")

# Check customers
customers = Customer.objects.all()
print(f"\nTotal Customers: {customers.count()}")
for customer in customers[:5]:  # Show first 5
    print(f"Customer: {customer.name}")