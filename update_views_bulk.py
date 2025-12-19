#!/usr/bin/env python3
"""
Script to bulk update views.py to use HRMS user info instead of Django User
Run: python update_views_bulk.py
"""
import re

# Read the views file
with open('marketing_app/views.py', 'r') as f:
    content = f.read()

# Pattern 1: Replace created_by=request.user in .create() calls
pattern1 = r'(\s+)(created_by=request\.user)'
replacement1 = r'''\1# Get user info from HRMS session
\1user_info = get_user_info_dict(request)
\1
\1# Store HRMS user info
\1created_by_user_id=user_info['user_id'],
\1created_by_username=user_info['username'],
\1created_by_email=user_info['email'],
\1created_by_full_name=user_info['full_name'],'''
content = re.sub(pattern1, replacement1, content)

# Pattern 2: Replace approved_by=request.user
pattern2 = r'(\s+)(approved_by=request\.user)'
replacement2 = r'''\1# Get user info from HRMS session
\1user_info = get_user_info_dict(request)
\1
\1# Store HRMS user info
\1approved_by_user_id=user_info['user_id'],
\1approved_by_username=user_info['username'],
\1approved_by_email=user_info['email'],
\1approved_by_full_name=user_info['full_name'],'''
content = re.sub(pattern2, replacement2, content)

# Write back
with open('marketing_app/views.py', 'w') as f:
    f.write(content)

print("Updated views.py with HRMS user info fields")
print("Please review the changes and test!")

