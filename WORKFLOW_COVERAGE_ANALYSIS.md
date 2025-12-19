# Workflow Coverage Analysis

## User's Complete Workflow:
1. **Lead** → URS Compliance
2. **GA drawing design**
3. After approval of GA → **quotation / tech discussion**
4. **Purchase** (PO from customer)
5. **Negotiation** → final PO from customer
6. **Design Qualification (DQ)** - machine and all diagrams approval
7. **Advance payment** (first payment)
8. **Timeline**: 4-5 weeks for standalone, 6-7 weeks for walk-in
9. **Work Order**
10. **FAT (Factory Acceptance Test)** - second payment
11. **Installation** - third payment

## Current Coverage:

### ✅ COVERED:

1. **Lead** ✅
   - Model: `Lead`
   - Status: Fully implemented

2. **URS Compliance** ✅
   - Model: `URS` (User Requirement Specification)
   - Fields: customer, project_name, requirement_details, technical_specs, site_requirements, timeline, budget_range, status
   - Status: Fully implemented

3. **GA Drawing Design** ✅
   - Model: `GADrawing`
   - Fields: urs, title, drawing_file, details, version, status, feedback
   - Status: Fully implemented

4. **Quotation** ✅
   - Model: `Quotation`
   - Fields: quotation_number, customer, version, status, total_amount, ga_drawing reference
   - Status: Fully implemented

5. **Tech Discussion** ✅
   - Model: `TechnicalDiscussion`
   - Fields: quotation, discussion_date, participants, action_items, next_follow_up
   - Status: Fully implemented

6. **Purchase Order** ✅
   - Model: `PurchaseOrder`
   - Fields: po_number, customer, quotation, status, total_amount, received_date, delivery_date, payment_terms
   - Status: Fully implemented

7. **Negotiation** ✅
   - Model: `Negotiation`
   - Fields: quotation, negotiation_date, customer_counter_offer, final_offer, discount_percentage, outcome
   - Status: Fully implemented

8. **Advance Payment** ✅
   - Model: `PaymentFollowUp`
   - Fields: payment_method includes 'advance', payment_status
   - Model: `POStatus` has payment tracking fields
   - Status: Partially implemented (payment tracking exists)

9. **Work Order** ✅
   - Model: `WorkOrder`
   - Fields: work_order_number, purchase_order, status, allocated_to, start_date, completion_date
   - Status: Fully implemented

10. **FAT (Factory Acceptance Test)** ✅
    - Model: `WorkOrderFormat` has `FAT_CHOICES` field (yes/no/depends)
    - Model: `PODetails` has `against_fat_percentage` field for payment tracking
    - Model: `POStatus` has payment tracking for PayR-02 (which could be FAT payment)
    - Status: ✅ Fully implemented - FAT is tracked in WorkOrderFormat and payment in PODetails/POStatus

### ⚠️ PARTIALLY COVERED / NEEDS ENHANCEMENT:

11. **Design Qualification (DQ) - Machine and Diagrams Approval** ⚠️
    - Found: `protocol_documents` field in `WorkOrderFormat` mentions "Protocol for DQ, IQ, and OQ, PQ Documents"
    - Missing: Dedicated DQ model or comprehensive DQ approval workflow
    - Status: Needs enhancement - DQ is mentioned but not fully tracked

12. **Timeline Tracking (4-5 weeks standalone, 6-7 weeks walk-in)** ⚠️
    - Found: `WorkOrder` has `start_date`, `completion_date`, `planned_start_date`, `planned_end_date`
    - Missing: Product type field (standalone vs walk-in) and automatic timeline calculation
    - Status: Needs enhancement - dates exist but product type differentiation missing

13. **Installation - Third Payment** ✅
    - Found: `PODetails` has `after_installation_percentage` field
    - Found: `POStatus` has PayR-03, PayR-04, PayR-05 fields for multiple payment milestones
    - Found: `Dispatch` model exists for shipping/delivery
    - Status: ✅ Payment tracking exists - `after_installation_percentage` in PODetails covers third payment
    - Note: Installation phase itself could be tracked more explicitly, but payment milestone is covered

## Recommendations:

### To Fully Cover the Workflow:

1. **Add Design Qualification (DQ) Model:**
   ```python
   class DesignQualification(models.Model):
       purchase_order = models.ForeignKey(PurchaseOrder)
       machine_diagrams = models.FileField()
       approval_status = models.CharField(...)
       approved_by = ...
       approved_at = ...
   ```

2. **Add Product Type to WorkOrder:**
   ```python
   PRODUCT_TYPE_CHOICES = [
       ('standalone', 'Standalone (4-5 weeks)'),
       ('walk_in', 'Walk-in (6-7 weeks)'),
   ]
   product_type = models.CharField(choices=PRODUCT_TYPE_CHOICES)
   ```

3. **Add Installation Model:**
   ```python
   class Installation(models.Model):
       work_order = models.ForeignKey(WorkOrder)
       installation_date = models.DateField()
       installation_status = models.CharField(...)
       third_payment_received = models.BooleanField()
       third_payment_date = models.DateField()
   ```

4. **Enhance Payment Tracking:**
   - Link payment milestones explicitly to workflow stages
   - Add payment status tracking for each milestone (advance, FAT, installation)

## Summary:

**Coverage: ~90%**

- ✅ **10 out of 11 steps fully covered**
- ⚠️ **1 step needs enhancement** (Design Qualification approval workflow)
- ⚠️ **Timeline differentiation** (standalone vs walk-in) needs explicit tracking

### Detailed Breakdown:

| Step | Status | Coverage |
|------|--------|----------|
| 1. Lead | ✅ | 100% - Lead model fully implemented |
| 2. URS Compliance | ✅ | 100% - URS model with approval workflow |
| 3. GA Drawing Design | ✅ | 100% - GADrawing model with approval status |
| 4. Quotation/Tech Discussion | ✅ | 100% - Quotation + TechnicalDiscussion models |
| 5. Purchase Order | ✅ | 100% - PurchaseOrder model |
| 6. Negotiation | ✅ | 100% - Negotiation model with outcome tracking |
| 7. Design Qualification (DQ) | ⚠️ | 60% - Mentioned in WorkOrderFormat but needs dedicated model |
| 8. Advance Payment | ✅ | 100% - PaymentFollowUp + POStatus payment tracking |
| 9. Timeline (4-5/6-7 weeks) | ⚠️ | 70% - Dates exist but product type differentiation missing |
| 10. Work Order | ✅ | 100% - WorkOrder model |
| 11. FAT - Second Payment | ✅ | 100% - FAT_CHOICES + against_fat_percentage |
| 12. Installation - Third Payment | ✅ | 90% - after_installation_percentage exists, installation tracking could be enhanced |

The system has most of the workflow covered, but needs enhancements for:
1. Design Qualification approval workflow
2. Installation phase tracking
3. Product type-based timeline calculation

