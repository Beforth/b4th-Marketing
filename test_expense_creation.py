#!/usr/bin/env python
"""
Test script to verify expense creation functionality
"""
import os
import sys
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketing_system.settings')
django.setup()

from marketing_app.models import Expense
from django.test import RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from marketing_app.views import expense_create, expense_list

def test_expense_creation():
    """Test expense creation through the view"""
    factory = RequestFactory()
    
    # Test POST request to create expense
    post_data = {
        'date': date.today().strftime('%Y-%m-%d'),
        'expense_type': 'transport',
        'amount': '1200.50',
        'description': 'Taxi fare for client meeting'
    }
    
    request = factory.post('/expenses/create/', post_data)
    request.user = AnonymousUser()  # Simulate anonymous user for testing
    
    print("Testing expense creation...")
    print(f"Before creation: {Expense.objects.count()} expenses")
    
    try:
        # This would normally require login, but we'll test the core logic
        response = expense_create(request)
        print(f"After creation attempt: {Expense.objects.count()} expenses")
        print("Response status:", response.status_code if hasattr(response, 'status_code') else 'Redirect')
    except Exception as e:
        print(f"Error during creation: {e}")
    
    # Test expense list view
    print("\nTesting expense list view...")
    request = factory.get('/expenses/')
    request.user = AnonymousUser()
    
    try:
        response = expense_list(request)
        print("Expense list view executed successfully")
        print(f"Response status: {response.status_code if hasattr(response, 'status_code') else 'OK'}")
    except Exception as e:
        print(f"Error in expense list: {e}")
    
    # Show current expenses
    print(f"\nCurrent expenses in database: {Expense.objects.count()}")
    for expense in Expense.objects.all()[:5]:  # Show first 5
        print(f"- ID: {expense.id}, Type: {expense.expense_type}, Amount: ₹{expense.amount}, User: {expense.expense_full_name or 'Unknown'}")

if __name__ == '__main__':
    test_expense_creation()