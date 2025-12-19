"""
Custom fields and mixins for storing HRMS user information
instead of Django User ForeignKeys
"""
from django.db import models


class HRMSUserInfoMixin(models.Model):
    """
    Mixin to add HRMS user information fields to models
    Use this instead of ForeignKey(User) for HRMS authentication
    """
    # HRMS User Information (from HRMS RBAC API)
    user_id = models.IntegerField(null=True, blank=True, help_text="HRMS User ID")
    username = models.CharField(max_length=150, blank=True, help_text="HRMS Username")
    user_email = models.EmailField(blank=True, help_text="HRMS User Email")
    user_full_name = models.CharField(max_length=255, blank=True, help_text="HRMS User Full Name")
    user_info = models.JSONField(default=dict, blank=True, help_text="Complete HRMS user info as JSON")
    
    class Meta:
        abstract = True
    
    @property
    def created_by_user(self):
        """Return user info as dict for templates"""
        return {
            'id': self.user_id,
            'username': self.username,
            'email': self.user_email,
            'full_name': self.user_full_name,
        }
    
    def set_user_info(self, user_data):
        """
        Set user information from HRMS user data
        
        Args:
            user_data: Dict with user info from HRMS API
        """
        if isinstance(user_data, dict):
            self.user_id = user_data.get('id')
            self.username = user_data.get('username', '')
            self.user_email = user_data.get('email', '')
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '')
            self.user_full_name = f"{first_name} {last_name}".strip()
            self.user_info = user_data


def get_user_info_from_request(request):
    """
    Extract user information from request session (HRMS authentication)
    
    Args:
        request: Django request object
    
    Returns:
        dict: User information dict with id, username, email, first_name, last_name
    """
    user_info = request.session.get('hrms_user_info', {})
    user_data = user_info.get('user', {})
    
    if not user_data:
        # Fallback to employee data
        employee_data = user_info.get('employee', {})
        if employee_data:
            return {
                'id': employee_data.get('id'),
                'username': request.session.get('username', ''),
                'email': employee_data.get('email', ''),
                'first_name': employee_data.get('first_name', ''),
                'last_name': employee_data.get('last_name', ''),
            }
        return {}
    
    return {
        'id': user_data.get('id'),
        'username': user_data.get('username', ''),
        'email': user_data.get('email', ''),
        'first_name': user_data.get('first_name', ''),
        'last_name': user_data.get('last_name', ''),
    }

