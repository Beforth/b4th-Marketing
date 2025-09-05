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
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_visits')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer.name} - {self.get_visit_type_display()} - {self.scheduled_date.strftime('%Y-%m-%d')}"
    
    @property
    def duration_minutes(self):
        if self.actual_start_time and self.actual_end_time:
            return int((self.actual_end_time - self.actual_start_time).total_seconds() / 60)
        return 0
    
    @property
    def participant_count(self):
        """Get total number of participants in this visit"""
        return self.participants.count()
    
    @property
    def participant_names(self):
        """Get comma-separated list of participant names"""
        return ', '.join([p.user.get_full_name() or p.user.username for p in self.participants.all()])


class VisitParticipant(models.Model):
    """Track multiple participants in a single visit"""
    ROLE_CHOICES = [
        ('primary', 'Primary Executive'),
        ('secondary', 'Secondary Executive'),
        ('technical', 'Technical Expert'),
        ('manager', 'Manager'),
        ('observer', 'Observer'),
    ]
    
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='secondary')
    is_primary = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text="Specific notes about this participant's role in the visit")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['visit', 'user']
        ordering = ['-is_primary', 'role', 'user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()} ({self.visit})"

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

class BudgetCategory(models.Model):
    """Budget categories for exhibitions"""
    CATEGORY_TYPES = [
        ('trade_show', 'Trade Show'),
        ('industry_exhibition', 'Industry Exhibition'),
        ('regional_exhibition', 'Regional Exhibition'),
        ('international_exhibition', 'International Exhibition'),
        ('local_event', 'Local Event'),
        ('conference', 'Conference'),
        ('seminar', 'Seminar'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=30, choices=CATEGORY_TYPES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Budget Categories"
    
    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"


class AnnualExhibitionBudget(models.Model):
    """Annual budget allocation for exhibitions"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    year = models.IntegerField(unique=True)
    total_budget = models.DecimalField(max_digits=12, decimal_places=2)
    allocated_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    spent_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_budgets')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_budgets')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year']
    
    def __str__(self):
        return f"Annual Budget {self.year} - ₹{self.total_budget:,.2f}"
    
    def save(self, *args, **kwargs):
        # Calculate remaining budget
        self.remaining_budget = self.total_budget - self.spent_budget
        super().save(*args, **kwargs)
    
    @property
    def utilization_percentage(self):
        """Calculate budget utilization percentage"""
        if self.total_budget > 0:
            return (self.spent_budget / self.total_budget) * 100
        return 0
    
    @property
    def allocation_percentage(self):
        """Calculate budget allocation percentage"""
        if self.total_budget > 0:
            return (self.allocated_budget / self.total_budget) * 100
        return 0


class BudgetAllocation(models.Model):
    """Budget allocation to specific categories"""
    annual_budget = models.ForeignKey(AnnualExhibitionBudget, on_delete=models.CASCADE, related_name='allocations')
    category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['annual_budget', 'category']
    
    def __str__(self):
        return f"{self.annual_budget.year} - {self.category.name} - ₹{self.allocated_amount:,.2f}"
    
    @property
    def remaining_amount(self):
        """Calculate remaining amount for this category"""
        return self.allocated_amount - self.spent_amount
    
    @property
    def utilization_percentage(self):
        """Calculate utilization percentage for this category"""
        if self.allocated_amount > 0:
            return (self.spent_amount / self.allocated_amount) * 100
        return 0


class BudgetApproval(models.Model):
    """Budget approval workflow"""
    APPROVAL_LEVELS = [
        ('manager', 'Manager'),
        ('director', 'Director'),
        ('ceo', 'CEO'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    annual_budget = models.ForeignKey(AnnualExhibitionBudget, on_delete=models.CASCADE, related_name='approvals')
    approval_level = models.CharField(max_length=20, choices=APPROVAL_LEVELS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    comments = models.TextField(blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.annual_budget.year} - {self.get_approval_level_display()} - {self.get_status_display()}"


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
    budget_category = models.ForeignKey(BudgetCategory, on_delete=models.SET_NULL, null=True, blank=True)
    annual_budget = models.ForeignKey(AnnualExhibitionBudget, on_delete=models.SET_NULL, null=True, blank=True)
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
    
    def save(self, *args, **kwargs):
        # Update annual budget spent amount when exhibition expenses change
        if self.annual_budget and self.budget_category:
            try:
                allocation = BudgetAllocation.objects.get(
                    annual_budget=self.annual_budget,
                    category=self.budget_category
                )
                # Update spent amount for this category
                category_exhibitions = Exhibition.objects.filter(
                    annual_budget=self.annual_budget,
                    budget_category=self.budget_category
                ).exclude(id=self.id)
                total_spent = sum(ex.total_expense for ex in category_exhibitions) + self.total_expense
                allocation.spent_amount = total_spent
                allocation.save()
                
                # Update annual budget spent amount
                annual_spent = sum(allocation.spent_amount for allocation in self.annual_budget.allocations.all())
                self.annual_budget.spent_budget = annual_spent
                self.annual_budget.save()
            except BudgetAllocation.DoesNotExist:
                pass
        super().save(*args, **kwargs)

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
    
    @property
    def total_revisions(self):
        """Get total number of revisions for this quotation"""
        return self.revisions.count()
    
    @property
    def latest_revision(self):
        """Get the latest revision for this quotation"""
        return self.revisions.first()
    
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
    
    PAYMENT_METHOD_CHOICES = [
        ('advance', 'Advance Payment'),
        ('credit', 'Credit Payment'),
        ('l_c', 'Letter of Credit'),
        ('bank_guarantee', 'Bank Guarantee'),
        ('cheque', 'Cheque'),
        ('neft_rtgs', 'NEFT/RTGS'),
        ('cash', 'Cash'),
        ('other', 'Other'),
    ]
    
    po_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    received_date = models.DateField()
    delivery_date = models.DateField()
    payment_terms = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    payment_terms_declared = models.TextField(blank=True, help_text="Detailed payment terms as declared by customer")
    special_requirements = models.TextField(blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_pos')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_pos')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.po_number} - {self.customer.name}"
    
    @property
    def payment_followup_required(self):
        """Check if payment follow-up is required"""
        return self.status in ['received', 'verified', 'approved'] and not self.payment_followups.exists()
    
    @property
    def latest_payment_followup(self):
        """Get the latest payment follow-up"""
        return self.payment_followups.order_by('-created_at').first()


class PaymentFollowUp(models.Model):
    """Payment Follow-up tracking after PO received"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('advance', 'Advance Payment'),
        ('credit', 'Credit Payment'),
        ('l_c', 'Letter of Credit'),
        ('bank_guarantee', 'Bank Guarantee'),
        ('cheque', 'Cheque'),
        ('neft_rtgs', 'NEFT/RTGS'),
        ('cash', 'Cash'),
        ('other', 'Other'),
    ]
    
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='payment_followups')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_terms_declared = models.TextField(help_text="Payment terms as declared by customer")
    follow_up_date = models.DateField()
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-follow_up_date', '-created_at']
    
    def __str__(self):
        return f"Payment Follow-up - {self.purchase_order.po_number} - {self.get_payment_method_display()}"
    
    @property
    def is_overdue(self):
        """Check if follow-up is overdue"""
        return self.follow_up_date < timezone.now().date() and self.status == 'pending'

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

class QuotationRevision(models.Model):
    """Track quotation revisions and link to negotiations"""
    REVISION_REASONS = [
        ('price_adjustment', 'Price Adjustment'),
        ('specification_change', 'Specification Change'),
        ('terms_modification', 'Terms Modification'),
        ('customer_request', 'Customer Request'),
        ('market_conditions', 'Market Conditions'),
        ('competitor_response', 'Competitor Response'),
        ('other', 'Other'),
    ]
    
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='revisions')
    revision_number = models.IntegerField()
    revision_date = models.DateTimeField(auto_now_add=True)
    revision_reason = models.CharField(max_length=30, choices=REVISION_REASONS)
    previous_amount = models.DecimalField(max_digits=12, decimal_places=2)
    new_amount = models.DecimalField(max_digits=12, decimal_places=2)
    changes_summary = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    negotiation = models.ForeignKey('Negotiation', on_delete=models.SET_NULL, null=True, blank=True, related_name='quotation_revisions')
    
    class Meta:
        ordering = ['-revision_date']
    
    def __str__(self):
        return f"{self.quotation.quotation_number} - Revision {self.revision_number}"

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
    
    @property
    def revision_count(self):
        """Count of quotation revisions for this negotiation"""
        return self.quotation_revisions.count()
    
    @property
    def revision_timeline(self):
        """Get timeline of all revisions for this negotiation"""
        return self.quotation_revisions.all().order_by('revision_date')
    
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

