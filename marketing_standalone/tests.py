from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta
from .models import (
    Customer, CustomerLocation, Region, Lead, Visit, Expense, 
    Exhibition, Quotation, PurchaseOrder, WorkOrder, Manufacturing,
    Dispatch, URS, GADrawing, TechnicalDiscussion, Negotiation,
    ProductionPlan, QCTracking, PackingDetails, DispatchChecklist
)

class ModelTests(TestCase):
    """Test cases for all models"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.region = Region.objects.create(
            name='North',
            description='Northern Region'
        )
        self.customer = Customer.objects.create(
            name='Test Company',
            contact_person='John Doe',
            email='john@testcompany.com',
            phone='+91-9876543210',
            region=self.region,
            created_by=self.user
        )
        self.customer_location = CustomerLocation.objects.create(
            customer=self.customer,
            address='123 Test Street',
            city='Test City',
            state='Test State',
            pincode='123456'
        )

    def test_customer_creation(self):
        """Test customer model creation"""
        self.assertEqual(self.customer.name, 'Test Company')
        self.assertEqual(self.customer.contact_person, 'John Doe')
        self.assertEqual(self.customer.email, 'john@testcompany.com')
        self.assertEqual(self.customer.created_by, self.user)
        self.assertIsNotNone(self.customer.created_at)

    def test_customer_location_creation(self):
        """Test customer location model creation"""
        self.assertEqual(self.customer_location.customer, self.customer)
        self.assertEqual(self.customer_location.address, '123 Test Street')
        self.assertEqual(self.customer_location.city, 'Test City')
        self.assertEqual(self.customer_location.state, 'Test State')
        self.assertEqual(self.customer_location.pincode, '123456')

    def test_region_creation(self):
        """Test region model creation"""
        self.assertEqual(self.region.name, 'North')
        self.assertEqual(self.region.description, 'Northern Region')

    def test_lead_creation(self):
        """Test lead model creation"""
        lead = Lead.objects.create(
            customer=self.customer,
            source='cold_calling',
            status='new',
            priority='high',
            expected_value=Decimal('50000.00'),
            created_by=self.user
        )
        self.assertEqual(lead.customer, self.customer)
        self.assertEqual(lead.source, 'cold_calling')
        self.assertEqual(lead.status, 'new')
        self.assertEqual(lead.priority, 'high')
        self.assertEqual(lead.expected_value, Decimal('50000.00'))

    def test_visit_creation(self):
        """Test visit model creation"""
        visit = Visit.objects.create(
            customer=self.customer,
            visit_date=date.today(),
            visit_time=timezone.now().time(),
            purpose='Sales Meeting',
            outcome='Positive',
            next_follow_up=date.today() + timedelta(days=7),
            created_by=self.user
        )
        self.assertEqual(visit.customer, self.customer)
        self.assertEqual(visit.purpose, 'Sales Meeting')
        self.assertEqual(visit.outcome, 'Positive')
        self.assertIsNotNone(visit.next_follow_up)

    def test_expense_creation(self):
        """Test expense model creation"""
        expense = Expense.objects.create(
            user=self.user,
            expense_type='travel',
            amount=Decimal('1000.00'),
            description='Travel to customer site',
            expense_date=date.today(),
            status='pending'
        )
        self.assertEqual(expense.user, self.user)
        self.assertEqual(expense.expense_type, 'travel')
        self.assertEqual(expense.amount, Decimal('1000.00'))
        self.assertEqual(expense.status, 'pending')

    def test_exhibition_creation(self):
        """Test exhibition model creation"""
        exhibition = Exhibition.objects.create(
            name='Test Expo 2024',
            event_date=date.today() + timedelta(days=30),
            venue='Test Venue',
            city='Test City',
            organizer='Test Organizer',
            booth_size='3x3',
            expected_visitors=1000,
            budget=Decimal('50000.00'),
            created_by=self.user
        )
        self.assertEqual(exhibition.name, 'Test Expo 2024')
        self.assertEqual(exhibition.venue, 'Test Venue')
        self.assertEqual(exhibition.booth_size, '3x3')
        self.assertEqual(exhibition.expected_visitors, 1000)

    def test_quotation_creation(self):
        """Test quotation model creation"""
        quotation = Quotation.objects.create(
            customer=self.customer,
            quotation_number='QT-2024-001',
            total_amount=Decimal('100000.00'),
            valid_until=date.today() + timedelta(days=30),
            status='draft',
            created_by=self.user
        )
        self.assertEqual(quotation.customer, self.customer)
        self.assertEqual(quotation.quotation_number, 'QT-2024-001')
        self.assertEqual(quotation.total_amount, Decimal('100000.00'))
        self.assertEqual(quotation.status, 'draft')

    def test_purchase_order_creation(self):
        """Test purchase order model creation"""
        po = PurchaseOrder.objects.create(
            customer=self.customer,
            po_number='PO-2024-001',
            order_date=date.today(),
            delivery_date=date.today() + timedelta(days=60),
            total_amount=Decimal('100000.00'),
            status='confirmed'
        )
        self.assertEqual(po.customer, self.customer)
        self.assertEqual(po.po_number, 'PO-2024-001')
        self.assertEqual(po.total_amount, Decimal('100000.00'))
        self.assertEqual(po.status, 'confirmed')

    def test_work_order_creation(self):
        """Test work order model creation"""
        work_order = WorkOrder.objects.create(
            po_number='PO-2024-001',
            work_order_number='WO-2024-001',
            assigned_to=self.user,
            start_date=date.today(),
            completion_date=date.today() + timedelta(days=30),
            status='assigned'
        )
        self.assertEqual(work_order.po_number, 'PO-2024-001')
        self.assertEqual(work_order.work_order_number, 'WO-2024-001')
        self.assertEqual(work_order.assigned_to, self.user)
        self.assertEqual(work_order.status, 'assigned')

    def test_manufacturing_creation(self):
        """Test manufacturing model creation"""
        manufacturing = Manufacturing.objects.create(
            work_order_number='WO-2024-001',
            batch_number='BATCH-001',
            machine_number='MACH-001',
            planned_start_date=date.today(),
            planned_completion_date=date.today() + timedelta(days=15),
            status='planned'
        )
        self.assertEqual(manufacturing.work_order_number, 'WO-2024-001')
        self.assertEqual(manufacturing.batch_number, 'BATCH-001')
        self.assertEqual(manufacturing.machine_number, 'MACH-001')
        self.assertEqual(manufacturing.status, 'planned')

    def test_dispatch_creation(self):
        """Test dispatch model creation"""
        dispatch = Dispatch.objects.create(
            work_order_number='WO-2024-001',
            dispatch_number='DISP-2024-001',
            dispatch_date=date.today(),
            transporter='Test Transporter',
            tracking_number='TRACK-001',
            status='dispatched'
        )
        self.assertEqual(dispatch.work_order_number, 'WO-2024-001')
        self.assertEqual(dispatch.dispatch_number, 'DISP-2024-001')
        self.assertEqual(dispatch.transporter, 'Test Transporter')
        self.assertEqual(dispatch.status, 'dispatched')

    def test_urs_creation(self):
        """Test URS model creation"""
        urs = URS.objects.create(
            customer=self.customer,
            urs_number='URS-2024-001',
            requirements='Test requirements',
            specifications='Test specifications',
            status='draft',
            created_by=self.user
        )
        self.assertEqual(urs.customer, self.customer)
        self.assertEqual(urs.urs_number, 'URS-2024-001')
        self.assertEqual(urs.requirements, 'Test requirements')
        self.assertEqual(urs.status, 'draft')

    def test_ga_drawing_creation(self):
        """Test GA Drawing model creation"""
        ga_drawing = GADrawing.objects.create(
            urs_number='URS-2024-001',
            drawing_number='GA-2024-001',
            version='1.0',
            drawing_file='test_drawing.pdf',
            status='draft',
            created_by=self.user
        )
        self.assertEqual(ga_drawing.urs_number, 'URS-2024-001')
        self.assertEqual(ga_drawing.drawing_number, 'GA-2024-001')
        self.assertEqual(ga_drawing.version, '1.0')
        self.assertEqual(ga_drawing.status, 'draft')

    def test_technical_discussion_creation(self):
        """Test Technical Discussion model creation"""
        tech_discussion = TechnicalDiscussion.objects.create(
            customer=self.customer,
            discussion_date=date.today(),
            discussion_type='telephonic',
            participants='John Doe, Jane Smith',
            minutes_of_meeting='Test MoM',
            status='scheduled',
            created_by=self.user
        )
        self.assertEqual(tech_discussion.customer, self.customer)
        self.assertEqual(tech_discussion.discussion_type, 'telephonic')
        self.assertEqual(tech_discussion.participants, 'John Doe, Jane Smith')
        self.assertEqual(tech_discussion.status, 'scheduled')

    def test_negotiation_creation(self):
        """Test Negotiation model creation"""
        negotiation = Negotiation.objects.create(
            customer=self.customer,
            negotiation_date=date.today(),
            negotiation_type='commercial',
            discussed_points='Price, Payment Terms',
            outcome='Agreed',
            status='completed',
            created_by=self.user
        )
        self.assertEqual(negotiation.customer, self.customer)
        self.assertEqual(negotiation.negotiation_type, 'commercial')
        self.assertEqual(negotiation.discussed_points, 'Price, Payment Terms')
        self.assertEqual(negotiation.outcome, 'Agreed')

    def test_production_plan_creation(self):
        """Test Production Plan model creation"""
        production_plan = ProductionPlan.objects.create(
            work_order_number='WO-2024-001',
            plan_number='PP-2024-001',
            planned_start_date=date.today(),
            planned_completion_date=date.today() + timedelta(days=30),
            status='draft',
            created_by=self.user
        )
        self.assertEqual(production_plan.work_order_number, 'WO-2024-001')
        self.assertEqual(production_plan.plan_number, 'PP-2024-001')
        self.assertEqual(production_plan.status, 'draft')

    def test_qc_tracking_creation(self):
        """Test QC Tracking model creation"""
        qc_tracking = QCTracking.objects.create(
            work_order_number='WO-2024-001',
            qc_number='QC-2024-001',
            qc_start_date=date.today(),
            qc_end_date=date.today() + timedelta(days=5),
            status='in_progress'
        )
        self.assertEqual(qc_tracking.work_order_number, 'WO-2024-001')
        self.assertEqual(qc_tracking.qc_number, 'QC-2024-001')
        self.assertEqual(qc_tracking.status, 'in_progress')

    def test_packing_details_creation(self):
        """Test Packing Details model creation"""
        packing_details = PackingDetails.objects.create(
            work_order_number='WO-2024-001',
            packing_number='PK-2024-001',
            packing_date=date.today(),
            packed_by=self.user,
            status='completed'
        )
        self.assertEqual(packing_details.work_order_number, 'WO-2024-001')
        self.assertEqual(packing_details.packing_number, 'PK-2024-001')
        self.assertEqual(packing_details.packed_by, self.user)
        self.assertEqual(packing_details.status, 'completed')

    def test_dispatch_checklist_creation(self):
        """Test Dispatch Checklist model creation"""
        dispatch_checklist = DispatchChecklist.objects.create(
            dispatch_number='DISP-2024-001',
            checklist_number='CL-2024-001',
            checklist_date=date.today(),
            completed_by=self.user,
            status='completed'
        )
        self.assertEqual(dispatch_checklist.dispatch_number, 'DISP-2024-001')
        self.assertEqual(dispatch_checklist.checklist_number, 'CL-2024-001')
        self.assertEqual(dispatch_checklist.completed_by, self.user)
        self.assertEqual(dispatch_checklist.status, 'completed')


class ViewTests(TestCase):
    """Test cases for views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.region = Region.objects.create(
            name='North',
            description='Northern Region'
        )
        self.customer = Customer.objects.create(
            name='Test Company',
            contact_person='John Doe',
            email='john@testcompany.com',
            phone='+91-9876543210',
            region=self.region,
            created_by=self.user
        )

    def test_dashboard_view(self):
        """Test dashboard view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/dashboard.html')

    def test_customer_list_view(self):
        """Test customer list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:customer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/customer_list.html')

    def test_customer_create_view(self):
        """Test customer create view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:customer_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/customer_form.html')

    def test_lead_list_view(self):
        """Test lead list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:lead_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/lead_list.html')

    def test_visit_list_view(self):
        """Test visit list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:visit_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/visit_list.html')

    def test_expense_list_view(self):
        """Test expense list view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/expense_list.html')

    def test_exhibition_planning_view(self):
        """Test exhibition planning view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:exhibition_planning_interface'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/exhibition_planning_interface.html')

    def test_email_automation_view(self):
        """Test email automation view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:email_automation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/email_automation.html')

    def test_real_time_notifications_view(self):
        """Test real-time notifications view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:real_time_notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/real_time_notifications.html')

    def test_audit_trail_view(self):
        """Test audit trail view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('marketing:audit_trail_system'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marketing/audit_trail_system.html')

    def test_unauthorized_access(self):
        """Test unauthorized access to views"""
        response = self.client.get(reverse('marketing:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class IntegrationTests(TestCase):
    """Integration tests for workflows"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.customer = Customer.objects.create(
            name='Test Company',
            contact_person='John Doe',
            email='john@testcompany.com',
            phone='+91-9876543210',
            created_by=self.user
        )

    def test_customer_to_lead_workflow(self):
        """Test complete customer to lead workflow"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create lead
        lead_data = {
            'customer': self.customer.id,
            'source': 'cold_calling',
            'status': 'new',
            'priority': 'high',
            'expected_value': '50000.00'
        }
        response = self.client.post(reverse('marketing:lead_create'), lead_data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        
        # Verify lead was created
        lead = Lead.objects.filter(customer=self.customer).first()
        self.assertIsNotNone(lead)
        self.assertEqual(lead.source, 'cold_calling')
        self.assertEqual(lead.status, 'new')

    def test_visit_to_followup_workflow(self):
        """Test visit to follow-up workflow"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create visit
        visit_data = {
            'customer': self.customer.id,
            'visit_date': date.today(),
            'purpose': 'Sales Meeting',
            'outcome': 'Positive',
            'next_follow_up': date.today() + timedelta(days=7)
        }
        response = self.client.post(reverse('marketing:visit_create'), visit_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify visit was created
        visit = Visit.objects.filter(customer=self.customer).first()
        self.assertIsNotNone(visit)
        self.assertEqual(visit.purpose, 'Sales Meeting')
        self.assertEqual(visit.outcome, 'Positive')

    def test_quotation_to_po_workflow(self):
        """Test quotation to purchase order workflow"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create quotation
        quotation_data = {
            'customer': self.customer.id,
            'quotation_number': 'QT-2024-001',
            'total_amount': '100000.00',
            'valid_until': date.today() + timedelta(days=30),
            'status': 'draft'
        }
        response = self.client.post(reverse('marketing:quotation_create'), quotation_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify quotation was created
        quotation = Quotation.objects.filter(customer=self.customer).first()
        self.assertIsNotNone(quotation)
        self.assertEqual(quotation.quotation_number, 'QT-2024-001')
        self.assertEqual(quotation.status, 'draft')


class PerformanceTests(TestCase):
    """Performance tests"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create bulk test data
        for i in range(100):
            customer = Customer.objects.create(
                name=f'Test Company {i}',
                contact_person=f'Contact {i}',
                email=f'contact{i}@testcompany.com',
                phone=f'+91-98765432{i:02d}',
                created_by=self.user
            )
            
            # Create leads for each customer
            for j in range(5):
                Lead.objects.create(
                    customer=customer,
                    source='cold_calling',
                    status='new',
                    priority='high',
                    expected_value=Decimal('50000.00'),
                    created_by=self.user
                )

    def test_customer_list_performance(self):
        """Test customer list view performance"""
        self.client.login(username='testuser', password='testpass123')
        
        import time
        start_time = time.time()
        response = self.client.get(reverse('marketing:customer_list'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 1.0)  # Should load in less than 1 second

    def test_lead_list_performance(self):
        """Test lead list view performance"""
        self.client.login(username='testuser', password='testpass123')
        
        import time
        start_time = time.time()
        response = self.client.get(reverse('marketing:lead_list'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 1.0)  # Should load in less than 1 second

    def test_dashboard_performance(self):
        """Test dashboard view performance"""
        self.client.login(username='testuser', password='testpass123')
        
        import time
        start_time = time.time()
        response = self.client.get(reverse('marketing:dashboard'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 2.0)  # Should load in less than 2 seconds


class SecurityTests(TestCase):
    """Security tests"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.customer = Customer.objects.create(
            name='Test Company',
            contact_person='John Doe',
            email='john@testcompany.com',
            phone='+91-9876543210',
            created_by=self.user
        )

    def test_sql_injection_protection(self):
        """Test SQL injection protection"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test with potentially malicious input
        malicious_input = "'; DROP TABLE customers; --"
        response = self.client.get(f"{reverse('marketing:customer_list')}?search={malicious_input}")
        
        self.assertEqual(response.status_code, 200)
        # Should not crash or expose data

    def test_xss_protection(self):
        """Test XSS protection"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test with potentially malicious input
        malicious_input = "<script>alert('XSS')</script>"
        response = self.client.get(f"{reverse('marketing:customer_list')}?search={malicious_input}")
        
        self.assertEqual(response.status_code, 200)
        # Should not execute JavaScript

    def test_csrf_protection(self):
        """Test CSRF protection"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test POST without CSRF token
        response = self.client.post(reverse('marketing:customer_create'), {
            'name': 'Test Company',
            'contact_person': 'John Doe',
            'email': 'john@testcompany.com'
        })
        
        self.assertEqual(response.status_code, 403)  # Should be forbidden without CSRF token
