# HRMS RBAC Integration Documentation

This document describes the HRMS RBAC API integration for the b4th-Marketing system.

## Overview

The b4th-Marketing system now uses the HRMS RBAC API for authentication and permission management. All user authentication and permission checks are handled through the HRMS system at `hrms.aureolegroup.com`.

## Configuration

### Settings (`marketing_system/settings.py`)

The following settings have been added:

```python
# HRMS RBAC API Configuration
HRMS_RBAC_API_URL = 'https://hrms.aureolegroup.com/api/rbac'
HRMS_RBAC_EXEMPT_URLS = [
    '/hrms-login/',
    '/hrms-logout/',
    '/static/',
    '/media/',
    '/admin/',
]
```

### Middleware

The `HRMSRBACMiddleware` has been added to check authentication for all protected views. It automatically redirects unauthenticated users to the login page.

## API Base URL

All API calls are made to:
```
https://hrms.aureolegroup.com/api/rbac
```

## Authentication Flow

1. **Login**: User submits credentials at `/hrms-login/`
2. **API Call**: System calls `POST /api/rbac/login/` with username and password
3. **Token Storage**: On success, token is stored in session as `hrms_rbac_token`
4. **User Info**: User information, roles, and permissions are stored in session
5. **Redirect**: User is redirected to dashboard or requested page

## Usage

### Login View

Access the login page at:
```
/hrms-login/
```

### Logout

Access logout at:
```
/hrms-logout/
```

### Using Permissions in Views

#### Option 1: Using the Decorator

```python
from marketing_app.hrms_rbac import require_hrms_permission

@require_hrms_permission('marketing.view')
def my_view(request):
    # View code here
    pass
```

#### Option 2: Manual Permission Check

```python
from marketing_app.hrms_rbac import get_rbac_client

def my_view(request):
    client = get_rbac_client(request)
    
    if client.check_permission('marketing.create'):
        # User has permission
        pass
    else:
        # User doesn't have permission
        return HttpResponseForbidden()
```

### Getting User Information

```python
from marketing_app.hrms_rbac import get_rbac_client

def my_view(request):
    client = get_rbac_client(request)
    user_info = client.get_user_info()
    
    # Access user data
    user = user_info.get('user')
    employee = user_info.get('employee')
    roles = user_info.get('roles', [])
    permissions = user_info.get('permissions', [])
```

## API Endpoints Used

### 1. Login
- **Endpoint**: `POST /api/rbac/login/`
- **Request**: `{"username": "...", "password": "..."}`
- **Response**: Token, user info, roles, permissions

### 2. Logout
- **Endpoint**: `POST /api/rbac/logout/`
- **Headers**: `Authorization: Token <token>`
- **Response**: Success confirmation

### 3. Check Permission
- **Endpoint**: `POST /api/rbac/check-permission/`
- **Headers**: `Authorization: Token <token>`
- **Request**: `{"permission": "permission.code"}`
- **Response**: `{"has_permission": true/false}`

### 4. Check Multiple Permissions
- **Endpoint**: `POST /api/rbac/check-permissions/`
- **Headers**: `Authorization: Token <token>`
- **Request**: `{"permissions": ["perm1", "perm2"]}`
- **Response**: `{"permissions": {"perm1": true, "perm2": false}}`

### 5. Get User Info
- **Endpoint**: `GET /api/rbac/user/info/`
- **Headers**: `Authorization: Token <token>`
- **Response**: Complete user information with roles and permissions

## Session Storage

The following data is stored in the Django session:

- `hrms_rbac_token`: Authentication token for API calls
- `hrms_user_info`: Complete user information from login response
- `username`: Username for quick access

## Error Handling

The system handles various error scenarios:

1. **Connection Errors**: Logged and user-friendly error messages displayed
2. **Invalid Credentials**: Clear error message shown to user
3. **Token Expiration**: User redirected to login
4. **Permission Denied**: 403 error page shown

## Security Considerations

1. **HTTPS**: All API calls use HTTPS (verify=True)
2. **Token Storage**: Tokens stored in server-side session (not cookies)
3. **Timeout**: API requests have 10-second timeout
4. **Error Logging**: All errors are logged for debugging

## Testing

To test the integration:

1. Start the Django development server
2. Navigate to `/hrms-login/`
3. Enter valid HRMS credentials
4. Verify successful login and redirect
5. Check that protected views require authentication
6. Test permission checks on views

## Troubleshooting

### Connection Errors

If you see connection errors:
- Verify the HRMS API URL is correct: `https://hrms.aureolegroup.com/api/rbac`
- Check network connectivity
- Verify SSL certificate is valid

### Authentication Fails

If authentication fails:
- Verify credentials are correct
- Check HRMS API is accessible
- Review server logs for detailed error messages

### Permission Checks Fail

If permission checks fail:
- Verify user has the required permissions in HRMS
- Check token is valid (not expired)
- Review API response in logs

## Files Modified

1. `marketing_system/settings.py` - Added HRMS configuration
2. `marketing_app/hrms_rbac.py` - Updated API client with correct base URL
3. `marketing_app/hrms_auth_views.py` - Updated login/logout views
4. `marketing_app/hrms_middleware.py` - Updated exempt URLs
5. `marketing_system/urls.py` - Added HRMS login/logout routes
6. `requirements.txt` - Added requests library

## Next Steps

1. Update views to use HRMS permission decorators where needed
2. Add permission checks to sensitive operations
3. Test all authentication flows
4. Configure appropriate permissions in HRMS system

