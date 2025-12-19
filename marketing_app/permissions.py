"""
Permission helpers for Marketing App using HRMS RBAC
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse
from .hrms_rbac import HRMSRBACClient
import logging

logger = logging.getLogger(__name__)


def get_rbac_client(request):
    """
    Get HRMS RBAC client from request session
    
    Returns:
        HRMSRBACClient: Client instance with token set
    """
    token = request.session.get('hrms_rbac_token')
    if not token:
        return None
    
    client = HRMSRBACClient()
    client.token = token
    return client


def check_permission(request, permission_code):
    """
    Check if user has specific permission via HRMS RBAC
    
    Args:
        request: Django request object
        permission_code (str): Permission code to check (e.g., 'marketing.campaign.view')
    
    Returns:
        bool: True if user has permission, False otherwise
    """
    client = get_rbac_client(request)
    if not client:
        logger.warning(f"No HRMS token found for permission check: {permission_code}")
        return False
    
    try:
        return client.check_permission(permission_code)
    except Exception as e:
        error_msg = str(e)
        # Check if it's a connection error
        if 'Connection refused' in error_msg or 'Max retries' in error_msg:
            logger.error(f"HRMS server unavailable for permission check {permission_code}: {error_msg}")
        else:
            logger.error(f"Permission check error for {permission_code}: {error_msg}")
        # On API error, default to False (deny access) for security
        return False


def check_multiple_permissions(request, permission_codes):
    """
    Check multiple permissions at once
    
    Args:
        request: Django request object
        permission_codes (list): List of permission codes to check
    
    Returns:
        dict: Permission code -> bool mapping
    """
    client = get_rbac_client(request)
    if not client:
        return {perm: False for perm in permission_codes}
    
    return client.check_multiple_permissions(permission_codes)


def get_user_permissions(request):
    """
    Get all permissions for the current user
    
    Args:
        request: Django request object
    
    Returns:
        list: List of permission codes user has
    """
    client = get_rbac_client(request)
    if not client:
        return []
    
    user_info = client.get_user_info()
    if user_info and user_info.get('success'):
        permissions = user_info.get('permissions', [])
        return [perm.get('code') for perm in permissions if perm.get('code')]
    
    return []


def get_user_accessible_pages(request):
    """
    Get a list of pages the user has permission to access
    Returns URL name or path that user can access
    """
    user_perms = get_user_permissions(request)
    
    # Map permissions to page URLs
    accessible_pages = []
    
    if check_permission(request, 'marketing.campaign.view'):
        accessible_pages.append(('marketing:dashboard', 'Dashboard'))
    if check_permission(request, 'marketing.customer.view'):
        accessible_pages.append(('marketing:customer_list', 'Customers'))
    if check_permission(request, 'marketing.lead.view'):
        accessible_pages.append(('marketing:lead_list', 'Leads'))
    if check_permission(request, 'marketing.visit.view'):
        accessible_pages.append(('marketing:visit_list', 'Visits'))
    if check_permission(request, 'marketing.reports.view'):
        accessible_pages.append(('marketing:campaign_analytics', 'Reports'))
    
    return accessible_pages


def require_permission(permission_code, redirect_url=None, raise_exception=False):
    """
    Decorator to require specific permission for a view
    
    Usage:
        @require_permission('marketing.campaign.view')
        def my_view(request):
            pass
    
    Args:
        permission_code (str): Permission code required
        redirect_url (str): URL to redirect if permission denied (default: show 403 page or redirect to accessible page)
        raise_exception (bool): If True, raise 403 instead of redirecting
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Check if user has HRMS token
            token = request.session.get('hrms_rbac_token')
            if not token:
                return redirect(f"{reverse('hrms_login')}?next={request.path}")
            
            # Check permission
            try:
                has_perm = check_permission(request, permission_code)
            except Exception as e:
                # If permission check fails (e.g., API error), log and show error page
                logger.error(f"Permission check error: {str(e)}")
                has_perm = False
            
            if not has_perm:
                logger.warning(
                    f"Permission denied: User tried to access "
                    f"{view_func.__name__} without {permission_code}"
                )
                
                if raise_exception:
                    from django.shortcuts import render
                    return render(request, 'marketing_app/403_permission_denied.html', {
                        'permission': permission_code,
                        'view_name': view_func.__name__
                    }, status=403)
                
                messages.error(
                    request,
                    f"You don't have permission to access this resource. "
                    f"Required permission: {permission_code}"
                )
                
                if redirect_url:
                    return redirect(redirect_url)
                
                # Try to find a page user has permission for
                accessible_pages = get_user_accessible_pages(request)
                if accessible_pages:
                    # Redirect to first accessible page
                    return redirect(accessible_pages[0][0])
                else:
                    # No accessible pages, show 403 page
                    from django.shortcuts import render
                    return render(request, 'marketing_app/403_permission_denied.html', {
                        'permission': permission_code,
                        'view_name': view_func.__name__
                    }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_any_permission(permission_codes, redirect_url=None, raise_exception=False):
    """
    Decorator to require any of the specified permissions
    
    Usage:
        @require_any_permission(['marketing.campaign.view', 'marketing.campaign.edit'])
        def my_view(request):
            pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            token = request.session.get('hrms_rbac_token')
            if not token:
                return redirect(f"{reverse('hrms_login')}?next={request.path}")
            
            try:
                permissions = check_multiple_permissions(request, permission_codes)
                has_any = any(permissions.values())
            except Exception as e:
                logger.error(f"Permission check error: {str(e)}")
                has_any = False
            
            if not has_any:
                logger.warning(
                    f"Permission denied: User tried to access "
                    f"{view_func.__name__} without any of {permission_codes}"
                )
                
                if raise_exception:
                    from django.shortcuts import render
                    return render(request, 'marketing_app/403_permission_denied.html', {
                        'permission': ', '.join(permission_codes),
                        'view_name': view_func.__name__
                    }, status=403)
                
                messages.error(
                    request,
                    f"You don't have permission to access this resource. "
                    f"Required permissions: {', '.join(permission_codes)}"
                )
                
                if redirect_url:
                    return redirect(redirect_url)
                
                # Try to find a page user has permission for
                accessible_pages = get_user_accessible_pages(request)
                if accessible_pages:
                    return redirect(accessible_pages[0][0])
                else:
                    from django.shortcuts import render
                    return render(request, 'marketing_app/403_permission_denied.html', {
                        'permission': ', '.join(permission_codes),
                        'view_name': view_func.__name__
                    }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_all_permissions(permission_codes, redirect_url=None, raise_exception=False):
    """
    Decorator to require all of the specified permissions
    
    Usage:
        @require_all_permissions(['marketing.campaign.view', 'marketing.campaign.edit'])
        def my_view(request):
            pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            token = request.session.get('hrms_rbac_token')
            if not token:
                return redirect(f"{reverse('hrms_login')}?next={request.path}")
            
            try:
                permissions = check_multiple_permissions(request, permission_codes)
                has_all = all(permissions.values())
            except Exception as e:
                logger.error(f"Permission check error: {str(e)}")
                has_all = False
            
            if not has_all:
                logger.warning(
                    f"Permission denied: User tried to access "
                    f"{view_func.__name__} without all of {permission_codes}"
                )
                
                if raise_exception:
                    from django.shortcuts import render
                    return render(request, 'marketing_app/403_permission_denied.html', {
                        'permission': ', '.join(permission_codes),
                        'view_name': view_func.__name__
                    }, status=403)
                
                messages.error(
                    request,
                    f"You don't have permission to access this resource. "
                    f"Required permissions: {', '.join(permission_codes)}"
                )
                
                if redirect_url:
                    return redirect(redirect_url)
                
                # Try to find a page user has permission for
                accessible_pages = get_user_accessible_pages(request)
                if accessible_pages:
                    return redirect(accessible_pages[0][0])
                else:
                    from django.shortcuts import render
                    return render(request, 'marketing_app/403_permission_denied.html', {
                        'permission': ', '.join(permission_codes),
                        'view_name': view_func.__name__
                    }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# Marketing-specific permission codes
MARKETING_PERMISSIONS = {
    # Campaign Management
    'campaign.view': 'marketing.campaign.view',
    'campaign.create': 'marketing.campaign.create',
    'campaign.edit': 'marketing.campaign.edit',
    'campaign.delete': 'marketing.campaign.delete',
    
    # Lead Management
    'lead.view': 'marketing.lead.view',
    'lead.create': 'marketing.lead.create',
    'lead.edit': 'marketing.lead.edit',
    'lead.delete': 'marketing.lead.delete',
    'lead.import': 'marketing.lead.import',
    
    # Customer Management
    'customer.view': 'marketing.customer.view',
    'customer.create': 'marketing.customer.create',
    'customer.edit': 'marketing.customer.edit',
    'customer.delete': 'marketing.customer.delete',
    'customer.import': 'marketing.customer.import',
    
    # Visit Management
    'visit.view': 'marketing.visit.view',
    'visit.create': 'marketing.visit.create',
    'visit.edit': 'marketing.visit.edit',
    'visit.delete': 'marketing.visit.delete',
    
    # Reports & Analytics
    'reports.view': 'marketing.reports.view',
    'reports.export': 'marketing.reports.export',
    
    # Settings
    'settings.view': 'marketing.settings.view',
    'settings.edit': 'marketing.settings.edit',
}

