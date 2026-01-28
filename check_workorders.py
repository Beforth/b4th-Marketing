#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketing_system.settings')
django.setup()

from marketing_app.models import WorkOrder, WorkOrderFormat

# Check WorkOrder objects
work_orders = WorkOrder.objects.all()
print(f"Total WorkOrder objects: {work_orders.count()}")

for wo in work_orders:
    print(f"WorkOrder: {wo.work_order_number} - PO: {wo.purchase_order.po_number} - Status: {wo.status} - Created: {wo.created_at}")

# Check WorkOrderFormat objects
work_order_formats = WorkOrderFormat.objects.all()
print(f"\nTotal WorkOrderFormat objects: {work_order_formats.count()}")

for wof in work_order_formats[:3]:  # Show first 3
    print(f"WorkOrderFormat: {wof.work_order_no} - Created: {wof.created_at}")