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
        self.base_url = base_url or getattr(settings, 'HRMS_RBAC_API_URL', 'http://localhost:8000/api/rbac')
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
                timeout=10
            )
            data = response.json()
            
            if data.get('success'):
                self.token = data['token']
                self.user_info = data
                logger.info(f"User {username} authenticated successfully via HRMS RBAC")
                return data
            else:
                logger.warning(f"Authentication failed for {username}: {data.get('error')}")
                return None
        except Exception as e:
            logger.error(f"HRMS RBAC login error: {str(e)}")
            return None
    
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
                headers={'Authorization': f'Token {self.token}'},
                json={'permission': permission_code},
                timeout=10
            )
            data = response.json()
            return data.get('has_permission', False)
        except Exception as e:
            logger.error(f"Permission check error: {str(e)}")
            return False
    
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
                headers={'Authorization': f'Token {self.token}'},
                json={'permissions': permissions},
                timeout=10
            )
            data = response.json()
            return data.get('permissions', {})
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
                headers={'Authorization': f'Token {self.token}'},
                timeout=10
            )
            data = response.json()
            if data.get('success'):
                return data
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
                headers={'Authorization': f'Token {self.token}'},
                timeout=10
            )
            self.token = None
            self.user_info = None
            return True
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return False


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
                return JsonResponse({
                    'success': False,
                    'error': 'Authentication required'
                }, status=401)
            
            # Check permission
            client = HRMSRBACClient()
            client.token = token
            
            if not client.check_permission(permission_code):
                logger.warning(
                    f"Permission denied: {request.user} tried to access "
                    f"{view_func.__name__} without {permission_code}"
                )
                return JsonResponse({
                    'success': False,
                    'error': f'Permission denied. Required: {permission_code}'
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
