# Demo 1: Simple Webhook Rulebook

## Overview
Demonstrates the core Event-Driven Ansible workflow using a webhook event source.

**Duration:** 10 minutes  
**Complexity:** Beginner  
**Location:** Run on `workstation.lab.example.com`

## What This Demo Shows

- Basic rulebook syntax (sources, rules, conditions, actions)
- How webhooks trigger automation
- Multiple rules evaluating the same event
- Running rulebooks from command line with `ansible-rulebook`

## Setup (Before the Presentation)

**On workstation.lab.example.com:**

```bash
# Create demo directory
mkdir -p ~/demo-eda
cd ~/demo-eda

# Copy files from this directory:
# - inventory
# - webhook_example.yml
# - update_playbook.yml

# Or create them manually (see files below)
```

## Pre-Demo Checklist

- [ ] Logged into workstation as student
- [ ] Two terminal windows open
- [ ] Terminal 1: In ~/demo-eda directory
- [ ] Terminal 2: Ready for curl commands
- [ ] Files created: inventory, webhook_example.yml, update_playbook.yml

## Demo Script

### Step 1: Show the Rulebook (Terminal 1)

```bash
cd ~/demo-eda
cat webhook_example.yml
```

**Talking points:**
- "This rulebook listens for webhook events on port 5001"
- "We have two rules: one triggers a playbook, one prints debug info"
- "The first rule condition checks if message equals 'force-update'"
- "The second rule matches any event with a payload"

### Step 2: Start the Rulebook (Terminal 1)

```bash
ansible-rulebook -i inventory -r webhook_example.yml --verbose
```

**Expected output:**
```
INFO:ansible_rulebook.app:Starting sources
INFO:ansible_rulebook.app:Starting rules
INFO:ansible_rulebook.builtin:Waiting for events from webhook...
```

**Talking points:**
- "The rulebook is now running and listening for events"
- "It's waiting on port 5001 for HTTP POST requests"
- "This will run continuously until we stop it"

### Step 3: Send First Event (Terminal 2)

```bash
curl -H 'Content-Type: application/json' \
  -d '{"message": "force-update"}' \
  http://localhost:5001
```

**Watch Terminal 1 for output**

**Talking points:**
- "This event matches our first rule condition"
- "Event-Driven Ansible runs the update_playbook.yml playbook"
- "Notice how quickly this happens - milliseconds from event to action"

### Step 4: Send Second Event (Terminal 2)

```bash
curl -H 'Content-Type: application/json' \
  -d '{"message": "test-event", "source": "demo"}' \
  http://localhost:5001
```

**Watch Terminal 1 for output**

**Talking points:**
- "This event doesn't match 'force-update' so the first rule doesn't fire"
- "But it does match the second rule - event.payload is defined"
- "You can see the debug output showing the webhook payload"
- "Multiple rules can evaluate the same event"

### Step 5: Stop the Rulebook (Terminal 1)

Press `Ctrl+C`

**Talking points:**
- "In production, rulebooks run continuously in Event-Driven Ansible controller"
- "The command line is perfect for development and testing"

## Key Talking Points

1. **Event Sources:** "Webhooks are just one type of event source. Others include journald logs, Kafka topics, AWS SQS queues, and monitoring systems like Prometheus"

2. **Conditions:** "Conditions can check any field in the event data. You can use operators like ==, !=, >, <, and logical operators like and, or"

3. **Actions:** "Actions can run playbooks locally, launch job templates on automation controller, run modules, or send events back to the rule engine"

4. **Production Use:** "In production, these webhooks come from GitLab, Jenkins, ServiceNow, monitoring systems, or cloud providers"

## What Can Go Wrong

**Port already in use:**
```bash
# Check what's using port 5001
sudo lsof -i :5001

# Solution: Change port in webhook_example.yml to 5002 or another free port
```

**ansible.eda collection not installed:**
```bash
# Check if installed
ansible-galaxy collection list | grep ansible.eda

# Install if missing
ansible-galaxy collection install ansible.eda
```

**No output from curl:**
- Check you're sending to the correct port
- Verify the rulebook is still running in Terminal 1
- Check for firewall rules blocking localhost connections

## Backup Plan

If the demo fails, show the files and explain:
- "If we ran this, here's what would happen..."
- Point to the sources section: "This opens a webhook listener"
- Point to the conditions: "When this matches..."
- Point to the actions: "This playbook would run"

## Next Steps

After this demo, transition to Demo 2 which shows:
- Event-Driven Ansible controller (production deployment)
- Integration with automation controller
- Real self-healing scenario
- Complete audit trail