class InquiryLog(models.Model):
    """Main Enquiry Log Structure"""
    OFFER_CATEGORIES = [
        ('standard', 'Standard'),
        ('customized', 'Customized'),
        ('discounted', 'Discounted'),
        ('final', 'Final'),
    ]
    
    ENQUIRY_THROUGH_CHOICES = [
        ('regional_head', 'Regional Head'),
        ('area_sales_manager', 'Area Sales Manager'),
        ('enquiry_mail', 'Enquiry Mail'),
        ('website', 'Website'),
        ('individual_vp', 'Individual (VP)'),
        ('individual_india_head', 'Individual (India Head)'),
        ('individual_other', 'Individual (Other)'),
        ('exhibition', 'Exhibition'),
        ('mail', 'Mail'),
        ('call', 'Call'),
    ]
    
    FOLLOW_UP_STATUS_CHOICES = [
        ('yes_updated', 'Yes (Updated in Follow-Up Status)'),
        ('yet_not', 'Yet Not (Not updated in Follow-Up Status)'),
    ]
    
    QUOTE_SEND_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    # SR. No. - Auto-generated
    sr_no = models.AutoField(primary_key=True)
    
    # Enquiry Details
    month = models.CharField(max_length=20, help_text="Month of enquiry")
    enquiry_number = models.CharField(max_length=50, unique=True, help_text="ENQ-No")
    enquiry_date = models.DateField(help_text="Enquiry Date")
    location = models.CharField(max_length=200, help_text="Location")
    enquiry_mail = models.EmailField(help_text="Enquiry Mail")
    enquiry_through = models.CharField(max_length=30, choices=ENQUIRY_THROUGH_CHOICES, help_text="How the enquiry was received")
    
    # Quote Details
    quote_number = models.CharField(max_length=50, blank=True, help_text="Quote No.")
    quote_date = models.DateField(null=True, blank=True, help_text="Quote Date")
    
    # Company Details
    offer_category = models.CharField(max_length=20, choices=OFFER_CATEGORIES, default='standard')
    company_name = models.CharField(max_length=200)
    company_address = models.TextField()
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email_id = models.EmailField()
    
    # Requirement Details
    requirement_details = models.TextField()
    
    # Quote Status
    quote_send = models.CharField(max_length=3, choices=QUOTE_SEND_CHOICES, default='no')
    quote_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Follow Up
    follow_up_status = models.CharField(max_length=20, choices=FOLLOW_UP_STATUS_CHOICES, blank=True, help_text="Follow-up status")
    follow_up = models.TextField(blank=True, help_text="Follow up notes and status")
    
    # System fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-enquiry_date', '-created_at']
        verbose_name = "Inquiry Log"
        verbose_name_plural = "Inquiry Logs"
    
    def __str__(self):
        return f"{self.enquiry_number} - {self.company_name}"
    
    def save(self, *args, **kwargs):
        if not self.enquiry_number:
            # Generate enquiry number if not provided
            from django.utils import timezone
            month_year = timezone.now().strftime('%Y%m')
            last_enquiry = InquiryLog.objects.filter(
                enquiry_number__startswith=f'ENQ-{month_year}'
            ).order_by('-enquiry_number').first()
            
            if last_enquiry:
                last_num = int(last_enquiry.enquiry_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.enquiry_number = f'ENQ-{month_year}-{new_num:04d}'
        
        super().save(*args, **kwargs)
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage if both prices are available"""
        if self.quote_price and self.discounted_price and self.quote_price > 0:
            return ((self.quote_price - self.discounted_price) / self.quote_price) * 100
        return 0
    
    @property
    def is_quote_sent(self):
        """Check if quote has been sent"""
        return self.quote_send == 'yes'


# MIS System Models
class FollowUpStatus(models.Model):
    """Sheet 2: Follow-Up Status"""
    FOLLOW_UP_STATUS_CHOICES = [
        ('qtn_submitted', 'QTN Submitted'),
        ('qtn_followup', 'QTN Followup'),
        ('technical_discussions', 'Technical Discussions'),
        ('at_customer_desk', 'At Customer Desk'),
        ('order_finalization', 'Order Finalization (AP)'),
        ('po_release', 'PO Release (AP)'),
        ('po_acknowledge', 'PO Acknowledge (AP)'),
        ('wo_prepared', 'WO Prepared'),
        ('on_hold', 'On-Hold (Customer end)'),
        ('requirement_cancelled', 'Requirement Cancelled (Customer end)'),
        ('order_loss_1', '1 - Order Loss'),
        ('order_loss_2', '2 - Order Loss'),
        ('order_loss_3', '3 - Order Loss'),
    ]
    
    sr_no = models.AutoField(primary_key=True)
    month = models.CharField(max_length=20)
    date = models.DateField()
    quote_no = models.CharField(max_length=50, blank=True)
    responsible_person = models.CharField(max_length=100)
    company_group = models.CharField(max_length=200)
    address = models.TextField()
    contact_person = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    mail_id = models.EmailField()
    requirements = models.TextField()
    follow_up_date = models.DateField()
    follow_up_status = models.CharField(max_length=30, choices=FOLLOW_UP_STATUS_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-follow_up_date', '-created_at']
        verbose_name = "Follow-Up Status"
        verbose_name_plural = "Follow-Up Status"
    
    def __str__(self):
        return f"{self.company_group} - {self.follow_up_date}"


class ProjectToday(models.Model):
    """Sheet 3: Project Today"""
    PHARMA_CATEGORIES = [
        ('api', 'API'),
        ('injectable', 'Injectable'),
        ('formulation', 'Formulation'),
        ('oncology', 'Oncology'),
        ('intermediate', 'Intermediate'),
        ('packaging', 'Packaging'),
    ]
    
    NON_PHARMA_CATEGORIES = [
        ('fmcg', 'FMCG'),
        ('chemical', 'Chemical Industry'),
        ('blood_bank', 'Blood bank'),
        ('oil_gas', 'Oil & Gas Industry'),
        ('cosmetics', 'Cosmetics'),
        ('textile', 'Textile'),
        ('hospital', 'Hospital'),
        ('government', 'Government'),
        ('agri', 'Agri'),
        ('dairy', 'Dairy'),
        ('veterinary', 'Veterinary'),
        ('other', 'Other'),
    ]
    
    sr_no = models.AutoField(primary_key=True)
    location = models.CharField(max_length=200)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    product1 = models.CharField(max_length=200)
    promoter_name = models.CharField(max_length=200)
    promoter_office_add = models.TextField()
    promoter_contact_person_name = models.CharField(max_length=100)
    promoter_contact_person_designation = models.CharField(max_length=100)
    promoter_contact_person_direct_contact = models.CharField(max_length=20)
    promoter_contact_person_email = models.EmailField()
    architect_name = models.CharField(max_length=100, blank=True)
    consultant_name = models.CharField(max_length=100, blank=True)
    contractor_name = models.CharField(max_length=100, blank=True)
    followup_date = models.DateField()
    followup_status = models.CharField(max_length=30, choices=FollowUpStatus.FOLLOW_UP_STATUS_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-followup_date', '-created_at']
        verbose_name = "Project Today"
        verbose_name_plural = "Projects Today"
    
    def __str__(self):
        return f"{self.promoter_name} - {self.location}"


class OrderExpectedNextMonth(models.Model):
    """Sheet 4: Order expected in Next Month"""
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delayed', 'Delayed'),
        ('cancelled', 'Cancelled'),
    ]
    
    region = models.CharField(max_length=100)
    from_month = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200)
    requirement = models.TextField()
    location = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    ap_quote_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    last_status_date = models.DateField()
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
    expected_in_month = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_status_date', '-created_at']
        verbose_name = "Order Expected Next Month"
        verbose_name_plural = "Orders Expected Next Month"
    
    def __str__(self):
        return f"{self.company_name} - {self.expected_in_month}"


class MISPurchaseOrder(models.Model):
    """Sheet 5: Purchase Order - MIS System"""
    sr_no = models.AutoField(primary_key=True)
    person_name = models.CharField(max_length=100)
    purchase_order_no = models.CharField(max_length=100)
    po_date = models.DateField()
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    contact_person_details = models.TextField()
    contact_number = models.CharField(max_length=20)
    enquiry_log_number = models.CharField(max_length=50, blank=True)
    quote_no = models.CharField(max_length=50, blank=True)
    work_order_number = models.CharField(max_length=50, blank=True)
    product_name = models.CharField(max_length=200)
    capacity = models.CharField(max_length=100, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    machine_details = models.TextField(blank=True)
    equipment_sr_number = models.CharField(max_length=100, blank=True)
    po_amount = models.DecimalField(max_digits=12, decimal_places=2)
    ap_quote_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    percentage_order = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-po_date', '-created_at']
        verbose_name = "MIS Purchase Order"
        verbose_name_plural = "MIS Purchase Orders"
    
    def __str__(self):
        return f"{self.purchase_order_no} - {self.company_name}"


class NewData(models.Model):
    """Sheet 6: New Data - Monthly Tracking"""
    CATEGORY_CHOICES = [
        ('new_customer_visits_pharma', 'New customer visits or Enquiry (Pharma)'),
        ('new_customer_visits_non_pharma', 'New customer visits or Enquiry (Non Pharma)'),
        ('identify_pharma_groups', 'Identify new potential business in Pharma Field (Groups)'),
        ('identify_pharma_individual', 'Identify new potential business in Pharma Field (Individual Company)'),
        ('identify_non_pharma_groups', 'Identify new potential business in Non Pharma Field (Groups)'),
        ('identify_non_pharma_individual', 'Identify new potential business in Non Pharma Field (Individual Company)'),
    ]
    
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    april = models.IntegerField(default=0)
    may = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category']
        verbose_name = "New Data"
        verbose_name_plural = "New Data"
    
    def __str__(self):
        return f"{self.get_category_display()} - Total: {self.total}"


class NewDataDetails(models.Model):
    """Sheet 7: New Data Details"""
    PHARMA_CHOICES = [
        ('pharma', 'Pharma'),
        ('non_pharma', 'Non Pharma'),
    ]
    
    GROUP_CHOICES = [
        ('group', 'Group'),
        ('individual', 'Individual'),
    ]
    
    sr_no = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    pharma_non_pharma = models.CharField(max_length=20, choices=PHARMA_CHOICES)
    group_individual = models.CharField(max_length=20, choices=GROUP_CHOICES)
    contact_person = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=20)
    mail_id = models.EmailField()
    description = models.TextField()
    status = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "New Data Detail"
        verbose_name_plural = "New Data Details"
    
    def __str__(self):
        return f"{self.company_name} - {self.pharma_non_pharma}"


class ODPlan(models.Model):
    """Sheet 8: OD Plan - Outdoor Planning"""
    id = models.AutoField(primary_key=True)
    region = models.CharField(max_length=100)
    month = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    location = models.CharField(max_length=200)
    total_days = models.IntegerField()
    company_visits = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-from_date', '-created_at']
        verbose_name = "OD Plan"
        verbose_name_plural = "OD Plans"
    
    def __str__(self):
        return f"{self.name} - {self.region} ({self.month})"


# OD Plan and Visit Report System Models
class ODPlanVisitReport(models.Model):
    """OD Plan and Visit Report - Main outdoor planning and visit execution tracking"""
    
    REASON_FOR_VISIT_CHOICES = [
        ('first_visit', 'First Visit'),
        ('inquiry_collection', 'Inquiry Collection'),
        ('follow_up', 'Follow up'),
        ('casual_visit', 'Casual Visit'),
        ('order_finalization', 'Order Finalization'),
        ('technical_discussions', 'Technical Discussions'),
        ('payment_follow_up', 'Payment Follow up'),
        ('payment_collection', 'Payment Collection'),
        ('issue_escalation', 'Any Issue/Escalation'),
        ('upgradation_requirement', 'Upgradation Requirement'),
        ('amc_requirement', 'AMC Requirement'),
    ]
    
    APPOINTMENT_STATUS_CHOICES = [
        ('appointment_confirmed', 'Appointment confirmed'),
        ('direct_visit', 'Direct Visit'),
    ]
    
    VISIT_STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
        ('no_show', 'No Show'),
    ]
    
    MAIL_STATUS_CHOICES = [
        ('not_sent', 'Not Sent'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('opened', 'Opened'),
        ('replied', 'Replied'),
    ]
    
    # Outdoor Plan Section
    month = models.CharField(max_length=20, help_text="Month of planning")
    region = models.CharField(max_length=100, help_text="Region for visit")
    date = models.DateField(help_text="Planned date for visit")
    name = models.CharField(max_length=100, help_text="Person name")
    visit_plan = models.CharField(max_length=200, help_text="Visit plan details")
    location = models.CharField(max_length=200, help_text="Visit location")
    company_name = models.CharField(max_length=200, help_text="Company to visit")
    contact_person = models.CharField(max_length=100, help_text="Contact person name")
    contact_no = models.CharField(max_length=20, help_text="Contact number")
    mail_id = models.EmailField(help_text="Email address")
    reason_for_visit = models.CharField(max_length=50, choices=REASON_FOR_VISIT_CHOICES, help_text="Reason for visit")
    appointment_status = models.CharField(max_length=30, choices=APPOINTMENT_STATUS_CHOICES, help_text="Appointment status")
    
    # Visit Report Details Section
    visit_status = models.CharField(max_length=20, choices=VISIT_STATUS_CHOICES, default='planned', help_text="Visit status")
    visited_on_date = models.DateField(null=True, blank=True, help_text="Actual visit date")
    meeting_output = models.TextField(blank=True, help_text="Meeting output and results")
    next_action_needed = models.TextField(blank=True, help_text="Next action needed if any")
    next_follow_up_visit = models.DateField(null=True, blank=True, help_text="Next follow up visit date")
    mail_status_about_visit = models.CharField(max_length=20, choices=MAIL_STATUS_CHOICES, default='not_sent', help_text="Mail status about visit")
    comments = models.TextField(blank=True, help_text="Additional comments if any")
    
    # System fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = "OD Plan Visit Report"
        verbose_name_plural = "OD Plan Visit Reports"
    
    def __str__(self):
        return f"{self.company_name} - {self.region} ({self.date})"


class ODPlanRemarks(models.Model):
    """OD Plan Remarks - General remarks section"""
    remarks = models.TextField(help_text="General remarks if any")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "OD Plan Remark"
        verbose_name_plural = "OD Plan Remarks"
    
    def __str__(self):
        return f"Remarks - {self.created_at.strftime('%Y-%m-%d')}"


# Purchase Order Details System Model
class PODetails(models.Model):
    """Purchase Order Details - Complete PO template system"""
    
    PACKING_FORWARDING_CHOICES = [
        ('inclusive', 'Inclusive'),
        ('extra_as_actual', 'Extra As Actual'),
    ]
    
    TRANSPORTATION_CHOICES = [
        ('inclusive', 'Inclusive'),
        ('extra_as_actual', 'Extra As Actual'),
    ]
    
    # Basic PO Information (Sr. No. 1-4)
    customer_name = models.CharField(max_length=200, help_text="Customer Name")
    po_no = models.CharField(max_length=100, help_text="Purchase Order Number")
    po_date = models.DateField(help_text="Purchase Order Date")
    wo_no = models.CharField(max_length=100, help_text="Work Order Number")
    
    # Client Contact Details (Sr. No. 5)
    contact_name = models.CharField(max_length=100, help_text="Contact Person Name")
    contact_details = models.TextField(help_text="Contact Details")
    tel_mob_no = models.CharField(max_length=20, help_text="Telephone/Mobile Number")
    email_id = models.EmailField(help_text="Email Address")
    
    # Pricing (Sr. No. 6)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Discount Percentage")
    
    # Payment Terms Structure (Sr. No. 7)
    advance_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Advance Percentage")
    against_pi_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Against PI Percentage")
    against_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Against FAT Percentage")
    after_delivery_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="After Delivery Percentage")
    after_installation_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="After Installation Percentage")
    
    # Logistics (Sr. No. 8-9)
    packing_forwarding = models.CharField(max_length=20, choices=PACKING_FORWARDING_CHOICES, help_text="Packing & Forwarding")
    transportation = models.CharField(max_length=20, choices=TRANSPORTATION_CHOICES, help_text="Transportation")
    
    # Authorization Section
    marketing_dept = models.CharField(max_length=100, default="Miss. Pooja Kolse", help_text="Marketing Department Contact")
    accounts_dept = models.CharField(max_length=100, default="Mr. Jitendra Tajanpure", help_text="Accounts Department Contact")
    additional_contact = models.CharField(max_length=100, default="Mr. Harshal Ghoge", help_text="Additional Contact")
    
    # System fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-po_date', '-created_at']
        verbose_name = "PO Details"
        verbose_name_plural = "PO Details"
    
    def __str__(self):
        return f"{self.po_no} - {self.customer_name}"


# Purchase Order Status System Model
class POStatus(models.Model):
    """Purchase Order Status - Comprehensive PO tracking and payment management"""
    
    ORDER_TYPE_CHOICES = [
        ('stability', 'Stability'),
        ('tt', 'TT'),
        ('validation', 'Validation'),
        ('other', 'Other'),
    ]
    
    # Core Information Fields
    sr_no = models.AutoField(primary_key=True)
    month = models.CharField(max_length=20, help_text="Month")
    region = models.CharField(max_length=100, help_text="Region")
    company = models.CharField(max_length=200, help_text="Company Name")
    order_is_for = models.CharField(max_length=50, choices=ORDER_TYPE_CHOICES, help_text="Order is for (Stability / TT / ...)")
    
    # Order Generation Details
    po_number = models.CharField(max_length=100, help_text="PO Number")
    responsible_marketing_person = models.CharField(max_length=100, help_text="Responsible Marketing Person")
    coordinator = models.CharField(max_length=100, help_text="Coordinator")
    po_date = models.DateField(help_text="PO Date")
    po_value_without_gst = models.DecimalField(max_digits=12, decimal_places=2, help_text="PO Value (Without GST)")
    gst = models.DecimalField(max_digits=12, decimal_places=2, help_text="GST")
    po_acceptance_date = models.DateField(null=True, blank=True, help_text="PO Acceptance Date")
    wo_date = models.DateField(null=True, blank=True, help_text="WO Date")
    
    # Payment Tracking Structure - PayR-01
    payr01_agreed_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="PayR-01 Agreed Percentage")
    payr01_agreed_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="PayR-01 Agreed Amount")
    payr01_received_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="PayR-01 Received Percentage")
    payr01_received_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="PayR-01 Received Amount")
    payr01_received_date = models.DateField(null=True, blank=True, help_text="PayR-01 Received Date")
    
    # Payment Tracking Structure - PayR-02
    payr02_agreed_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="PayR-02 Agreed Percentage")
    payr02_agreed_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="PayR-02 Agreed Amount")
    payr02_received_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="PayR-02 Received Percentage")
    payr02_received_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="PayR-02 Received Amount")
    payr02_received_date = models.DateField(null=True, blank=True, help_text="PayR-02 Received Date")
    
    # Payment Tracking Structure - PayR-03
    payr03_agreed_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="PayR-03 Agreed Percentage")
    payr03_agreed_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="PayR-03 Agreed Amount")
    payr03_received_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="PayR-03 Received Percentage")
    payr03_received_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="PayR-03 Received Amount")
    payr03_received_date = models.DateField(null=True, blank=True, help_text="PayR-03 Received Date")
    
    # Payment Tracking Structure - PayR-04
    payr04_agreed_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="PayR-04 Agreed Percentage")
    payr04_agreed_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="PayR-04 Agreed Amount")
    payr04_received_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="PayR-04 Received Percentage")
    payr04_received_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="PayR-04 Received Amount")
    payr04_received_date = models.DateField(null=True, blank=True, help_text="PayR-04 Received Date")
    
    # Payment Tracking Structure - PayR-05
    payr05_agreed_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="PayR-05 Agreed Percentage")
    payr05_agreed_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="PayR-05 Agreed Amount")
    payr05_received_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="PayR-05 Received Percentage")
    payr05_received_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="PayR-05 Received Amount")
    payr05_received_date = models.DateField(null=True, blank=True, help_text="PayR-05 Received Date")
    
    # Total section
    total_agreed_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Total Agreed Amount")
    total_received_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Total Received Amount")
    
    # System fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-po_date', '-created_at']
        verbose_name = "PO Status"
        verbose_name_plural = "PO Status"
    
    def __str__(self):
        return f"{self.po_number} - {self.company}"
    
    def save(self, *args, **kwargs):
        # Calculate total amounts
        if self.po_value_without_gst:
            self.total_agreed_amount = self.po_value_without_gst
        
        # Calculate total received amount
        received_amounts = [
            self.payr01_received_amount or 0,
            self.payr02_received_amount or 0,
            self.payr03_received_amount or 0,
            self.payr04_received_amount or 0,
            self.payr05_received_amount or 0,
        ]
        self.total_received_amount = sum(received_amounts)
        
        super().save(*args, **kwargs)


# Work Order System Model
class WorkOrderFormat(models.Model):
    """Work Order Format - Comprehensive Equipment Manufacturing Template"""
    
    # Controller System Options
    CONTROLLER_CHOICES = [
        ('plc_ab', 'PLC "AB"'),
        ('plc_delta', 'PLC Delta'),
        ('digital_controller', 'Digital Controller System'),
        ('microprocessor_pid', 'Microprocessor based PID Controller'),
    ]
    
    # HMI Options
    HMI_CHOICES = [
        ('hmi_43_ab', '4.3" AB'),
        ('hmi_43_delta', '4.3" Delta'),
        ('hmi_7_ab', '7" AB'),
        ('hmi_7_delta', '7" Delta'),
        ('other_na', 'Any Other/NA'),
    ]
    
    # Door Access System Options
    DOOR_ACCESS_CHOICES = [
        ('password', 'Password Protected Door Access System'),
        ('biometric', 'Biometric Door Access System'),
        ('na', 'NA'),
    ]
    
    # Hooter System Options
    HOOTER_CHOICES = [
        ('4_chamber', 'Yes (4 Chamber Connectivity)'),
        ('8_chamber', 'Yes (8 Chamber Connectivity)'),
        ('na', 'NA'),
        ('other', 'Any Other'),
    ]
    
    # Packaging Options
    PACKAGING_CHOICES = [
        ('normal', 'Normal'),
        ('wooden', 'Wooden'),
        ('other', 'Any other'),
    ]
    
    # FAT Options
    FAT_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('depends', 'Depends'),
    ]
    
    # Header Information
    date = models.DateField(help_text="Date")
    work_order_no = models.CharField(max_length=100, help_text="Work Order No.")
    equipment_no = models.CharField(max_length=100, help_text="Equipment No.")
    delivery_date = models.DateField(help_text="Delivery Date")
    
    # Equipment Details
    equipment_type = models.CharField(max_length=200, help_text="Equipment type")
    capacity = models.CharField(max_length=50, help_text="Capacity (Ltr)")
    model = models.CharField(max_length=100, help_text="Model")
    
    # Material of Construction (MOC)
    inner_body_moc = models.CharField(max_length=100, help_text="Inner Body MOC")
    outer_body_moc = models.CharField(max_length=100, help_text="Outer Body MOC")
    
    # Dimensions
    inside_dimensions = models.CharField(max_length=100, help_text="Inside dimensions (W x D x H in MM)")
    outer_size = models.CharField(max_length=100, help_text="Outer Size (W x D x H in MM)")
    
    # Temperature Specifications
    temp_range = models.CharField(max_length=100, help_text="Temp Range")
    accuracy = models.CharField(max_length=100, help_text="Accuracy")
    uniformity = models.CharField(max_length=100, help_text="Uniformity")
    
    # Control Systems
    controller_system = models.CharField(max_length=50, choices=CONTROLLER_CHOICES, help_text="Controller System")
    hmi_system = models.CharField(max_length=50, choices=HMI_CHOICES, help_text="HMI System")
    
    # Communication & Monitoring
    gsm_system = models.BooleanField(default=False, help_text="GSM System")
    scanner = models.CharField(max_length=200, blank=True, help_text="Scanner")
    software = models.CharField(max_length=200, blank=True, help_text="Software")
    
    # Access Control
    door_access_system = models.CharField(max_length=50, choices=DOOR_ACCESS_CHOICES, help_text="Door Access System")
    
    # Alert Systems
    hooter_system = models.CharField(max_length=50, choices=HOOTER_CHOICES, help_text="Hooter System")
    
    # Physical Features
    castor_wheels = models.BooleanField(default=False, help_text="Castor Wheels")
    pipe_length = models.CharField(max_length=50, blank=True, help_text="Pipe Length (Meter/NA)")
    packaging = models.CharField(max_length=50, choices=PACKAGING_CHOICES, help_text="Packaging Options")
    fat = models.CharField(max_length=20, choices=FAT_CHOICES, help_text="FAT")
    
    # Standby System Section
    refrigeration_system = models.CharField(max_length=20, choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'NA')], help_text="Refrigeration System")
    sg_system = models.CharField(max_length=20, choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'NA')], help_text="S.G. System")
    sensor = models.CharField(max_length=20, choices=[('yes', 'Yes'), ('na', 'NA')], help_text="Sensor")
    
    # Tray & Rack Specifications
    tray_qty = models.CharField(max_length=50, help_text="Tray Qty. (Nos)")
    tray_type = models.CharField(max_length=100, default="Perforated", help_text="Tray Type")
    tray_moc = models.CharField(max_length=100, help_text="Tray MOC")
    tray_dimension = models.CharField(max_length=100, help_text="Tray Dimension (W x D x H in MM)")
    rack_qty = models.CharField(max_length=50, help_text="Rack Qty. (Nos/NA)")
    
    # Documentation Section
    protocol_documents = models.BooleanField(default=True, help_text="Protocol for DQ, IQ, and OQ, PQ Documents will be provided")
    calibration_duration = models.CharField(max_length=50, default="1 hour", help_text="Calibration duration")
    validation_duration = models.CharField(max_length=100, help_text="Validation duration (24/48/72 hours with load and 24/48/72 hours without load)")
    validation_compressor = models.CharField(max_length=100, help_text="Validation at one set point with one compressor")
    extra_validation_charge = models.BooleanField(default=True, help_text="Any extra Validation would be charged extra per day")
    calibration_probes = models.CharField(max_length=100, help_text="Calibration and Validation with probes (8/9/10/Option)")
    plc_validation = models.BooleanField(default=True, help_text="PLC Based System validation will be carried out")
    training_handover = models.BooleanField(default=True, help_text="Training and handover of documents")
    
    # Special Instructions
    special_instructions = models.TextField(blank=True, help_text="Special Instructions")
    
    # Payment Terms
    advance_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Advance Percentage")
    against_pi_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Against PI Percentage")
    after_material_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="After receiving material at site Percentage")
    
    # System fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = "Work Order Format"
        verbose_name_plural = "Work Order Formats"
    
    def __str__(self):
        return f"{self.work_order_no} - {self.equipment_type}"
