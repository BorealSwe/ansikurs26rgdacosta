# Event-Driven Ansible Presentation Guide
## 1-Hour Customer Session - Day 8

## Quick Start

**Before the presentation:**
1. Read `/Users/rgdacosta/teaching/SCRIPT_DO274_EDA_Overview_teleprompter.md`
2. Test all three demos (15 minutes total)
3. Open browser tabs for documentation references
4. Prepare two terminal windows

**During the presentation:**
- Use the teleprompter script for narrative
- Run demos live from this directory
- Use talking points from demo README files
- Keep total demo time to 25-30 minutes

---

## Presentation Structure (60 minutes)

### Section 1: Introduction (10 minutes)
**Script location:** Teleprompter lines 1-60

**Key points:**
- What is Event-Driven Ansible?
- Why it matters (reactive → proactive automation)
- Real-world problem it solves

**Visual aids:**
- Show architecture diagram (Event sources → Rules → Actions)
- Use DO274 PDF Figure 1.1 (page 2)

---

### Section 2: Architecture & Components (15 minutes)
**Script location:** Teleprompter lines 61-150

**Three components to explain:**

1. **Event Sources**
   - Show list from `ansible.eda` collection
   - Mention certified content (CrowdStrike, Dynatrace, etc.)
   - Key point: "Events are notifications of interesting occurrences"

2. **Rules**
   - Conditions + Actions
   - Can have multiple rules per source
   - All matching rules fire (not just first match)

3. **Actions**
   - run_playbook (local)
   - run_job_template (automation controller)
   - run_workflow_template
   - post_event, debug, etc.

**Demo preparation:**
At end of this section, say:
> "Let me show you this in action with three real-world demonstrations"

---

### Section 3: Live Demonstrations (25-30 minutes)

#### Demo 1: Webhook Integration (10 min)
**Location:** `~/git/ansible/eda/1-webhook/`

**Setup (do before presentation):**
```bash
cd ~/git/ansible/eda/1-webhook
# Verify files exist
ls -l
```

**During presentation:**

**Terminal 1:**
```bash
cd ~/git/ansible/eda/1-webhook
cat webhook_example.yml  # Show rulebook structure
ansible-rulebook -i inventory -r webhook_example.yml --verbose
```

**Terminal 2:**
```bash
cd ~/git/ansible/eda/1-webhook
./test_webhooks.sh
```

**Talking points while running:**
- "This simulates events from Prometheus, Jenkins, GitLab"
- "Notice the condition checking - event.payload.severity == 'critical'"
- "Different rules can match the same event"
- "In production, this triggers ServiceNow tickets, Slack alerts, remediation"

**Key visual:** Show how quickly events trigger actions (milliseconds)

#### Demo 2: System Security Monitoring (10 min)
**Location:** `~/git/ansible/eda/2-journald/`

**Setup:**
```bash
cd ~/git/ansible/eda/2-journald
# May need sudo for journal access
```

**During presentation:**

**Terminal 1:**
```bash
cd ~/git/ansible/eda/2-journald
cat journald_security.yml  # Show journal monitoring
sudo ansible-rulebook -i inventory -r journald_security.yml --verbose
```

**Terminal 2:**
```bash
# Trigger failed SSH
ssh nonexistentuser@localhost
# (Try wrong password or Ctrl+C)

# Trigger sudo event
sudo whoami

# If SELinux enabled, trigger that
sudo setenforce 0  # (if permissive mode allowed)
```

**Talking points:**
- "Monitoring systemd journal in real-time, no polling"
- "Detects security events: failed SSH, sudo usage, SELinux violations"
- "Self-healing: when SELinux is disabled, automatically re-enable it"
- "Compliance: audit trail of all privilege escalation"

**Key visual:** Show immediate detection and response

#### Demo 3: Configuration Drift (8 min - optional)
**Location:** `~/git/ansible/eda/3-filewatcher/`

**Setup:**
```bash
cd ~/git/ansible/eda/3-filewatcher
mkdir -p /tmp/watched-config /tmp/watched-logs
```

**During presentation:**

**Terminal 1:**
```bash
cd ~/git/ansible/eda/3-filewatcher
ansible-rulebook -i inventory -r file_monitor.yml --verbose
```

**Terminal 2:**
```bash
# Create config file
echo "database_host=localhost" > /tmp/watched-config/app.conf

# Modify it
echo "database_host=production.example.com" > /tmp/watched-config/app.conf

# Create suspicious file
touch /tmp/watched-logs/backdoor.sh
chmod +x /tmp/watched-logs/backdoor.sh

# Delete config
rm /tmp/watched-config/app.conf
```

