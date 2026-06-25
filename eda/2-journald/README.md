# Demo 2: System Journal Monitoring with Event-Driven Ansible

## Overview
Real-world demonstration of monitoring system journal events for security and compliance automation.

**Duration:** 10 minutes  
**Complexity:** Intermediate  
**Location:** Any RHEL 9 / Fedora / CentOS Stream system with systemd

## What This Demo Shows

- Monitoring systemd journal logs in real-time
- Detecting security events (failed SSH logins, SELinux denials, sudo usage)
- Automating incident response
- Self-healing infrastructure patterns

## Real-World Use Cases

1. **Security Incident Response** - Detect and respond to failed login attempts
2. **Compliance Automation** - Monitor and remediate SELinux policy violations
3. **Privilege Escalation Auditing** - Track and log all sudo commands
4. **Service Monitoring** - Detect service failures and auto-restart

## Setup (Before the Presentation)

**Requirements:**
- RHEL 9, Fedora, or CentOS Stream (any system with systemd-journald)
- ansible-rulebook installed
- ansible.eda collection installed
- Root or sudo access

```bash
# Create demo directory
mkdir -p ~/demo-journald
cd ~/demo-journald

# Files needed (see below):
# - inventory
# - journald_security.yml
# - handle_failed_ssh.yml
# - handle_selinux_denial.yml
# - handle_sudo_usage.yml
```

## Pre-Demo Checklist

- [ ] Logged into demo system with sudo access
- [ ] Two terminal windows open
- [ ] Terminal 1: For running ansible-rulebook
- [ ] Terminal 2: For triggering events (SSH failures, sudo commands)
- [ ] Files created in ~/demo-journald

## Demo Script

### Step 1: Show the Rulebook (Terminal 1)

```bash
cd ~/demo-journald
cat journald_security.yml
```

**Talking points:**
- "This rulebook monitors systemd journal in real-time"
- "We're watching for three types of security events"
- "Failed SSH attempts, SELinux denials, and sudo command usage"
- "Each event type triggers a different automated response"

### Step 2: Start the Rulebook (Terminal 1)

```bash
ansible-rulebook -i inventory -r journald_security.yml --verbose
```

**Expected output:**
```
INFO:ansible_rulebook.app:Starting sources
INFO:ansible_rulebook.app:Starting rules
INFO:ansible_rulebook.builtin:Waiting for events from journald...
```

**Talking points:**
- "Event-Driven Ansible is now monitoring the journal in real-time"
- "It's watching for specific patterns in log messages"
- "This runs continuously, 24/7 in production"

### Step 3: Trigger Failed SSH Event (Terminal 2)

```bash
# Attempt SSH with wrong password to localhost
ssh wronguser@localhost
# (Type wrong password or Ctrl+C to abort)
```

**Watch Terminal 1 for the rulebook response**

**Talking points:**
- "The failed SSH attempt generated a journal entry"
- "Event-Driven Ansible detected it immediately"
- "The playbook runs to log the event and could block the IP"
- "In production, this might create a ServiceNow ticket or update a firewall"

### Step 4: Trigger SELinux Event (Terminal 2)

```bash
# Generate an SELinux denial (example varies by system)
# Option 1: Try to execute a file from /tmp with noexec
sudo touch /tmp/testscript
sudo chmod +x /tmp/testscript
sudo /tmp/testscript

# Option 2: Check for existing denials
sudo ausearch -m avc -ts recent
```

**Watch Terminal 1**

**Talking points:**
- "SELinux denials appear in the journal"
- "These could indicate misconfigurations or security issues"
- "Automated response logs the denial for security team review"
- "Could trigger automatic remediation in permissive environments"

### Step 5: Trigger Sudo Event (Terminal 2)

```bash
sudo whoami
```

**Watch Terminal 1**

**Talking points:**
- "Every sudo command is logged in the journal"
- "Event-Driven Ansible captures privilege escalation events"
- "For compliance, we audit who is using elevated privileges"
- "Could alert security team for sensitive commands"

### Step 6: Stop the Rulebook (Terminal 1)

Press `Ctrl+C`

## Key Talking Points

1. **Real-Time Monitoring:** "Unlike parsing log files after the fact, Event-Driven Ansible reacts in real-time as events occur"

2. **No Polling Required:** "The journald event source uses the journal API, so there's no CPU-intensive log file polling"

3. **Structured Data:** "Journal events include structured metadata - we can match on specific fields like SYSLOG_IDENTIFIER, PRIORITY, or MESSAGE"

4. **Production Patterns:**
   - Failed SSH → Update firewall rules (fail2ban-style)
   - SELinux denial → Create ticket for security review
   - Sudo usage → Audit log for compliance reporting
   - Service failure → Auto-restart service

## Advanced Matching Examples

**Match by systemd unit:**
```yaml
condition: event.journald.SYSLOG_IDENTIFIER == "sshd"
```

**Match by priority (severity):**
```yaml
condition: event.journald.PRIORITY == "3"  # Error level
```

**Match by message content:**
```yaml
condition: event.journald.MESSAGE matches ".*Failed password.*"
```

**Complex conditions:**
```yaml
condition: >
  event.journald._COMM == "sudo" and
  event.journald.MESSAGE matches ".*COMMAND.*"
```

## What Can Go Wrong

**No journal events appearing:**
```bash
# Check journald is running
systemctl status systemd-journald

# Check you have permission to read journal
sudo journalctl -f
```

**Event source fails to start:**
- Ensure you have python3-systemd installed
- Check SELinux isn't blocking journal access
- Run with sudo if permission denied

**Too many events:**
- Refine your conditions to be more specific
- Filter by SYSLOG_IDENTIFIER or other structured fields
- Use the match keyword for pattern matching

## Production Deployment Notes

**In production with EDA Controller:**
1. Rulebook runs on each monitored host OR
2. Central journal collection (rsyslog → centralized journal) OR
3. Use event forwarders (journal → Kafka → EDA)

**Scaling considerations:**
- One rulebook activation per host for local monitoring
- Centralized pattern for enterprise-wide monitoring
- Filter early to reduce event processing load

**Security:**
- Journal access requires appropriate permissions
- Use decision environments with python3-systemd
- Audit rule activations themselves (who started/stopped)

## Next Steps

After this demo, transition to Demo 3 which shows:
- File system monitoring with file_watch
- Detecting configuration changes
- Auto-remediation of unauthorized changes
