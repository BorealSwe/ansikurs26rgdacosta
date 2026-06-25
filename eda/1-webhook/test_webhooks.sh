#!/usr/bin/env bash
#
# Test webhook events for Event-Driven Ansible demo
#

WEBHOOK_URL="http://localhost:5001"

echo "Testing Event-Driven Ansible Webhooks"
echo "======================================"
echo ""

# Test 1: Critical alert
echo "[Test 1] Sending critical alert..."
curl -s -H 'Content-Type: application/json' \
  -d '{
    "severity": "critical",
    "source": "Prometheus",
    "message": "Database connection pool exhausted",
    "host": "db-prod-01",
    "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"
  }' \
  "$WEBHOOK_URL"
echo ""
echo "✓ Critical alert sent"
echo ""
sleep 2

# Test 2: Service deployment
echo "[Test 2] Triggering service deployment..."
curl -s -H 'Content-Type: application/json' \
  -d '{
    "action": "deploy",
    "service": "api-gateway",
    "version": "v2.3.1",
    "environment": "production",
    "user": "jenkins-ci"
  }' \
  "$WEBHOOK_URL"
echo ""
echo "✓ Deployment webhook sent"
echo ""
sleep 2

# Test 3: Generic event (will only match debug rule)
echo "[Test 3] Sending generic monitoring event..."
curl -s -H 'Content-Type: application/json' \
  -d '{
    "source": "Nagios",
    "message": "Disk usage at 75% on web-server-03",
    "severity": "warning"
  }' \
  "$WEBHOOK_URL"
echo ""
echo "✓ Generic event sent (should only match debug rule)"
echo ""

echo "======================================"
echo "All test webhooks sent!"
echo "Check the ansible-rulebook terminal for output"
