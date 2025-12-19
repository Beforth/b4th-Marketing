#!/bin/bash

# Test HRMS RBAC API Login
# Usage: ./test_hrms_api.sh <username> <password>

BASE_URL="https://hrms.aureolegroup.com/api/rbac"
USERNAME="${1:-admin}"
PASSWORD="${2:-password}"

echo "Testing HRMS RBAC API Login"
echo "============================"
echo "Base URL: $BASE_URL"
echo "Username: $USERNAME"
echo ""

# Test Login
echo "1. Testing Login..."
curl -X POST "$BASE_URL/login/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" \
  -w "\n\nHTTP Status: %{http_code}\n" \
  -v

echo ""
echo ""
echo "2. If login successful, test getting user info with token:"
echo "   Replace TOKEN_HERE with the token from login response"
echo ""
echo "curl -X GET \"$BASE_URL/user/info/\" \\"
echo "  -H \"Authorization: Token TOKEN_HERE\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -H \"Accept: application/json\""

