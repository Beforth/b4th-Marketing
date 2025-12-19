"""
HRMS RBAC Integration Module for b4th-Marketing
Provides authentication and permission checking via HRMS RBAC API
"""
import requests
import logging
from functools import wraps
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)


class HRMSRBACClient:
    """
    Client for interacting with HRMS RBAC API
    """
    def __init__(self, base_url=None):
        self.base_url = base_url or getattr(settings, 'HRMS_RBAC_API_URL', 'https://hrms.aureolegroup.com/api/rbac')
        self.token = None
        self.user_info = None
    
    def login(self, username, password):
        """
        Authenticate user via HRMS RBAC API
        
        Returns:
            dict: User info, roles, and permissions
        """
        try:
            response = requests.post(
                f'{self.base_url}/login/',
                json={'username': username, 'password': password},
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                timeout=10,
                verify=True  # Verify SSL certificate
            )
            
            # Try to parse JSON response regardless of status code
            try:
                data = response.json()
            except ValueError:
                # If response is not JSON, create error response
                data = {
                    'success': False,
                    'error': f'Invalid response format. Status: {response.status_code}'
                }
            
            # Check if request was successful
            if response.status_code == 200 and data.get('success'):
                self.token = data.get('token')
                self.user_info = data
                logger.info(f"User {username} authenticated successfully via HRMS RBAC")
                return data
            else:
                # Handle error responses (401, 400, etc.)
                error_msg = data.get('error', f'Authentication failed. Status: {response.status_code}')
                logger.warning(f"Authentication failed for {username}: {error_msg}")
                return {'success': False, 'error': error_msg}
                
        except requests.exceptions.Timeout:
            logger.error(f"HRMS RBAC login timeout for {username}")
            return {'success': False, 'error': 'Connection timeout. Please try again.'}
        except requests.exceptions.ConnectionError as e:
            logger.error(f"HRMS RBAC connection error: {str(e)}")
            return {'success': False, 'error': 'Cannot connect to HRMS server. Please check your connection.'}
        except requests.exceptions.RequestException as e:
            logger.error(f"HRMS RBAC login error: {str(e)}")
            return {'success': False, 'error': f'Connection error: {str(e)}'}
        except Exception as e:
            logger.error(f"HRMS RBAC login error: {str(e)}")
            return {'success': False, 'error': f'Unexpected error: {str(e)}'}
    
    def check_permission(self, permission_code):
        """
        Check if current user has specific permission
        
        Args:
            permission_code (str): Permission code (e.g., 'employee.view')
        
        Returns:
            bool: True if user has permission
        """
        if not self.token:
            return False
        
        try:
            response = requests.post(
                f'{self.base_url}/check-permission/',
                headers={
                    'Authorization': f'Token {self.token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                json={'permission': permission_code},
                timeout=10,
                verify=True  # Verify SSL certificate
            )
            response.raise_for_status()
            data = response.json()
            return data.get('has_permission', False)
        except requests.exceptions.ConnectionError as e:
            logger.error(f"HRMS RBAC connection error (server may be down): {str(e)}")
            raise  # Re-raise to let caller handle it
        except requests.exceptions.Timeout:
            logger.error(f"HRMS RBAC timeout while checking permission: {permission_code}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Permission check error for {permission_code}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error checking permission {permission_code}: {str(e)}")
            raise
    
    def check_multiple_permissions(self, permissions):
        """
        Check multiple permissions at once
        
        Args:
            permissions (list): List of permission codes
        
        Returns:
            dict: Permission code -> bool mapping
        """
        if not self.token:
            return {perm: False for perm in permissions}
        
        try:
            response = requests.post(
                f'{self.base_url}/check-permissions/',
                headers={
                    'Authorization': f'Token {self.token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                json={'permissions': permissions},
                timeout=10,
                verify=True  # Verify SSL certificate
            )
            response.raise_for_status()
            data = response.json()
            return data.get('permissions', {})
        except requests.exceptions.RequestException as e:
            logger.error(f"Multiple permission check error: {str(e)}")
            return {perm: False for perm in permissions}
        except Exception as e:
            logger.error(f"Multiple permission check error: {str(e)}")
            return {perm: False for perm in permissions}
    
    def get_user_info(self):
        """
        Get complete user information
        
        Returns:
            dict: User info with roles and permissions
        """
        if not self.token:
            return None
        
        try:
            response = requests.get(
                f'{self.base_url}/user/info/',
                headers={
                    'Authorization': f'Token {self.token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                timeout=10,
                verify=True  # Verify SSL certificate
            )
            response.raise_for_status()
            data = response.json()
            if data.get('success'):
                return data
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"HRMS RBAC connection error (server may be down): {str(e)}")
            return None
        except requests.exceptions.Timeout:
            logger.error(f"HRMS RBAC timeout while getting user info")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Get user info error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Get user info error: {str(e)}")
            return None
    
    def logout(self):
        """
        Logout and invalidate token
        """
        if not self.token:
            return True
        
        try:
            response = requests.post(
                f'{self.base_url}/logout/',
                headers={
                    'Authorization': f'Token {self.token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                timeout=10,
                verify=True  # Verify SSL certificate
            )
            response.raise_for_status()
            self.token = None
            self.user_info = None
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Logout error: {str(e)}")
            # Even if logout fails, clear local state
            self.token = None
            self.user_info = None
            return True
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            self.token = None
            self.user_info = None
            return True


def hrms_login_required(view_func):
    """
    Decorator to require HRMS authentication for a view
    
    Usage:
        @hrms_login_required
        def my_view(request):
            pass
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user has HRMS token
        token = request.session.get('hrms_rbac_token')
        if not token:
            from django.shortcuts import redirect
            from django.urls import reverse
            return redirect(f"{reverse('hrms_login')}?next={request.path}")
        
        return view_func(request, *args, **kwargs)
    return wrapper


def require_hrms_permission(permission_code):
    """
    Decorator to require HRMS permission for a view
    
    Usage:
        @require_hrms_permission('employee.view')
        def my_view(request):
            pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get RBAC client from session
            token = request.session.get('hrms_rbac_token')
            if not token:
                from django.shortcuts import redirect
                from django.urls import reverse
                return redirect(f"{reverse('hrms_login')}?next={request.path}")
            
            # Check permission
            client = HRMSRBACClient()
            client.token = token
            
            if not client.check_permission(permission_code):
                logger.warning(
                    f"Permission denied: User tried to access "
                    f"{view_func.__name__} without {permission_code}"
                )
                from django.http import HttpResponseForbidden
                from django.shortcuts import render
                return render(request, 'marketing_app/403_permission_denied.html', {
                    'permission': permission_code,
                    'view_name': view_func.__name__
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def get_rbac_client(request):
    """
    Get RBAC client from request session
    
    Args:
        request: Django request object
    
    Returns:
        HRMSRBACClient: Initialized client with token
    """
    client = HRMSRBACClient()
    token = request.session.get('hrms_rbac_token')
    if token:
        client.token = token
        client.user_info = request.session.get('hrms_user_info')
    return client
