#!/bin/bash

# Test HRMS API connectivity from Docker container
# Usage: docker-compose exec web ./test_hrms_connectivity.sh

HRMS_URL="${HRMS_RBAC_API_URL:-https://hrms.aureolegroup.com/api/rbac}"

echo "=========================================="
echo "Testing HRMS API Connectivity"
echo "=========================================="
echo ""
echo "HRMS API URL: $HRMS_URL"
echo ""

# Test basic connectivity
echo "1. Testing DNS resolution..."
if host hrms.aureolegroup.com > /dev/null 2>&1; then
    echo "✅ DNS resolution successful"
else
    echo "❌ DNS resolution failed"
fi

echo ""
echo "2. Testing HTTP connectivity..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$HRMS_URL/login/" 2>&1)
if [ "$HTTP_CODE" = "405" ] || [ "$HTTP_CODE" = "400" ] || [ "$HTTP_CODE" = "200" ]; then
    echo "✅ HTTP connectivity successful (Status: $HTTP_CODE)"
elif [ "$HTTP_CODE" = "502" ]; then
    echo "❌ Bad Gateway (502) - HRMS server is unreachable"
elif [ "$HTTP_CODE" = "000" ]; then
    echo "❌ Connection failed - Cannot reach server"
else
    echo "⚠️  HTTP Status: $HTTP_CODE"
fi

echo ""
echo "3. Testing SSL certificate..."
SSL_TEST=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -k "$HRMS_URL/login/" 2>&1)
if [ "$SSL_TEST" != "000" ]; then
    echo "✅ SSL connection possible (with -k flag)"
else
    echo "❌ SSL connection failed"
fi

echo ""
echo "4. Full curl test with verbose output..."
echo "----------------------------------------"
curl -v --max-time 10 "$HRMS_URL/login/" 2>&1 | head -30
echo ""
echo "=========================================="

