"""
Context processors to make permissions available in all templates
"""
from marketing_app.permissions import check_permission, get_user_permissions


class PermissionChecker:
    """
    Wrapper class to make permission checking callable in templates
    """
    def __init__(self, request):
        self.request = request
    
    def __call__(self, permission_code):
        return check_permission(self.request, permission_code)


def permissions(request):
    """
    Add permission checking functions to template context
    
    Usage in template:
        {% if has_permission 'marketing.campaign.view' %}
            ...
        {% endif %}
    """
    if not request.session.get('hrms_rbac_token'):
        return {
            'user_permissions': [],
            'has_permission': PermissionChecker(None),
        }
    
    user_perms = get_user_permissions(request)
    
    return {
        'user_permissions': user_perms,
        'has_permission': PermissionChecker(request),
    }

