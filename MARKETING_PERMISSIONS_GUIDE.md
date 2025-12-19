# Marketing App Permissions Guide

This guide explains how to implement permission-based access control in the Marketing app using HRMS RBAC.

## Overview

The Marketing app uses HRMS RBAC API to check user permissions. Users can only see and access features they have permission for.

## Permission Codes

Marketing permissions follow this pattern: `marketing.{module}.{action}`

### Campaign Permissions
- `marketing.campaign.view` - View campaigns
- `marketing.campaign.create` - Create campaigns
- `marketing.campaign.edit` - Edit campaigns
- `marketing.campaign.delete` - Delete campaigns

### Lead Permissions
- `marketing.lead.view` - View leads
- `marketing.lead.create` - Create leads
- `marketing.lead.edit` - Edit leads
- `marketing.lead.delete` - Delete leads
- `marketing.lead.import` - Import leads

### Customer Permissions
- `marketing.customer.view` - View customers
- `marketing.customer.create` - Create customers
- `marketing.customer.edit` - Edit customers
- `marketing.customer.delete` - Delete customers
- `marketing.customer.import` - Import customers

### Visit Permissions
- `marketing.visit.view` - View visits
- `marketing.visit.create` - Create visits
- `marketing.visit.edit` - Edit visits
- `marketing.visit.delete` - Delete visits

### Report Permissions
- `marketing.reports.view` - View reports
- `marketing.reports.export` - Export reports

### Settings Permissions
- `marketing.settings.view` - View settings
- `marketing.settings.edit` - Edit settings

## Using Permissions in Views

### Basic Permission Check

```python
from marketing_app.permissions import require_permission, MARKETING_PERMISSIONS

@hrms_login_required
@require_permission(MARKETING_PERMISSIONS['campaign.view'])
def campaign_list(request):
    # Only users with campaign.view permission can access this
    campaigns = Campaign.objects.all()
    return render(request, 'marketing/campaign_list.html', {'campaigns': campaigns})
```

### Multiple Permissions (Any)

```python
from marketing_app.permissions import require_any_permission

@hrms_login_required
@require_any_permission([
    MARKETING_PERMISSIONS['campaign.view'],
    MARKETING_PERMISSIONS['campaign.edit']
])
def campaign_detail(request, campaign_id):
    # Users with either view or edit permission can access
    pass
```

### Multiple Permissions (All)

```python
from marketing_app.permissions import require_all_permissions

@hrms_login_required
@require_all_permissions([
    MARKETING_PERMISSIONS['campaign.view'],
    MARKETING_PERMISSIONS['campaign.edit']
])
def campaign_edit(request, campaign_id):
    # Users must have both view AND edit permissions
    pass
```

### Conditional Permission Check

```python
from marketing_app.permissions import check_permission

def my_view(request):
    can_edit = check_permission(request, MARKETING_PERMISSIONS['campaign.edit'])
    
    if can_edit:
        # Show edit button
        pass
    else:
        # Hide edit button
        pass
```

## Filtering Data by Permissions

Use permission filters to restrict data visibility:

```python
from marketing_app.permission_filters import filter_campaigns_by_permission

def campaign_list(request):
    campaigns = Campaign.objects.all()
    campaigns = filter_campaigns_by_permission(request, campaigns)
    # Only campaigns user has permission to see will be returned
    return render(request, 'marketing/campaign_list.html', {'campaigns': campaigns})
```

## Using Permissions in Templates

### Method 1: Context Processor (Recommended)

The permissions context processor makes `has_permission` available in all templates:

```html
{% if has_permission|call:'marketing.campaign.view' %}
    <a href="/campaigns/">View Campaigns</a>
{% endif %}

{% if has_permission|call:'marketing.campaign.create' %}
    <a href="/campaigns/create/">Create Campaign</a>
{% endif %}
```

### Method 2: Template Tags

```html
{% load marketing_permissions %}

{% has_permission 'marketing.campaign.view' as can_view %}
{% if can_view %}
    <a href="/campaigns/">Campaigns</a>
{% endif %}

{% if request|has_perm:'marketing.campaign.create' %}
    <button>Create Campaign</button>
{% endif %}
```

### Method 3: User Permissions List

```html
{% load marketing_permissions %}

{% user_permissions as permissions %}
{% if 'marketing.campaign.view' in permissions %}
    <a href="/campaigns/">Campaigns</a>
{% endif %}
```

## Setting Up Permissions in HRMS

1. Log into HRMS system
2. Go to RBAC Management
3. Create permissions with codes like:
   - `marketing.campaign.view`
   - `marketing.campaign.create`
   - etc.
4. Assign permissions to roles
5. Assign roles to users

## Example: Complete View with Permissions

```python
from marketing_app.permissions import (
    require_permission, check_permission, MARKETING_PERMISSIONS
)
from marketing_app.permission_filters import (
    filter_campaigns_by_permission,
    can_edit_campaign,
    can_delete_campaign
)

@hrms_login_required
@require_permission(MARKETING_PERMISSIONS['campaign.view'])
def campaign_list(request):
    # Filter campaigns based on permissions
    campaigns = Campaign.objects.all()
    campaigns = filter_campaigns_by_permission(request, campaigns)
    
    # Check additional permissions for UI
    can_create = check_permission(request, MARKETING_PERMISSIONS['campaign.create'])
    can_edit = can_edit_campaign(request)
    can_delete = can_delete_campaign(request)
    
    context = {
        'campaigns': campaigns,
        'can_create': can_create,
        'can_edit': can_edit,
        'can_delete': can_delete,
    }
    
    return render(request, 'marketing/campaign_list.html', context)
```

## Best Practices

1. **Always use decorators** on views to enforce permissions
2. **Filter querysets** to only show data users can access
3. **Check permissions in templates** to show/hide UI elements
4. **Use permission filters** for complex data filtering
5. **Log permission denials** for security auditing
6. **Provide clear error messages** when permissions are denied

## Troubleshooting

### Permission not working?

1. Check if permission exists in HRMS with exact code
2. Verify user has the permission assigned
3. Check if token is valid in session
4. Review server logs for permission check errors

### Data still showing?

1. Make sure you're filtering querysets, not just checking view access
2. Use permission filters for data filtering
3. Check template conditions are correct

### Template permission check not working?

1. Make sure context processor is added to settings
2. Verify template tag is loaded: `{% load marketing_permissions %}`
3. Check permission code spelling matches exactly

