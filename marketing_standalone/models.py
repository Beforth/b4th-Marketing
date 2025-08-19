from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Campaign(models.Model):
    CAMPAIGN_TYPES = [
        ('email', 'Email Campaign'),
        ('social', 'Social Media'),
        ('ads', 'Digital Ads'),
        ('content', 'Content Marketing'),
        ('webinar', 'Webinar'),
        ('event', 'Event'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    target_audience = models.TextField(blank=True)
    goals = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days
    
    @property
    def is_active(self):
        today = timezone.now().date()
        return self.status == 'active' and self.start_date <= today <= self.end_date

class Lead(models.Model):
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('social_media', 'Social Media'),
        ('email', 'Email Campaign'),
        ('referral', 'Referral'),
        ('event', 'Event'),
        ('ads', 'Digital Ads'),
        ('cold_call', 'Cold Call'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    position = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    score = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class EmailTemplate(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class CampaignMetric(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    date = models.DateField()
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    spend = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ['campaign', 'date']
    
    @property
    def ctr(self):
        return (self.clicks / self.impressions * 100) if self.impressions > 0 else 0
    
    @property
    def conversion_rate(self):
        return (self.conversions / self.clicks * 100) if self.clicks > 0 else 0
    
    @property
    def roi(self):
        return ((self.revenue - self.spend) / self.spend * 100) if self.spend > 0 else 0

class Region(models.Model):
    """Marketing regions (North, South, East, West)"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_regions')
    monthly_target = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quarterly_target = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    """Customer with multi-location support"""
    CUSTOMER_TYPES = [
        ('prospect', 'Prospect'),
        ('existing', 'Existing Customer'),
        ('lapsed', 'Lapsed Customer'),
    ]
    
    name = models.CharField(max_length=200)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='prospect')
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def total_locations(self):
        return self.locations.count()
    
    @property
    def total_orders(self):
        return self.purchase_orders.count()

class CustomerLocation(models.Model):
    """Multiple locations per customer"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='locations')
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer.name} - {self.city}"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            # Ensure only one primary location per customer
            CustomerLocation.objects.filter(customer=self.customer, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

class Visit(models.Model):
    """Customer visits with GPS tracking"""
    VISIT_TYPES = [
        ('cold_call', 'Cold Call'),
        ('follow_up', 'Follow Up'),
        ('presentation', 'Presentation'),
        ('technical_discussion', 'Technical Discussion'),
        ('negotiation', 'Negotiation'),
        ('exhibition', 'Exhibition'),
        ('road_show', 'Road Show'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location = models.ForeignKey(CustomerLocation, on_delete=models.CASCADE, null=True, blank=True)
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    scheduled_date = models.DateTimeField()
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    gps_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    gps_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    purpose = models.TextField()
    outcome = models.TextField(blank=True)
    next_follow_up_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer.name} - {self.get_visit_type_display()} - {self.scheduled_date.strftime('%Y-%m-%d')}"
    
    @property
    def duration_minutes(self):
        if self.actual_start_time and self.actual_end_time:
            return int((self.actual_end_time - self.actual_start_time).total_seconds() / 60)
        return 0

class Expense(models.Model):
    """Daily expense tracking with approval workflow"""
    EXPENSE_TYPES = [
        ('travel', 'Travel'),
        ('meals', 'Meals'),
        ('accommodation', 'Accommodation'),
        ('transport', 'Transport'),
        ('entertainment', 'Entertainment'),
        ('office', 'Office Supplies'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('prepared', 'Prepared'),
        ('verified', 'Verified'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    receipt = models.FileField(upload_to='expenses/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='prepared')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_expenses')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_expenses')
    verified_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.expense_type} - {self.amount}"

class Exhibition(models.Model):
    """Exhibition management"""
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=200)
    organizer = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stall_size = models.CharField(max_length=100, blank=True)
    stall_design_vendor = models.CharField(max_length=200, blank=True)
    artwork_finalized = models.BooleanField(default=False)
    hotel_booked = models.BooleanField(default=False)
    tickets_booked = models.BooleanField(default=False)
    materials_prepared = models.BooleanField(default=False)
    gifts_finalized = models.BooleanField(default=False)
    invitations_sent = models.BooleanField(default=False)
    visitor_count = models.IntegerField(default=0)
    total_expense = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.start_date.strftime('%Y-%m-%d')}"

class Quotation(models.Model):
    """Quotation with version control"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent to Customer'),
        ('revised', 'Revised'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    quotation_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    version = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    valid_until = models.DateField()
    terms_conditions = models.TextField(blank=True)
    payment_terms = models.CharField(max_length=200, blank=True)
    delivery_terms = models.CharField(max_length=200, blank=True)
    ga_drawing = models.FileField(upload_to='quotations/drawings/', null=True, blank=True)
    customer_feedback = models.TextField(blank=True)
    sent_date = models.DateTimeField(null=True, blank=True)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.quotation_number} v{self.version} - {self.customer.name}"
    
    def save(self, *args, **kwargs):
        if not self.quotation_number:
            self.quotation_number = f"QT-{timezone.now().strftime('%Y%m')}-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class PurchaseOrder(models.Model):
    """Purchase Order management"""
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('verified', 'Verified'),
        ('approved', 'Approved'),
        ('in_production', 'In Production'),
        ('completed', 'Completed'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
    ]
    
    po_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    received_date = models.DateField()
    delivery_date = models.DateField()
    payment_terms = models.CharField(max_length=200)
    special_requirements = models.TextField(blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_pos')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_pos')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.po_number} - {self.customer.name}"

class WorkOrder(models.Model):
    """Internal work order"""
    STATUS_CHOICES = [
        ('allocated', 'Allocated'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    
    work_order_number = models.CharField(max_length=50, unique=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='allocated')
    allocated_to = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    completion_date = models.DateField()
    actual_start_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.work_order_number} - {self.purchase_order.po_number}"

class Manufacturing(models.Model):
    """Manufacturing tracking with QC"""
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('started', 'Started'),
        ('in_progress', 'In Progress'),
        ('qc_started', 'QC Started'),
        ('qc_completed', 'QC Completed'),
        ('packing', 'Packing'),
        ('ready_dispatch', 'Ready for Dispatch'),
    ]
    
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=50, unique=True)
    machine_number = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    planned_start_date = models.DateField()
    planned_completion_date = models.DateField()
    actual_start_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateField(null=True, blank=True)
    qc_start_date = models.DateField(null=True, blank=True)
    qc_end_date = models.DateField(null=True, blank=True)
    packing_start_date = models.DateField(null=True, blank=True)
    packing_end_date = models.DateField(null=True, blank=True)
    tentative_dispatch_date = models.DateField(null=True, blank=True)
    delays = models.TextField(blank=True)
    breakdowns = models.TextField(blank=True)
    qc_remarks = models.TextField(blank=True)
    packing_details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.batch_number} - {self.work_order.work_order_number}"

class Dispatch(models.Model):
    """Final dispatch to customer"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('dispatched', 'Dispatched'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
    ]
    
    TRANSPORT_MODES = [
        ('road', 'Road'),
        ('rail', 'Rail'),
        ('air', 'Air'),
        ('sea', 'Sea'),
    ]
    
    manufacturing = models.ForeignKey(Manufacturing, on_delete=models.CASCADE)
    challan_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transport_mode = models.CharField(max_length=20, choices=TRANSPORT_MODES)
    transporter_name = models.CharField(max_length=200)
    vehicle_number = models.CharField(max_length=20, blank=True)
    dispatch_date = models.DateTimeField(null=True, blank=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)
    delivery_receipt_received = models.BooleanField(default=False)
    delivery_receipt_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.challan_number} - {self.manufacturing.batch_number}"

class ProductionPlan(models.Model):
    """Production planning and scheduling"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    plan_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    planned_start_date = models.DateField()
    planned_end_date = models.DateField()
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], default='medium')
    department = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    resource_requirements = models.TextField(blank=True)
    special_instructions = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_production_plans')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.plan_number} - {self.work_order.work_order_number}"

class QCTracking(models.Model):
    """Quality Control tracking"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('rework', 'Rework Required'),
    ]
    
    manufacturing = models.ForeignKey(Manufacturing, on_delete=models.CASCADE)
    qc_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    qc_date = models.DateField()
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    inspection_type = models.CharField(max_length=50, choices=[
        ('visual', 'Visual Inspection'),
        ('dimensional', 'Dimensional Check'),
        ('functional', 'Functional Test'),
        ('material', 'Material Test'),
        ('final', 'Final Inspection'),
    ])
    parameters_checked = models.TextField()
    test_results = models.TextField()
    defects_found = models.TextField(blank=True)
    corrective_actions = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.qc_number} - {self.manufacturing.batch_number}"

class PackingDetails(models.Model):
    """Packing and packaging details"""
    manufacturing = models.ForeignKey(Manufacturing, on_delete=models.CASCADE)
    packing_date = models.DateField()
    packed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    packaging_type = models.CharField(max_length=100, choices=[
        ('wooden_crate', 'Wooden Crate'),
        ('cardboard_box', 'Cardboard Box'),
        ('plastic_wrap', 'Plastic Wrap'),
        ('bubble_wrap', 'Bubble Wrap'),
        ('custom', 'Custom Packaging'),
    ])
    dimensions = models.CharField(max_length=100, blank=True)  # L x W x H
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity_packed = models.IntegerField()
    special_handling = models.TextField(blank=True)
    fragile_items = models.BooleanField(default=False)
    packing_list = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Packing - {self.manufacturing.batch_number}"

class DispatchChecklist(models.Model):
    """Department-wise dispatch checklist"""
    dispatch = models.ForeignKey(Dispatch, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    checklist_item = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.department} - {self.checklist_item}"

class URS(models.Model):
    """User Requirement Specification"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200)
    requirement_details = models.TextField()
    technical_specs = models.TextField()
    site_requirements = models.TextField()
    timeline = models.CharField(max_length=100)
    budget_range = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.project_name} - {self.customer.name}"

class GADrawing(models.Model):
    """General Arrangement Drawing"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('shared', 'Shared with Customer'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    urs = models.ForeignKey(URS, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    version = models.CharField(max_length=20, default='1.0')
    drawing_file = models.FileField(upload_to='ga_drawings/', blank=True, null=True)
    details = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    feedback = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} v{self.version} - {self.urs.project_name}"

class TechnicalDiscussion(models.Model):
    """Technical Discussion Records"""
    DISCUSSION_TYPES = [
        ('telephonic', 'Telephonic'),
        ('in_person', 'In Person'),
        ('video', 'Video Call'),
    ]
    
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    discussion_date = models.DateTimeField()
    discussion_type = models.CharField(max_length=20, choices=DISCUSSION_TYPES)
    participants = models.TextField()
    discussion_points = models.TextField()
    decisions_made = models.TextField()
    action_items = models.TextField()
    next_follow_up = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Tech Discussion - {self.quotation.quotation_number}"

class Negotiation(models.Model):
    """Negotiation Records"""
    NEGOTIATION_TYPES = [
        ('initial', 'Initial Discussion'),
        ('counter', 'Counter Offer'),
        ('final', 'Final Negotiation'),
    ]
    
    OUTCOME_CHOICES = [
        ('successful', 'Successful'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]
    
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    negotiation_date = models.DateTimeField()
    negotiation_type = models.CharField(max_length=20, choices=NEGOTIATION_TYPES)
    participants = models.TextField()
    initial_offer = models.DecimalField(max_digits=10, decimal_places=2)
    customer_counter_offer = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_offer = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    payment_terms = models.TextField()
    delivery_terms = models.TextField()
    outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Negotiation - {self.quotation.quotation_number}"

class LeadActivity(models.Model):
    ACTIVITY_TYPES = [
        ('email_sent', 'Email Sent'),
        ('email_opened', 'Email Opened'),
        ('email_clicked', 'Email Clicked'),
        ('call_made', 'Call Made'),
        ('meeting_scheduled', 'Meeting Scheduled'),
        ('proposal_sent', 'Proposal Sent'),
        ('note_added', 'Note Added'),
        ('visit_completed', 'Visit Completed'),
        ('quotation_sent', 'Quotation Sent'),
        ('negotiation_started', 'Negotiation Started'),
        ('po_received', 'PO Received'),
    ]
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    performed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-performed_at']
    
    def __str__(self):
        return f"{self.lead.full_name} - {self.get_activity_type_display()}"
