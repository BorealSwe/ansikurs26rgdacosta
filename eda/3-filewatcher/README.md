# Demo 3: File System Monitoring with Event-Driven Ansible

## Overview
Real-world demonstration of monitoring file system changes for configuration management and security.

**Duration:** 10 minutes  
**Complexity:** Intermediate  
**Location:** Any Linux system with ansible-rulebook

## What This Demo Shows

- Real-time file system monitoring
- Detecting unauthorized configuration changes
- Automatic backup and remediation
- Configuration drift detection and correction

## Real-World Use Cases

1. **Configuration Management** - Detect and revert unauthorized /etc changes
2. **Security Monitoring** - Detect new files in sensitive directories
3. **Compliance** - Audit and log all changes to critical files
4. **Incident Response** - Alert when suspicious files appear

## Setup (Before the Presentation)

**Requirements:**
- Any Linux system
- ansible-rulebook installed
- ansible.eda collection installed

```bash
# Create demo directory and monitored paths
mkdir -p ~/filewatcher-demo
mkdir -p /tmp/watched-config
mkdir -p /tmp/watched-logs

cd ~/filewatcher-demo

# Files needed:
# - inventory
# - file_monitor.yml
# - handle_config_change.yml
# - handle_new_file.yml
# - handle_file_deletion.yml
```

## Pre-Demo Checklist

- [ ] Two terminal windows open
- [ ] Terminal 1: For running ansible-rulebook
- [ ] Terminal 2: For creating/modifying/deleting files
- [ ] Directories created: /tmp/watched-config and /tmp/watched-logs
- [ ] Files created in ~/filewatcher-demo

## Demo Script

### Step 1: Show the Rulebook (Terminal 1)

```bash
cd ~/filewatcher-demo
cat file_monitor.yml
```

**Talking points:**
- "This rulebook monitors two directories for file system events"
- "/tmp/watched-config simulates critical configuration files"
- "/tmp/watched-logs simulates log directories"
- "We detect creates, modifies, and deletes in real-time"

### Step 2: Start the Rulebook (Terminal 1)

```bash
ansible-rulebook -i inventory -r file_monitor.yml --verbose
```

**Expected output:**
```
INFO:ansible_rulebook.app:Starting sources
INFO:ansible_rulebook.app:Starting rules
INFO:ansible_rulebook.builtin:Watching /tmp/watched-config for changes...
INFO:ansible_rulebook.builtin:Watching /tmp/watched-logs for changes...
```

**Talking points:**
- "Event-Driven Ansible is now watching both directories"
- "It uses inotify on Linux, so there's no polling overhead"
- "Changes are detected immediately, in real-time"

### Step 3: Create a New Configuration File (Terminal 2)

```bash
echo "database_host=localhost" > /tmp/watched-config/app.conf
```

**Watch Terminal 1 for the rulebook response**

**Talking points:**
- "A new configuration file was created"
- "Event-Driven Ansible detected it immediately"
- "The playbook runs to back up the file and log the change"
- "In production, this might validate the config and alert admins"

### Step 4: Modify the Configuration File (Terminal 2)

```bash
echo "database_host=production-db.company.com" > /tmp/watched-config/app.conf
```

**Watch Terminal 1**

**Talking points:**
- "The modification was detected"
- "This triggers the config change handler"
- "In production, you might:"
  - "Compare against known-good config"
  - "Auto-revert unauthorized changes"
  - "Create a ServiceNow change ticket"
  - "Alert the ops team"

### Step 5: Create a Suspicious File (Terminal 2)

```bash
touch /tmp/watched-logs/backdoor.sh
chmod +x /tmp/watched-logs/backdoor.sh
```

**Watch Terminal 1**

**Talking points:**
- "Executable files in log directories are suspicious"
- "This could indicate a security breach"
- "Event-Driven Ansible alerts the security team"
- "Could automatically quarantine the file"

### Step 6: Delete a File (Terminal 2)

```bash
rm /tmp/watched-config/app.conf
```

**Watch Terminal 1**

**Talking points:**
- "File deletion is detected"
- "This might trigger:"
  - "Restore from backup"
  - "Alert that critical config is missing"
  - "Prevent service restart until resolved"

### Step 7: Stop the Rulebook (Terminal 1)

Press `Ctrl+C`

## Key Talking Points

1. **Zero Polling Overhead:** "Uses Linux inotify API - events are pushed, not polled"

2. **Recursive Monitoring:** "Can watch entire directory trees recursively"

3. **Event Types Detected:**
   - File created
   - File modified  
   - File deleted
   - File moved/renamed
   - Permissions changed
   - Directory created/removed

4. **Production Patterns:**
   - `/etc` monitoring → detect unauthorized config changes
   - `/var/www/html` → detect website defacement
   - `/home` → detect new SSH keys or .bashrc changes
   - `/tmp` → detect suspicious executable files
   - Certificate directories → auto-renew expiring certs

## Advanced File Watching

**Watch specific file types:**
```yaml
sources:
  - ansible.eda.file_watch:
      path: /etc
      recursive: true
      patterns:
        - "*.conf"
        - "*.cfg"
```

**Exclude certain paths:**
```yaml
sources:
  - ansible.eda.file_watch:
      path: /var/log
      recursive: true
      ignore_patterns:
        - "*.tmp"
        - ".git/*"
```

**Different event types:**
```yaml
rules:
  - name: File created
    condition: event.file.event_type == "created"
    
  - name: File modified  
    condition: event.file.event_type == "modified"
    
  - name: File deleted
    condition: event.file.event_type == "deleted"
    
  - name: Permissions changed
    condition: event.file.event_type == "changed"
```

## What Can Go Wrong

**No events appearing:**
```bash
# Check inotify limits
cat /proc/sys/fs/inotify/max_user_watches

# Increase if needed (as root)
echo 524288 | sudo tee /proc/sys/fs/inotify/max_user_watches
```

**Too many events:**
- Use ignore_patterns to exclude noisy files (.swp, .tmp)
- Don't watch /proc, /sys, or other virtual filesystems
- Be specific with patterns - don't watch everything

**Permission denied:**
- Ensure ansible-rulebook can read the monitored directories
- May need to run with elevated privileges for system paths

## Production Deployment Patterns

**Pattern 1: Configuration Drift Detection**
```
Watch /etc → Detect change → Compare against git repo → Auto-revert or alert
```

**Pattern 2: Security Monitoring**
```
Watch /tmp, /var/tmp → Detect .sh, .elf files → Quarantine + alert security
```

**Pattern 3: Certificate Management**
```
Watch /etc/pki → Detect expiring cert → Run renewal playbook → Reload services
```

**Pattern 4: Log Analysis Trigger**
```
Watch /var/log → New error.log → Run log parser → Create incidents
```

## Scaling Considerations

**Per-Host Monitoring:**
- One rulebook activation per host
- Monitors local filesystem only
- Low resource overhead

**Centralized Pattern:**
- Hosts write changes to message bus (Kafka, MQTT)
- Central EDA controller processes events
- Better for large-scale deployments

**Hybrid Approach:**
- Local monitoring for immediate response
- Also forward to central SIEM for correlation
- Best of both worlds

## Next Steps

After completing all three demos, you've shown:
1. **Webhooks** - External system integration
2. **Journald** - System event monitoring
3. **File Watch** - Configuration management

These three patterns cover the majority of real-world Event-Driven Ansible use cases.
