"""
Middleware for HRMS RBAC authentication
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class HRMSRBACMiddleware:
    """
    Middleware to check HRMS RBAC authentication for protected views
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that don't require authentication
        self.exempt_urls = getattr(settings, 'HRMS_RBAC_EXEMPT_URLS', [
            '/hrms-login/',
            '/hrms-logout/',
            '/static/',
            '/media/',
            '/admin/',
        ])
    
    def __call__(self, request):
        # Check if URL is exempt
        path = request.path
        is_exempt = any(path.startswith(url) for url in self.exempt_urls)
        
        # Check if user has HRMS token
        token = request.session.get('hrms_rbac_token')
        
        # Helper function to create HRMSUser
        def create_hrms_user(user_data, employee_data=None):
            class HRMSUser:
                def __init__(self, user_data, employee_data=None):
                    self.id = user_data.get('id')
                    self.username = user_data.get('username', '')
                    self.first_name = user_data.get('first_name', '')
                    self.last_name = user_data.get('last_name', '')
                    self.email = user_data.get('email', '')
                    self.is_authenticated = True
                    self.is_active = user_data.get('is_active', True)
                    self.is_staff = user_data.get('is_staff', False)
                    self.is_superuser = user_data.get('is_superuser', False)
                    self.employee_data = employee_data
                    
                def get_full_name(self):
                    name = f"{self.first_name} {self.last_name}".strip()
                    return name if name else self.username
                
                def __str__(self):
                    return self.username
            return HRMSUser(user_data, employee_data)
        
        if not is_exempt:
            # Protected URL - require authentication
            if not token:
                logger.debug(f"No HRMS token found for {path}, redirecting to login. Session keys: {list(request.session.keys())}")
                return redirect(f"{reverse('hrms_login')}?next={path}")
            else:
                # Token exists - set request.user
                user_info = request.session.get('hrms_user_info', {})
                if user_info:
                    user_data = user_info.get('user', {})
                    employee_data = user_info.get('employee')
                    if user_data:
                        request.user = create_hrms_user(user_data, employee_data)
                        request.hrms_authenticated = True
                        logger.debug(f"Set request.user for {path}: {request.user.username}, authenticated: {request.user.is_authenticated}")
                    else:
                        # If no user data, redirect to login
                        logger.warning(f"Token exists but no user data for {path}")
                        return redirect(f"{reverse('hrms_login')}?next={path}")
                else:
                    # Token exists but no user info - might be stale
                    logger.warning(f"Token exists but no user info for {path}. Session keys: {list(request.session.keys())}")
                    return redirect(f"{reverse('hrms_login')}?next={path}")
        elif token and path not in ['/hrms-login/', '/hrms-logout/']:
            # Exempt URL but user is authenticated - set request.user anyway
            user_info = request.session.get('hrms_user_info', {})
            if user_info:
                user_data = user_info.get('user', {})
                employee_data = user_info.get('employee')
                if user_data:
                    request.user = create_hrms_user(user_data, employee_data)
                    request.hrms_authenticated = True
        
        response = self.get_response(request)
        return response
