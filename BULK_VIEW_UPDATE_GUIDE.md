# Bulk View Update Guide

Due to the large number of views that need updating (58+ occurrences), here's a systematic approach:

## Pattern to Replace

**Find:**
```python
created_by=request.user
```

**Replace with:**
```python
# Get user info from HRMS session
user_info = get_user_info_dict(request)

# In model creation:
created_by_user_id=user_info['user_id'],
created_by_username=user_info['username'],
created_by_email=user_info['email'],
created_by_full_name=user_info['full_name'],
```

## Field Mappings

- `created_by=request.user` → `created_by_*` fields
- `assigned_to=request.user` → `assigned_to_*` fields  
- `approved_by=request.user` → `approved_by_*` fields
- `verified_by=request.user` → `verified_by_*` fields
- `allocated_to=request.user` → `allocated_to_*` fields
- `performed_by=request.user` → `performed_by_*` fields
- `inspector=request.user` → `inspector_*` fields
- `packed_by=request.user` → `packed_by_*` fields
- `completed_by=request.user` → `completed_by_*` fields
- `manager=request.user` → `manager_*` fields

## Special Cases

For `Expense` model:
- `user=request.user` → `expense_user_id`, `expense_username`, etc.

For `VisitParticipant` model:
- `user=request.user` → `participant_user_id`, `participant_username`, etc.

## Files to Update

All occurrences are in: `b4th-Marketing/marketing_app/views.py`

## Status

✅ Models updated
✅ Migration created
⏳ Views update in progress (58+ occurrences found)