**Talking points:**
- "Uses Linux inotify - pushed events, not polling"
- "Automatic backup before showing changes"
- "Detects suspicious files (executables in log directories)"
- "Auto-restore deleted configuration files from backup"

**Key visual:** Show automatic backup → detect → restore workflow

---

### Section 4: Production Deployment (5 minutes)
**Script location:** Teleprompter lines 200-250

**Show (if available):**
- EDA Controller web UI
- Rule Audit screen
- Rulebook Activations
- Integration with automation controller

**If lab not available:**
Use screenshots from DO274 PDF:
- Figure 2.9 (page 74) - Rule audit list
- Figure 2.10 (page 75) - Audit details
- Figure 2.12 (page 76) - List of audit actions

**Talking points:**
- "Production uses EDA Controller, not command line"
- "Centralized management of all rulebook activations"
- "Complete audit trail for compliance"
- "Integration with automation controller for job templates"
- "Decision environments provide containerized dependencies"

---

### Section 5: Real-World Use Cases (5 minutes)
**Script location:** Teleprompter lines 150-200

**Three scenarios to highlight:**

1. **Ticket Enrichment**
   - Monitoring event → Gather diagnostics → Create ServiceNow ticket with data
   - Saves time for support teams
   - Faster mean time to resolution

2. **Self-Healing Infrastructure**
   - Known issues remediated automatically
   - Restart services, redeploy apps, fix configurations
   - Reduces on-call burden

3. **Security & Compliance**
   - Red Hat Insights integration
   - Proactive security remediation
   - Compliance audit trails (SOX, PCI-DSS, HIPAA)

**Real examples from GitHub repos:**
- Arista CloudVision integration (Red Hat Summit demo)
- ServiceNow bidirectional integration
- Slack ChatOps notifications

---

### Section 6: Q&A and Discussion (5-10 minutes)

**Common questions and answers:**

**Q:** "How is this different from cron-scheduled playbooks?"
**A:** "Cron runs at fixed times whether needed or not. EDA responds to events as they occur - it's reactive, immediate, and efficient."

**Q:** "What's the performance impact?"
**A:** "Minimal. Event sources use push notifications or efficient APIs like inotify. No continuous polling. The rulebook process itself is lightweight."

**Q:** "Can we use this with our existing Ansible content?"
**A:** "Yes! Actions can run your existing playbooks or launch your existing job templates on automation controller. No need to rewrite anything."

**Q:** "How do we test rulebooks before production?"
**A:** "Use ansible-rulebook command locally to test, then deploy the same rulebook to EDA Controller for production. The controller provides staging environments."

**Q:** "What if multiple events happen simultaneously?"
**A:** "EDA processes events concurrently. Multiple rules can match the same event. You can configure worker count and queue size for high-volume scenarios."

**Q:** "Can events come from multiple sources in one rulebook?"
**A:** "Yes, absolutely. One rulebook can have multiple event sources - webhook, journald, and file_watch all feeding rules in the same ruleset."

**Q:** "How do we handle sensitive data in events?"
**A:** "Use automation controller vault for credentials. Event payloads can be filtered. Decision environments provide isolated containers. Full audit trail shows who triggered what."

**Q:** "What happens if the rulebook crashes?"
**A:** "EDA Controller can auto-restart with configurable restart policies (always, on-failure, never). You set the policy per rulebook activation."

---

## Technical Setup Guide

### Before the Presentation (30 minutes prep time)

**1. Test your demos (15 minutes):**
```bash
# Demo 1 - Webhook
cd ~/git/ansible/eda/1-webhook
ansible-rulebook -i inventory -r webhook_example.yml --verbose &
sleep 3
./test_webhooks.sh
pkill -f ansible-rulebook

# Demo 2 - Journald (needs sudo)
cd ~/git/ansible/eda/2-journald
sudo ansible-rulebook -i inventory -r journald_security.yml --verbose &
sleep 3
sudo whoami  # Should trigger event
sudo pkill -f ansible-rulebook

# Demo 3 - File watcher
cd ~/git/ansible/eda/3-filewatcher
mkdir -p /tmp/watched-config /tmp/watched-logs
ansible-rulebook -i inventory -r file_monitor.yml --verbose &
sleep 3
echo "test" > /tmp/watched-config/test.conf
pkill -f ansible-rulebook
```

**2. Prepare your environment (5 minutes):**
```bash
# Terminal window 1: For running rulebooks
# - Full screen or large font
# - Clear background
# - No distractions in prompt

# Terminal window 2: For triggering events
# - Split screen or separate window
# - Same font size as terminal 1

# Browser tabs:
# - DO274 PDF open to architecture diagram (page 2)
# - Ansible rulebook docs: https://ansible.readthedocs.io/projects/rulebook/
# - DO274 PDF open to Figure 2.9 (Rule Audit example)
```

