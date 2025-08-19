from django.contrib import admin
from .models import Campaign, Lead, EmailTemplate, CampaignMetric, LeadActivity

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'campaign_type', 'status', 'start_date', 'end_date', 'budget', 'created_by']
    list_filter = ['campaign_type', 'status', 'start_date', 'created_at']
    search_fields = ['name', 'description', 'target_audience']
    date_hierarchy = 'created_at'
    list_editable = ['status']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'campaign_type', 'status')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date')
        }),
        ('Budget & Goals', {
            'fields': ('budget', 'target_audience', 'goals')
        }),
        ('Metadata', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'company', 'source', 'status', 'score', 'assigned_to', 'created_at']
    list_filter = ['source', 'status', 'score', 'created_at', 'assigned_to']
    search_fields = ['first_name', 'last_name', 'email', 'company', 'phone']
    date_hierarchy = 'created_at'
    list_editable = ['status', 'score', 'assigned_to']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Company Information', {
            'fields': ('company', 'position')
        }),
        ('Lead Details', {
            'fields': ('source', 'status', 'score', 'notes')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'campaign')
        }),
    )

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'subject', 'content']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'subject', 'content', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )

@admin.register(CampaignMetric)
class CampaignMetricAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'date', 'impressions', 'clicks', 'conversions', 'spend', 'revenue', 'roi']
    list_filter = ['date', 'campaign']
    date_hierarchy = 'date'
    readonly_fields = ['roi']
    
    fieldsets = (
        ('Campaign & Date', {
            'fields': ('campaign', 'date')
        }),
        ('Performance Metrics', {
            'fields': ('impressions', 'clicks', 'conversions')
        }),
        ('Financial Metrics', {
            'fields': ('spend', 'revenue', 'roi')
        }),
    )

@admin.register(LeadActivity)
class LeadActivityAdmin(admin.ModelAdmin):
    list_display = ['lead', 'activity_type', 'performed_by', 'performed_at']
    list_filter = ['activity_type', 'performed_at', 'performed_by']
    search_fields = ['lead__first_name', 'lead__last_name', 'description']
    date_hierarchy = 'performed_at'
    
    fieldsets = (
        ('Activity Information', {
            'fields': ('lead', 'activity_type', 'description')
        }),
        ('Performer', {
            'fields': ('performed_by',)
        }),
    )

# Customize admin site
admin.site.site_header = "Marketing Management System"
admin.site.site_title = "Marketing Admin"
admin.site.index_title = "Welcome to Marketing Management"

