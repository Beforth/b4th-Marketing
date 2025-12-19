# Populate Marketing Permissions Guide

This guide explains how to populate Marketing permissions in the HRMS RBAC system.

## Overview

The Marketing module requires specific permissions to be created in the HRMS system. This script creates all necessary permissions and optionally assigns them to default roles.

## Permissions Created

The script creates the following permissions:

### Campaign Management
- `marketing.campaign.view` - View campaigns
- `marketing.campaign.create` - Create campaigns
- `marketing.campaign.edit` - Edit campaigns
- `marketing.campaign.delete` - Delete campaigns

### Lead Management
- `marketing.lead.view` - View leads
- `marketing.lead.create` - Create leads
- `marketing.lead.edit` - Edit leads
- `marketing.lead.delete` - Delete leads
- `marketing.lead.import` - Import leads

### Customer Management
- `marketing.customer.view` - View customers
- `marketing.customer.create` - Create customers
- `marketing.customer.edit` - Edit customers
- `marketing.customer.delete` - Delete customers
- `marketing.customer.import` - Import customers

### Visit Management
- `marketing.visit.view` - View visits
- `marketing.visit.create` - Create visits
- `marketing.visit.edit` - Edit visits
- `marketing.visit.delete` - Delete visits

### Reports & Analytics
- `marketing.reports.view` - View reports
- `marketing.reports.export` - Export reports

### Settings
- `marketing.settings.view` - View settings
- `marketing.settings.edit` - Edit settings

## Usage

### Method 1: Using Django Management Command

```bash
# From HRMS project root directory
python manage.py populate_marketing_permissions
```

### Method 2: Using Shell Script

```bash
# From HRMS project root directory
./populate_marketing_permissions.sh
```

Or if the script is in b4th-Marketing directory:

```bash
cd /path/to/HRMS-ady.edit
bash b4th-Marketing/populate_marketing_permissions.sh
```

## Default Role Assignments

The script automatically assigns permissions to default roles:

### Admin Role
- **All permissions** - Full access to all marketing features

### HR Role
- View, create, edit campaigns
- View, create, edit, import leads
- View, create, edit, import customers
- View, create, edit visits
- View and export reports

### Manager Role
- View campaigns
- View, create, edit leads
- View, create, edit customers
- View, create, edit visits
- View reports

### Employee Role
- View campaigns
- View leads
- View customers
- View visits

## Manual Assignment

If you need to assign permissions manually:

1. Log into HRMS Admin panel
2. Go to RBAC Management
3. Select a Role
4. Add the marketing permissions you want
5. Save the role

## Verification

After running the script, verify permissions were created:

1. Log into HRMS Admin panel
2. Go to RBAC → Permissions
3. Filter by category: "marketing"
4. You should see all 22 marketing permissions

## Troubleshooting

### Permission Already Exists

If a permission already exists, the script will update it with the latest information. This is safe and won't cause issues.

### Role Not Found

If a default role (admin, hr, manager, employee) doesn't exist, the script will skip assigning permissions to that role. You can manually assign permissions later.

### Database Errors

If you encounter database errors:
1. Check database connection
2. Ensure migrations are up to date: `python manage.py migrate`
3. Check database permissions

## Updating Permissions

To update existing permissions:

1. Run the script again - it will update existing permissions
2. Or manually edit permissions in the HRMS Admin panel

## Next Steps

After populating permissions:

1. **Review Permissions**: Check that all permissions were created correctly
2. **Assign to Roles**: Verify default role assignments or assign manually
3. **Assign Roles to Users**: Assign appropriate roles to users in HRMS
4. **Test Access**: Log in as different users and test permission-based access

## Example: Assigning Custom Permissions

If you want to create a custom role with specific marketing permissions:

```python
from employees.models import Role, Permission, RolePermission

# Create custom role
custom_role = Role.objects.create(
    name='Marketing Manager',
    role_type='manager',
    description='Marketing team manager',
    level=2,
    is_active=True
)

# Assign specific permissions
permissions = Permission.objects.filter(
    code__in=[
        'marketing.campaign.view',
        'marketing.campaign.create',
        'marketing.lead.view',
        'marketing.lead.create',
        'marketing.reports.view',
    ]
)

for perm in permissions:
    RolePermission.objects.create(
        role=custom_role,
        permission=perm,
        granted=True
    )
```

## Support

If you encounter issues:
1. Check the Django logs for error messages
2. Verify HRMS API is accessible
3. Ensure all migrations are applied
4. Check that default roles exist in the system