**3. Create a cheat sheet (10 minutes):**
```bash
# Create quick reference
cat > ~/eda-demo-commands.txt <<'EOF'
# DEMO 1 - WEBHOOK
cd ~/git/ansible/eda/1-webhook
ansible-rulebook -i inventory -r webhook_example.yml --verbose
# Terminal 2: ./test_webhooks.sh

# DEMO 2 - JOURNALD
cd ~/git/ansible/eda/2-journald
sudo ansible-rulebook -i inventory -r journald_security.yml --verbose
# Terminal 2: ssh baduser@localhost
# Terminal 2: sudo whoami

# DEMO 3 - FILEWATCHER
cd ~/git/ansible/eda/3-filewatcher
ansible-rulebook -i inventory -r file_monitor.yml --verbose
# Terminal 2: echo "test" > /tmp/watched-config/app.conf

# STOP RULEBOOK: Ctrl+C
EOF
```

---

## Troubleshooting During Presentation

### If Demo 1 (Webhook) Fails:

**Symptom:** Port already in use
**Fix:** 
```bash
# Check what's using port 5001
sudo lsof -i :5001
# Kill it or change port in webhook_example.yml
```

**Symptom:** No output from curl
**Fix:**
```bash
# Verify rulebook is still running in Terminal 1
# Check curl is targeting correct port
# Try: curl -v ... to see verbose output
```

### If Demo 2 (Journald) Fails:

**Symptom:** Permission denied
**Fix:**
```bash
# Need sudo for journal access
sudo ansible-rulebook ...
```

**Symptom:** No events triggering
**Fix:**
```bash
# Check journald is running
systemctl status systemd-journald
# Verify conditions in rulebook match actual journal fields
sudo journalctl -f  # Watch live to see actual messages
```

### If Demo 3 (File Watcher) Fails:

**Symptom:** inotify limit exceeded
**Fix:**
```bash
# Increase limit
echo 524288 | sudo tee /proc/sys/fs/inotify/max_user_watches
```

**Symptom:** No events for file changes
**Fix:**
```bash
# Verify paths are correct
ls -ld /tmp/watched-config
# Check files exist where you think they do
# Verify rulebook conditions match file extensions
```

### General Fallback Plan:

If all demos fail:
1. Show the rulebook YAML files and explain structure
2. Walk through "what would happen if we ran this"
3. Use DO274 PDF figures to show expected output
4. Focus on concepts rather than live execution
5. Engage audience with questions about their use cases

---

## Post-Presentation Follow-Up

### Materials to Send:

1. **Demo files from this repository**
   ```bash
   # Package everything
   cd ~/git/ansible
   tar czf eda-demos.tar.gz eda/
   # Send eda-demos.tar.gz to customer
   ```

2. **Reference links:**
   - DO274 course: https://www.redhat.com/en/services/training/do274-introduction-to-event-driven-ansible
   - EDA documentation: https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform/2.4/
   - Community examples: https://github.com/ansible/eda-sample-project
   - Red Hat Summit demo: https://github.com/nmartins0611/rhs-eda

3. **Next steps for customer:**
   - Identify 2-3 use cases from their environment
   - Trial Event-Driven Ansible with automation controller
   - POC with their monitoring systems (Prometheus, Splunk, etc.)
   - Integration with their ITSM (ServiceNow, Jira, etc.)

---

## Tips for Success

**Do:**
- ✅ Test all demos 30 minutes before presentation
- ✅ Have backup terminal windows ready
- ✅ Know how to quickly kill/restart rulebooks (Ctrl+C)
- ✅ Keep demos simple - they're proving concepts not complex automation
- ✅ Emphasise real-world value (time saved, incidents prevented)
- ✅ Connect to customer's pain points (on-call burden, manual remediation)

**Don't:**
- ❌ Apologise for demo failures - move to next one or explain conceptually
- ❌ Get lost in technical details - stay high-level
- ❌ Spend too long on one demo - timebox each to 10 minutes max
- ❌ Forget to stop rulebooks between demos (multiple running = confusion)
- ❌ Skip the "why it matters" narrative - demos without context are hollow

**Remember:**
- This is day 8 - they're familiar with Ansible concepts
- They're planning to use EDA - show how not theory
- Real-world context > technical perfection
- Questions indicate engagement - welcome them
- Your experience matters - share real customer stories

---

## Success Metrics

After the session, the customer should be able to:
1. ✅ Explain what Event-Driven Ansible is in one sentence
2. ✅ Describe the three components (events, rules, actions)
3. ✅ Identify 2-3 use cases relevant to their environment
4. ✅ Understand the difference between command-line and EDA Controller
5. ✅ Know how to get started (DO274 course, trial environment)

If they can do these five things, you've succeeded.
