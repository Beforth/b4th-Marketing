from django.contrib import admin
from .models import Campaign, Lead, EmailTemplate, CampaignMetric, LeadActivity, Visit, VisitParticipant, PurchaseOrder, PaymentFollowUp, BudgetCategory, AnnualExhibitionBudget, BudgetAllocation, BudgetApproval, Exhibition

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

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['customer', 'visit_type', 'status', 'scheduled_date', 'assigned_to', 'participant_count']
    list_filter = ['visit_type', 'status', 'scheduled_date', 'assigned_to']
    search_fields = ['customer__name', 'purpose', 'outcome']
    date_hierarchy = 'scheduled_date'
    list_editable = ['status']
    
    fieldsets = (
        ('Visit Information', {
            'fields': ('customer', 'location', 'visit_type', 'status', 'purpose')
        }),
        ('Schedule', {
            'fields': ('scheduled_date', 'actual_start_time', 'actual_end_time')
        }),
        ('Location & Tracking', {
            'fields': ('gps_latitude', 'gps_longitude')
        }),
        ('Outcome & Follow-up', {
            'fields': ('outcome', 'next_follow_up_date')
        }),
        ('Assignment', {
            'fields': ('assigned_to',)
        }),
    )

@admin.register(VisitParticipant)
class VisitParticipantAdmin(admin.ModelAdmin):
    list_display = ['visit', 'user', 'role', 'is_primary', 'created_at']
    list_filter = ['role', 'is_primary', 'created_at']
    search_fields = ['visit__customer__name', 'user__first_name', 'user__last_name', 'notes']
    list_editable = ['role', 'is_primary']
    
    fieldsets = (
        ('Participant Information', {
            'fields': ('visit', 'user', 'role', 'is_primary')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'customer', 'status', 'total_amount', 'payment_method', 'received_date', 'delivery_date']
    list_filter = ['status', 'payment_method', 'received_date', 'delivery_date']
    search_fields = ['po_number', 'customer__name', 'payment_terms']
    list_editable = ['status', 'payment_method']
    date_hierarchy = 'received_date'
    
    fieldsets = (
        ('Order Information', {
            'fields': ('po_number', 'customer', 'quotation', 'status', 'total_amount')
        }),
        ('Dates', {
            'fields': ('received_date', 'delivery_date')
        }),
        ('Payment Details', {
            'fields': ('payment_terms', 'payment_method', 'payment_terms_declared')
        }),
        ('Requirements', {
            'fields': ('special_requirements',)
        }),
        ('Approval', {
            'fields': ('verified_by', 'approved_by'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PaymentFollowUp)
class PaymentFollowUpAdmin(admin.ModelAdmin):
    list_display = ['purchase_order', 'payment_method', 'status', 'follow_up_date', 'created_by', 'is_overdue']
    list_filter = ['status', 'payment_method', 'follow_up_date', 'created_at']
    search_fields = ['purchase_order__po_number', 'purchase_order__customer__name', 'notes']
    list_editable = ['status']
    date_hierarchy = 'follow_up_date'
    
    fieldsets = (
        ('Follow-up Information', {
            'fields': ('purchase_order', 'payment_method', 'payment_terms_declared')
        }),
        ('Schedule', {
            'fields': ('follow_up_date', 'status')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )
    
    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'

@admin.register(BudgetCategory)
class BudgetCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'is_active', 'created_at']
    list_filter = ['category_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'category_type', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(AnnualExhibitionBudget)
class AnnualExhibitionBudgetAdmin(admin.ModelAdmin):
    list_display = ['year', 'total_budget', 'allocated_budget', 'spent_budget', 'remaining_budget', 'status', 'utilization_percentage']
    list_filter = ['status', 'year', 'created_at']
    search_fields = ['year', 'notes']
    list_editable = ['status']
    readonly_fields = ['remaining_budget', 'utilization_percentage', 'allocation_percentage']
    
    fieldsets = (
        ('Budget Information', {
            'fields': ('year', 'total_budget', 'status', 'notes')
        }),
        ('Financial Summary', {
            'fields': ('allocated_budget', 'spent_budget', 'remaining_budget', 'utilization_percentage', 'allocation_percentage'),
            'classes': ('collapse',)
        }),
        ('Approval', {
            'fields': ('created_by', 'approved_by', 'approved_at'),
            'classes': ('collapse',)
        }),
    )
    
    def utilization_percentage(self, obj):
        return f"{obj.utilization_percentage:.1f}%"
    utilization_percentage.short_description = 'Utilization %'

@admin.register(BudgetAllocation)
class BudgetAllocationAdmin(admin.ModelAdmin):
    list_display = ['annual_budget', 'category', 'allocated_amount', 'spent_amount', 'remaining_amount', 'utilization_percentage']
    list_filter = ['annual_budget__year', 'category__category_type', 'created_at']
    search_fields = ['annual_budget__year', 'category__name', 'notes']
    readonly_fields = ['remaining_amount', 'utilization_percentage']
    
    fieldsets = (
        ('Allocation Information', {
            'fields': ('annual_budget', 'category', 'allocated_amount', 'notes')
        }),
        ('Financial Summary', {
            'fields': ('spent_amount', 'remaining_amount', 'utilization_percentage'),
            'classes': ('collapse',)
        }),
    )
    
    def utilization_percentage(self, obj):
        return f"{obj.utilization_percentage:.1f}%"
    utilization_percentage.short_description = 'Utilization %'

@admin.register(BudgetApproval)
class BudgetApprovalAdmin(admin.ModelAdmin):
    list_display = ['annual_budget', 'approval_level', 'status', 'approved_by', 'approved_at']
    list_filter = ['approval_level', 'status', 'created_at']
    search_fields = ['annual_budget__year', 'comments']
    list_editable = ['status']
    
    fieldsets = (
        ('Approval Information', {
            'fields': ('annual_budget', 'approval_level', 'status', 'comments')
        }),
        ('Approval Details', {
            'fields': ('approved_by', 'approved_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'organizer', 'venue', 'start_date', 'status', 'budget', 'budget_category', 'total_expense']
    list_filter = ['status', 'budget_category__category_type', 'start_date', 'created_at']
    search_fields = ['name', 'organizer', 'venue', 'notes']
    list_editable = ['status']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Exhibition Information', {
            'fields': ('name', 'organizer', 'venue', 'start_date', 'end_date', 'status')
        }),
        ('Budget Information', {
            'fields': ('budget', 'budget_category', 'annual_budget', 'total_expense')
        }),
        ('Stall Details', {
            'fields': ('stall_size', 'stall_design_vendor'),
            'classes': ('collapse',)
        }),
        ('Preparation Status', {
            'fields': ('artwork_finalized', 'hotel_booked', 'tickets_booked', 'materials_prepared', 'gifts_finalized', 'invitations_sent'),
            'classes': ('collapse',)
        }),
        ('Results', {
            'fields': ('visitor_count', 'notes'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )

# Customize admin site
admin.site.site_header = "Marketing Management System"
admin.site.site_title = "Marketing Admin"
admin.site.index_title = "Welcome to Marketing Management"
