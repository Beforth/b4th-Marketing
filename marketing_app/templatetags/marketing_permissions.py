"""
Template tags for checking permissions in templates
"""
from django import template
from marketing_app.permissions import check_permission, get_user_permissions

register = template.Library()


@register.simple_tag(takes_context=True)
def has_permission(context, permission_code):
    """
    Check if user has specific permission
    
    Usage in template:
        {% has_permission 'marketing.campaign.view' as can_view_campaigns %}
        {% if can_view_campaigns %}
            <a href="/campaigns/">Campaigns</a>
        {% endif %}
    """
    request = context.get('request')
    if not request:
        return False
    
    return check_permission(request, permission_code)


@register.simple_tag(takes_context=True)
def user_permissions(context):
    """
    Get all permissions for current user
    
    Usage in template:
        {% user_permissions as permissions %}
        {% if 'marketing.campaign.view' in permissions %}
            ...
        {% endif %}
    """
    request = context.get('request')
    if not request:
        return []
    
    return get_user_permissions(request)


@register.filter
def has_perm(request, permission_code):
    """
    Filter to check permission in template
    
    Usage:
        {% if request|has_perm:'marketing.campaign.view' %}
            ...
        {% endif %}
    """
    if not request:
        return False
    
    from marketing_app.permissions import check_permission
    return check_permission(request, permission_code)

