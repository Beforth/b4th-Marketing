"""
Helper functions to filter querysets based on user permissions
"""
from marketing_app.permissions import check_permission, get_user_permissions


def filter_campaigns_by_permission(request, campaigns):
    """
    Filter campaigns based on user permissions
    
    Args:
        request: Django request object
        campaigns: Campaign queryset
    
    Returns:
        Filtered queryset based on permissions
    """
    user_perms = get_user_permissions(request)
    
    # If user has view permission, return all campaigns
    if check_permission(request, 'marketing.campaign.view'):
        return campaigns
    
    # Otherwise, return empty queryset
    return campaigns.none()


def filter_leads_by_permission(request, leads):
    """
    Filter leads based on user permissions
    
    Args:
        request: Django request object
        leads: Lead queryset
    
    Returns:
        Filtered queryset based on permissions
    """
    if check_permission(request, 'marketing.lead.view'):
        return leads
    
    return leads.none()


def filter_customers_by_permission(request, customers):
    """
    Filter customers based on user permissions
    
    Args:
        request: Django request object
        customers: Customer queryset
    
    Returns:
        Filtered queryset based on permissions
    """
    if check_permission(request, 'marketing.customer.view'):
        return customers
    
    return customers.none()


def filter_visits_by_permission(request, visits):
    """
    Filter visits based on user permissions
    
    Args:
        request: Django request object
        visits: Visit queryset
    
    Returns:
        Filtered queryset based on permissions
    """
    if check_permission(request, 'marketing.visit.view'):
        return visits
    
    return visits.none()


def can_create_campaign(request):
    """Check if user can create campaigns"""
    return check_permission(request, 'marketing.campaign.create')


def can_edit_campaign(request):
    """Check if user can edit campaigns"""
    return check_permission(request, 'marketing.campaign.edit')


def can_delete_campaign(request):
    """Check if user can delete campaigns"""
    return check_permission(request, 'marketing.campaign.delete')


def can_create_lead(request):
    """Check if user can create leads"""
    return check_permission(request, 'marketing.lead.create')


def can_edit_lead(request):
    """Check if user can edit leads"""
    return check_permission(request, 'marketing.lead.edit')


def can_delete_lead(request):
    """Check if user can delete leads"""
    return check_permission(request, 'marketing.lead.delete')


def can_create_customer(request):
    """Check if user can create customers"""
    return check_permission(request, 'marketing.customer.create')


def can_edit_customer(request):
    """Check if user can edit customers"""
    return check_permission(request, 'marketing.customer.edit')


def can_delete_customer(request):
    """Check if user can delete customers"""
    return check_permission(request, 'marketing.customer.delete')


def can_view_reports(request):
    """Check if user can view reports"""
    return check_permission(request, 'marketing.reports.view')


def can_export_reports(request):
    """Check if user can export reports"""
    return check_permission(request, 'marketing.reports.export')

