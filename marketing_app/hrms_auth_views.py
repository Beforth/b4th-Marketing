"""
Authentication views for HRMS RBAC integration
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .hrms_rbac import HRMSRBACClient
import logging

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def hrms_login(request):
    """
    Login view using HRMS RBAC authentication
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Username and password are required')
            return render(request, 'marketing_app/hrms_login.html')
        
        # Authenticate via HRMS RBAC
        client = HRMSRBACClient()
        result = client.login(username, password)
        
        if result and result.get('success'):
            # Store token and user info in session
            token = result.get('token')
            if token:
                # Store session data
                request.session['hrms_rbac_token'] = token
                request.session['hrms_user_info'] = result
                request.session['username'] = username
                
                # Mark session as modified and save
                request.session.modified = True
                
                # Force session save
                try:
                    request.session.save()
                    # Verify session was saved
                    saved_token = request.session.get('hrms_rbac_token')
                    if saved_token == token:
                        logger.info(f"Session saved successfully for user {username}. Token verified.")
                    else:
                        logger.error(f"Session save verification failed for {username}")
                except Exception as e:
                    logger.error(f"Error saving session: {str(e)}")
                
                # Get user name from response
                user_data = result.get('user', {})
                first_name = user_data.get('first_name', username)
                employee_data = result.get('employee', {})
                if employee_data:
                    first_name = employee_data.get('first_name', first_name)
                
                messages.success(request, f"Welcome, {first_name}!")
                logger.info(f"User {username} logged in successfully via HRMS RBAC. Token: {token[:10]}...")
                
                # Redirect to dashboard or next page
                next_url = request.GET.get('next', '/dashboard/')
                # Ensure next_url is safe and doesn't redirect to login
                if next_url == '/hrms-login/' or next_url.startswith('/hrms-login'):
                    next_url = '/dashboard/'
                logger.info(f"Redirecting user {username} to: {next_url}")
                return redirect(next_url)
            else:
                messages.error(request, 'Login successful but no token received')
                logger.error(f"Login succeeded but no token for {username}")
        else:
            error_msg = result.get('error', 'Invalid credentials or HRMS authentication failed') if result else 'Connection error'
            messages.error(request, error_msg)
            logger.warning(f"Failed login attempt for {username}: {error_msg}")
    
    return render(request, 'marketing_app/hrms_login.html')


@require_http_methods(["GET", "POST"])
def hrms_logout(request):
    """
    Logout view - invalidates HRMS token
    """
    token = request.session.get('hrms_rbac_token')
    
    if token:
        client = HRMSRBACClient()
        client.token = token
        client.logout()
    
    # Clear session
    request.session.flush()
    messages.success(request, 'Logged out successfully')
    logger.info(f"User logged out")
    
    return redirect('hrms_login')


def user_profile(request):
    """
    Display user profile with HRMS roles and permissions
    """
    token = request.session.get('hrms_rbac_token')
    
    if not token:
        messages.error(request, 'Please login first')
        return redirect('hrms_login')
    
    client = HRMSRBACClient()
    client.token = token
    user_info = client.get_user_info()
    
    if not user_info or not user_info.get('success'):
        messages.error(request, 'Failed to fetch user information')
        return redirect('hrms_login')
    
    context = {
        'user': user_info.get('user'),
        'employee': user_info.get('employee'),
        'roles': user_info.get('roles', []),
        'permissions': user_info.get('permissions', []),
        'permission_count': user_info.get('permission_count', 0)
    }
    
    return render(request, 'marketing_app/user_profile.html', context)
