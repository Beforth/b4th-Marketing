from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    # Dashboard
    path('', views.marketing_dashboard, name='dashboard'),
    path('dashboard/', views.marketing_dashboard, name='marketing_dashboard'),
    
    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_registration, name='customer_create'),
    path('customers/register/', views.customer_registration, name='customer_registration'),
    path('customers/form/', views.customer_form, name='customer_form'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customers/regions/', views.customer_regions, name='customer_regions'),
    path('customers/import/', views.customer_import, name='customer_import'),
    
    # Leads
    path('leads/', views.lead_list, name='lead_list'),
    path('leads/create/', views.lead_generation, name='lead_create'),
    path('leads/generate/', views.lead_generation, name='lead_generation'),
    path('leads/form/', views.lead_form, name='lead_form'),
    path('leads/<int:lead_id>/', views.lead_detail, name='lead_detail'),
    path('leads/import/', views.lead_import, name='lead_import'),
    path('leads/scoring/', views.lead_scoring, name='lead_scoring'),
    
    # Inquiry Log
    path('inquiry-log/', views.inquiry_log_list, name='inquiry_log_list'),
    path('inquiry-log/create/', views.inquiry_log_create, name='inquiry_log_create'),
    path('inquiry-log/<int:pk>/', views.inquiry_log_detail, name='inquiry_log_detail'),
    path('inquiry-log/<int:pk>/edit/', views.inquiry_log_edit, name='inquiry_log_edit'),
    path('inquiry-log/<int:pk>/delete/', views.inquiry_log_delete, name='inquiry_log_delete'),
    
    # Visits
    path('visits/', views.visit_list, name='visit_list'),
    path('visits/create/', views.customer_visit, name='visit_create'),
    path('visits/record/', views.customer_visit, name='customer_visit'),
    path('visits/<int:visit_id>/', views.visit_detail, name='visit_detail'),
    path('visits/tracking/', views.visit_tracking, name='visit_tracking'),
    path('visits/reports/', views.visit_reports, name='visit_reports'),
    path('follow-ups/', views.follow_up_reminders, name='follow_up_reminders'),
    
    # Sales Process - Phase 4
    path('urs/', views.urs_list, name='urs_list'),
    path('urs/evaluate/', views.urs_evaluation, name='urs_evaluation'),
    path('urs/<int:urs_id>/', views.urs_detail, name='urs_detail'),
    path('ga-drawings/', views.ga_drawing_list, name='ga_drawing_list'),
    path('ga-drawings/create/', views.ga_drawing_create, name='ga_drawing_create'),
    path('quotations/', views.quotation_list, name='quotation_list'),
    path('quotations/create/', views.quotation_create, name='quotation_create'),
    path('quotations/<int:quotation_id>/', views.quotation_detail, name='quotation_detail'),
    path('technical-discussions/', views.technical_discussion_list, name='technical_discussion_list'),
    path('technical-discussions/record/', views.technical_discussion, name='technical_discussion'),
    path('negotiations/', views.negotiation_list, name='negotiation_list'),
    path('negotiations/create/', views.negotiation_create, name='negotiation_create'),
    
    # Quotation Revisions
    path('quotations/<int:quotation_id>/revisions/', views.quotation_revision_timeline, name='quotation_revision_timeline'),
    path('quotations/<int:quotation_id>/revisions/create/', views.create_quotation_revision, name='create_quotation_revision'),
    
    path('purchase-orders/', views.po_list, name='po_list'),
    path('purchase-orders/create/', views.po_create, name='po_create'),
    path('purchase-orders/<int:po_id>/', views.po_detail, name='po_detail'),
    
    # Payment Follow-ups
    path('payment-followups/', views.payment_followup_list, name='payment_followup_list'),
    path('payment-followups/dashboard/', views.payment_followup_dashboard, name='payment_followup_dashboard'),
    path('payment-followups/create/<int:po_id>/', views.payment_followup_create, name='payment_followup_create'),
    path('payment-followups/update/<int:followup_id>/', views.payment_followup_update, name='payment_followup_update'),
    
    # Production
    path('work-orders/', views.workorder_list, name='workorder_list'),
    path('work-orders/create/', views.workorder_create, name='workorder_create'),
    path('work-orders/<int:workorder_id>/', views.workorder_detail, name='workorder_detail'),
    path('production-planning/', views.production_planning, name='production_planning'),
    path('manufacturing/', views.manufacturing_list, name='manufacturing_list'),
    path('manufacturing/<int:manufacturing_id>/', views.manufacturing_detail, name='manufacturing_detail'),
    path('qc-tracking/', views.qc_tracking, name='qc_tracking'),
    path('qc-tracking/create/', views.qc_create, name='qc_create'),
    path('qc-tracking/export/', views.qc_export, name='qc_export'),
    path('dispatch/', views.dispatch_list, name='dispatch_list'),
    path('dispatch/<int:dispatch_id>/', views.dispatch_detail, name='dispatch_detail'),
    
    # Campaigns
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaigns/create/', views.campaign_create, name='campaign_create'),
    path('campaigns/form/', views.campaign_form, name='campaign_form'),
    path('campaigns/<int:campaign_id>/', views.campaign_detail, name='campaign_detail'),
    path('campaigns/analytics/', views.campaign_analytics, name='campaign_analytics'),
    
    # Exhibitions
    path('exhibitions/', views.exhibition_list, name='exhibition_list'),
    path('exhibitions/create/', views.exhibition_create, name='exhibition_create'),
    path('exhibitions/<int:exhibition_id>/', views.exhibition_detail, name='exhibition_detail'),
    path('exhibitions/planning/', views.exhibition_planning, name='exhibition_planning'),
    path('visitor-database/', views.visitor_database, name='visitor_database'),
    path('visitor-database/create/', views.visitor_create, name='visitor_create'),
    path('visitor-database/export/', views.visitor_export, name='visitor_export'),
    
    # Expenses
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/create/', views.expense_create, name='expense_create'),
    path('expenses/<int:expense_id>/', views.expense_detail, name='expense_detail'),
    path('expenses/approval/', views.expense_approval, name='expense_approval'),
    path('expenses/reports/', views.expense_reports, name='expense_reports'),
    path('expenses/export/', views.expense_export, name='expense_export'),
    
    # Reports
    path('reports/daily/', views.daily_reports, name='daily_reports'),
    path('reports/daily-status/', views.daily_status_report, name='daily_status_report'),
    path('reports/monthly/', views.monthly_reports, name='monthly_reports'),
    path('reports/performance/', views.performance_analytics, name='performance_analytics'),
    path('reports/export/', views.export_data, name='export_data'),
    
    # MIS Reports
    path('mis/visitor-attendance/', views.visitor_attendance, name='visitor_attendance'),
    path('mis/ongoing-projects/', views.ongoing_projects, name='ongoing_projects'),
    path('mis/region-targets/', views.region_targets, name='region_targets'),
    
    # Phase 6: Tracking & Analytics
    path('tracking/live-gps/', views.live_gps_tracking, name='live_gps_tracking'),
    path('tracking/progress-dashboard/', views.progress_tracking_dashboard, name='progress_tracking_dashboard'),
    path('analytics/detailed/', views.performance_analytics_detailed, name='performance_analytics_detailed'),
    path('export/advanced/', views.export_data_advanced, name='export_data_advanced'),
    
    # Phase 7: Exhibition Management
    path('exhibitions/planning/', views.exhibition_planning_interface, name='exhibition_planning_interface'),
    path('exhibitions/vendors/', views.vendor_management, name='vendor_management'),
    path('exhibitions/visitors/', views.visitor_database_management, name='visitor_database_management'),
    path('exhibitions/expenses/', views.exhibition_expense_tracking, name='exhibition_expense_tracking'),
    path('exhibitions/analysis/', views.post_event_analysis, name='post_event_analysis'),
    
    # Annual Exhibition Budgets
    path('exhibitions/budgets/', views.annual_budget_list, name='annual_budget_list'),
    path('exhibitions/budgets/create/', views.annual_budget_create, name='annual_budget_create'),
    path('exhibitions/budgets/<int:budget_id>/', views.annual_budget_detail, name='annual_budget_detail'),
    path('exhibitions/budgets/<int:budget_id>/approve/', views.annual_budget_approve, name='annual_budget_approve'),
    path('exhibitions/budgets/dashboard/', views.budget_dashboard, name='budget_dashboard'),
    path('exhibitions/budgets/categories/', views.budget_category_manage, name='budget_category_manage'),
    
    # Phase 8: Advanced Features
    path('automation/email/', views.email_automation, name='email_automation'),
    path('automation/sms/', views.sms_notifications, name='sms_notifications'),
    path('files/management/', views.file_upload_management, name='file_upload_management'),
    path('calendar/integration/', views.calendar_integration, name='calendar_integration'),
    path('notifications/real-time/', views.real_time_notifications, name='real_time_notifications'),
    path('system/audit-trail/', views.audit_trail_system, name='audit_trail_system'),
    
    # User Management
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    
    # System Management
    path('system/users/', views.user_management, name='user_management'),
    path('system/users/create/', views.user_create, name='user_create'),
    path('system/users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('system/regions/', views.region_management, name='region_management'),
    path('system/notifications/', views.notification_settings, name='notification_settings'),
    path('reports/export/', views.export_reports, name='export_reports'),
]
