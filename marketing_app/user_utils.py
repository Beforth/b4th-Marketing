"""
Utility functions to get Django User from HRMS authentication
"""
from django.contrib.auth import get_user_model

User = get_user_model()


def get_django_user(request):
    """
    Get the actual Django User instance from request
    
    Args:
        request: Django request object
    
    Returns:
        User: Django User instance or None
    """
    if not hasattr(request, 'user') or not request.user:
        return None
    
    # If it's already a Django User, return it
    if isinstance(request.user, User):
        return request.user
    
    # If it's an HRMSUser mock object, get the real user
    if hasattr(request.user, 'username'):
        try:
            # Get username from HRMS user info in session
            user_info = request.session.get('hrms_user_info', {})
            user_data = user_info.get('user', {})
            username = user_data.get('username') or request.user.username
            
            if username:
                return User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        except Exception:
            pass
    
    return None

