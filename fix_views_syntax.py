#!/usr/bin/env python3
"""
Fix syntax errors in views.py by moving user_info declarations outside .create() calls
"""
import re

# Read the file
with open('marketing_app/views.py', 'r') as f:
    content = f.read()

# Pattern: Find .create( ... user_info = get_user_info_dict(request) ... )
# We need to move user_info declaration before .create()

# First, find all instances where user_info is inside .create()
pattern = r'(\s+)([A-Za-z_][A-Za-z0-9_]*\.objects\.create\([^)]*?)# Get user info from HRMS session\s+user_info = get_user_info_dict\(request\)\s+([^)]*?\))'

def fix_create_call(match):
    indent = match.group(1)
    create_call = match.group(2)
    rest = match.group(3)
    
    # Extract the model name and parameters before user_info
    # This is complex, so let's use a simpler approach
    
    # Find the line with .create( and extract everything before user_info
    lines = match.group(0).split('\n')
    
    # Find where .create( starts
    create_idx = None
    user_info_idx = None
    
    for i, line in enumerate(lines):
        if '.objects.create(' in line:
            create_idx = i
        if 'user_info = get_user_info_dict(request)' in line:
            user_info_idx = i
    
    if create_idx is None or user_info_idx is None:
        return match.group(0)  # Return unchanged if we can't parse
    
    # Extract everything before user_info
    before_user_info = '\n'.join(lines[:user_info_idx])
    after_user_info = '\n'.join(lines[user_info_idx+1:])
    
    # Remove the user_info line and its surrounding comments from inside
    # Move it before .create()
    before_create = '\n'.join(lines[:create_idx])
    create_line = lines[create_idx]
    
    # Extract the part after user_info but before closing )
    # This is getting too complex. Let's use a different approach.
    
    return match.group(0)  # For now, return unchanged

# Simpler approach: Find patterns and fix them manually
# Pattern 1: user_info inside .create() with proper indentation
pattern1 = r'(\s+)([A-Za-z_][A-Za-z0-9_]*\.objects\.create\(\s*\n(?:[^\n]*\n)*?)# Get user info from HRMS session\s*\n\s+user_info = get_user_info_dict\(request\)\s*\n\s+([^\n]*\n)'

# Actually, let's just find and replace the specific problematic pattern
# We'll look for the pattern where user_info is inside create()

# Read line by line and fix
lines = content.split('\n')
fixed_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if this line has .objects.create(
    if '.objects.create(' in line:
        # Look ahead for user_info = get_user_info_dict(request)
        j = i + 1
        found_user_info = False
        user_info_line_idx = None
        
        while j < len(lines) and not lines[j].strip().startswith(')'):
            if 'user_info = get_user_info_dict(request)' in lines[j]:
                found_user_info = True
                user_info_line_idx = j
                break
            j += 1
        
        if found_user_info:
            # Extract the user_info line
            user_info_line = lines[user_info_line_idx]
            indent_level = len(line) - len(line.lstrip())
            
            # Remove user_info from inside
            lines[user_info_line_idx] = ''  # Remove it
            
            # Add user_info before .create() with proper indentation
            fixed_lines.append(' ' * indent_level + '# Get user info from HRMS session')
            fixed_lines.append(' ' * indent_level + 'user_info = get_user_info_dict(request)')
            fixed_lines.append('')
            fixed_lines.append(line)
            i += 1
            continue
    
    fixed_lines.append(line)
    i += 1

# Write back
with open('marketing_app/views.py', 'w') as f:
    f.write('\n'.join(fixed_lines))

print("Fixed syntax errors in views.py")

