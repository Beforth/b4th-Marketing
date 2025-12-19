# HRMS User Fields Guide

This guide explains how the marketing app stores user information from HRMS instead of using Django User ForeignKeys.

## Overview

Since the marketing app uses HRMS RBAC for authentication, we don't need to create Django User instances. Instead, we store HRMS user information directly in the models.

## User Information Fields

Each model that previously had a `ForeignKey(User)` now has these fields:

- `{prefix}_user_id` - HRMS User ID (IntegerField)
- `{prefix}_username` - HRMS Username (CharField)
- `{prefix}_email` - HRMS User Email (EmailField)
- `{prefix}_full_name` - HRMS User Full Name (CharField)

Where `{prefix}` is:
- `created_by` - For objects created by a user
- `assigned_to` - For objects assigned to a user
- `approved_by` - For objects approved by a user
- etc.

## Example: Campaign Model

**Before:**
```python
created_by = models.ForeignKey(User, on_delete=models.CASCADE)
```

**After:**
```python
# HRMS User Information
created_by_user_id = models.IntegerField(null=True, blank=True)
created_by_username = models.CharField(max_length=150, blank=True)
created_by_email = models.EmailField(blank=True)
created_by_full_name = models.CharField(max_length=255, blank=True)
# Legacy field kept for backward compatibility
created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
```

## Using in Views

### Method 1: Using Helper Function

```python
from marketing_app.user_helpers import get_user_info_dict

def my_view(request):
    # Get user info from HRMS session
    user_info = get_user_info_dict(request)
    
    # Create object with user info
    campaign = Campaign.objects.create(
        name="My Campaign",
        # ... other fields ...
        created_by_user_id=user_info['user_id'],
        created_by_username=user_info['username'],
        created_by_email=user_info['email'],
        created_by_full_name=user_info['full_name'],
    )
```

### Method 2: Using Helper Function (Simpler)

```python
from marketing_app.user_helpers import set_user_info_on_model

def my_view(request):
    campaign = Campaign()
    campaign.name = "My Campaign"
    # ... set other fields ...
    
    # Set user info automatically
    set_user_info_on_model(campaign, request, 'created_by')
    campaign.save()
```

## Accessing User Info in Templates

In templates, you can access user info directly:

```html
{% if campaign.created_by_full_name %}
    Created by: {{ campaign.created_by_full_name }}
{% else %}
    Created by: {{ campaign.created_by_username }}
{% endif %}

Email: {{ campaign.created_by_email }}
```

## Migration Status

The following models have been updated:
- ✅ Campaign - `created_by_*` fields
- ✅ Lead - `assigned_to_*` fields
- ✅ Visit - `assigned_to_*` fields
- ⚠️ Customer - Needs migration
- ⚠️ EmailTemplate - Needs migration
- ⚠️ Other models - Can be updated as needed

## Benefits

1. **No Django User Dependency**: Don't need to create User instances
2. **HRMS Integration**: Directly uses HRMS user data
3. **Backward Compatible**: Legacy ForeignKey fields kept (nullable)
4. **Flexible**: Can store additional user info in JSON field if needed

## Migration

To add these fields to more models:

1. Update the model to add user info fields
2. Run: `python manage.py makemigrations marketing_app`
3. Run: `python manage.py migrate marketing_app`

## Example: Complete View Update

**Before:**
```python
def create_campaign(request):
    campaign = Campaign.objects.create(
        name=request.POST.get('name'),
        created_by=request.user  # ❌ Requires Django User
    )
```

**After:**
```python
from marketing_app.user_helpers import get_user_info_dict

def create_campaign(request):
    user_info = get_user_info_dict(request)
    
    campaign = Campaign.objects.create(
        name=request.POST.get('name'),
        # ✅ Store HRMS user info
        created_by_user_id=user_info['user_id'],
        created_by_username=user_info['username'],
        created_by_email=user_info['email'],
        created_by_full_name=user_info['full_name'],
    )
```

## Helper Functions

### `get_user_info_dict(request)`
Returns a dict with user info:
```python
{
    'user_id': 123,
    'username': 'john.doe',
    'email': 'john@example.com',
    'first_name': 'John',
    'last_name': 'Doe',
    'full_name': 'John Doe'
}
```

### `set_user_info_on_model(instance, request, field_prefix)`
Automatically sets user info fields on a model instance:
```python
campaign = Campaign()
set_user_info_on_model(campaign, request, 'created_by')
# Sets: created_by_user_id, created_by_username, etc.
```

## Notes

- Legacy `ForeignKey(User)` fields are kept but made nullable for backward compatibility
- Old data in ForeignKey fields will remain but new records use HRMS user info
- You can migrate existing data if needed (see migration scripts)

