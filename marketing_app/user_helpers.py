"""
Helper functions to get and set user information from HRMS authentication
"""
from marketing_app.user_fields import get_user_info_from_request


def get_user_info_dict(request):
    """
    Get user information dict from request session
    
    Returns:
        dict: User info with id, username, email, first_name, last_name, full_name
    """
    user_data = get_user_info_from_request(request)
    
    if user_data:
        first_name = user_data.get('first_name', '')
        last_name = user_data.get('last_name', '')
        full_name = f"{first_name} {last_name}".strip()
        
        return {
            'user_id': user_data.get('id'),
            'username': user_data.get('username', ''),
            'email': user_data.get('email', ''),
            'first_name': first_name,
            'last_name': last_name,
            'full_name': full_name,
        }
    
    return {
        'user_id': None,
        'username': '',
        'email': '',
        'first_name': '',
        'last_name': '',
        'full_name': '',
    }


def set_user_info_on_model(instance, request, field_prefix='created_by'):
    """
    Set user information fields on a model instance
    
    Args:
        instance: Model instance
        request: Django request object
        field_prefix: Prefix for field names (e.g., 'created_by', 'assigned_to')
    
    Usage:
        lead = Lead()
        set_user_info_on_model(lead, request, 'assigned_to')
        lead.save()
    """
    user_info = get_user_info_dict(request)
    
    setattr(instance, f'{field_prefix}_user_id', user_info['user_id'])
    setattr(instance, f'{field_prefix}_username', user_info['username'])
    setattr(instance, f'{field_prefix}_email', user_info['email'])
    setattr(instance, f'{field_prefix}_full_name', user_info['full_name'])

