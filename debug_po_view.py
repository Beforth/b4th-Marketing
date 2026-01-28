#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketing_system.settings')
django.setup()

from marketing_app.models import PurchaseOrder, Customer
from django.core.paginator import Paginator

# Simulate the view logic
purchase_orders = PurchaseOrder.objects.select_related('customer').order_by('-created_at')
print(f"Initial queryset count: {purchase_orders.count()}")

# Check pagination
paginator = Paginator(purchase_orders, 20)
page_obj = paginator.get_page(1)

print(f"Page object count: {page_obj.paginator.count}")
print(f"Page object has items: {bool(page_obj.object_list)}")
print(f"Page object items: {len(page_obj.object_list)}")

for po in page_obj.object_list:
    print(f"  - {po.po_number} | {po.customer.name} | {po.status}")