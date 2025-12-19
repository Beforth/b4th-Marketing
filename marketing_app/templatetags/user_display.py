"""
Template filters for displaying user information from HRMS or Django User
"""
from django import template

register = template.Library()


@register.filter
def user_display(obj, field_prefix='assigned_to'):
    """
    Display user information from HRMS fields or Django User ForeignKey
    
    Usage:
        {{ lead|user_display:"assigned_to" }}
        {{ campaign|user_display:"created_by" }}
    """
    if obj is None:
        return "Unassigned"
    
    # Try HRMS user fields first
    full_name = getattr(obj, f'{field_prefix}_full_name', None)
    if full_name:
        return full_name
    
    username = getattr(obj, f'{field_prefix}_username', None)
    if username:
        return username
    
    # Fall back to Django User ForeignKey
    user = getattr(obj, field_prefix, None)
    if user:
        if hasattr(user, 'get_full_name'):
            full_name = user.get_full_name()
            if full_name:
                return full_name
        if hasattr(user, 'username'):
            return user.username
    
    return "Unassigned"


@register.filter
def user_email(obj, field_prefix='assigned_to'):
    """
    Get user email from HRMS fields or Django User ForeignKey
    """
    if obj is None:
        return ""
    
    # Try HRMS user fields first
    email = getattr(obj, f'{field_prefix}_email', None)
    if email:
        return email
    
    # Fall back to Django User ForeignKey
    user = getattr(obj, field_prefix, None)
    if user and hasattr(user, 'email'):
        return user.email
    
    return ""

