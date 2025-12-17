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
        ])
    
    def __call__(self, request):
        # Check if URL is exempt
        path = request.path
        is_exempt = any(path.startswith(url) for url in self.exempt_urls)
        
        if not is_exempt:
            # Check if user has HRMS token
            token = request.session.get('hrms_rbac_token')
            
            if not token:
                logger.debug(f"No HRMS token found for {path}, redirecting to login")
                return redirect(f"{reverse('hrms_login')}?next={path}")
        
        response = self.get_response(request)
        return response
