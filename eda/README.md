# Event-Driven Ansible Demonstrations
## DO274 Customer Presentation

Three real-world demonstrations showing Event-Driven Ansible patterns for production environments.

## Directory Structure

```
eda/
├── README.md                    # This file
├── 1-webhook/                   # Webhook integration (monitoring, CI/CD)
├── 2-journald/                  # System security monitoring
├── 3-filewatcher/               # Configuration drift detection
└── ansible.cfg                  # Shared Ansible configuration
```

## Prerequisites

**For Real-World Demos (Recommended):**
- Any RHEL 9, Fedora, or CentOS Stream system
- ansible-rulebook package installed
- ansible.eda collection installed

**For DO274 Lab Environment:**
- Access to `workstation.lab.example.com`
- Student credentials
- All VMs running

## Installation

```bash
# Install ansible-rulebook (if not already installed)
sudo dnf install ansible-rulebook

# Install ansible.eda collection
ansible-galaxy collection install ansible.eda

# Verify installation
ansible-rulebook --version
ansible-galaxy collection list | grep ansible.eda
```

## Running the Demos

Each demonstration is standalone and can be run independently:

### 1. Webhook Integration (1-webhook/)
**Duration:** 10 minutes  
**Complexity:** Beginner  
**Shows:** External system integration via HTTP webhooks

Simulates receiving events from:
- Monitoring systems (Prometheus, Nagios)
- CI/CD pipelines (GitLab, Jenkins)
- Cloud providers (AWS, Azure)

```bash
cd 1-webhook
cat README.md  # Full instructions
```

### 2. System Security Monitoring (2-journald/)
**Duration:** 10 minutes  
**Complexity:** Intermediate  
**Shows:** Real-time system log monitoring for security events

Detects and responds to:
- Failed SSH login attempts
- SELinux policy violations
- Sudo command usage
- Service failures

```bash
cd 2-journald
cat README.md  # Full instructions
```

### 3. Configuration Drift Detection (3-filewatcher/)
**Duration:** 10 minutes  
**Complexity:** Intermediate  
**Shows:** File system monitoring for configuration management

Monitors for:
- Unauthorized configuration changes
- File creation/modification/deletion
- Suspicious executable files
- Automatic backup and remediation

```bash
cd 3-filewatcher
cat README.md  # Full instructions
```

## Demo Sequence

**Recommended order for presentations:**
1. Start with 1-webhook (simplest concept)
2. Progress to 2-journald (security focus)
3. Finish with 3-filewatcher (configuration management)

**Time allocation:**
- Setup/intro: 5 min
- Demo 1: 10 min
- Demo 2: 10 min
- Demo 3: 10 min (optional)
- Discussion: 5+ min

Total: 35-40 minutes of demonstrations

## Real-World Context

These demonstrations are based on actual production patterns used by Red Hat customers:

**Webhook Pattern:**
- ServiceNow integration for incident management
- GitLab/GitHub webhooks for GitOps workflows
- Prometheus Alertmanager for infrastructure monitoring

**Journal Pattern:**
- Security incident response (SIEM integration)
- Compliance auditing (SOX, PCI-DSS, HIPAA)
- Self-healing infrastructure

**File Watch Pattern:**
- Configuration drift detection
- Unauthorized change prevention
- Certificate expiration monitoring
- Web defacement detection

## Extending the Demos

Each demo includes comments showing production extensions:
- ServiceNow ticket creation
- Slack/Teams notifications
- PagerDuty alerting
- Firewall rule updates
- Automatic remediation playbooks

## Troubleshooting

**ansible-rulebook not found:**
```bash
sudo dnf install ansible-rulebook
```

**ansible.eda collection missing:**
```bash
ansible-galaxy collection install ansible.eda
```

**Permission denied on journald:**
```bash
# Run with sudo for journal access
sudo ansible-rulebook -i inventory -r journald_security.yml
```

**Port already in use (webhook demos):**
```bash
# Change port in rulebook from 5001 to another port
# Edit webhook_example.yml and modify port: 5001 to port: 5002
```

**inotify limits (file watcher):**
```bash
# Check current limit
cat /proc/sys/fs/inotify/max_user_watches

# Increase if needed
echo 524288 | sudo tee /proc/sys/fs/inotify/max_user_watches
```

## Additional Resources

**Official Documentation:**
- [Ansible Rulebook Docs](https://ansible.readthedocs.io/projects/rulebook/)
- [Event Source Plugins](https://ansible.readthedocs.io/projects/rulebook/en/latest/sources.html)
- [Red Hat EDA Documentation](https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform/2.4/)

**Example Repositories:**
- [Red Hat Summit EDA Demo](https://github.com/nmartins0611/rhs-eda) - Arista CloudVision integration
- [EDA Sample Project](https://github.com/ansible/eda-sample-project) - Official examples
- [Splunk EDA Plugin](https://github.com/nmartins0611/splunk-eda-plugin) - Event source plugins

**YouTube:**
- Ansible Automation Platform Playlist: PLduOGJoEf2a3fF2a3fIF5uaoyGV526ilwD97R

## Configuration Files

**ansible.cfg** (in this directory):
Shared configuration for all demos
- Disables host key checking for demos
- Sets inventory location
- Configures stdout callback for better output

**Common files in each demo:**
- `inventory` - Localhost target
- `*.yml` - Rulebooks (event sources, rules, conditions, actions)
- `*_playbook.yml` - Ansible playbooks triggered by rules
- `README.md` - Step-by-step demonstration guide
- `test_*.sh` - Helper scripts for triggering events

## Best Practices Demonstrated

1. **Structured Rulebooks** - Clear event sources, conditions, actions
2. **Logging** - All demos log events for audit trails
3. **Alerting** - Debug messages show what would happen in production
4. **Backup** - Configuration changes are backed up before modification
5. **Validation** - Checks before taking automated actions
6. **Idempotency** - Actions can run multiple times safely

## Notes for Presenters

**Key talking points:**
- Event-Driven Ansible enables reactive automation without manual intervention
- Events come from many sources: webhooks, logs, files, message queues
- Rules evaluate events and trigger actions based on conditions
- Actions can run playbooks, launch job templates, or run modules
- Production deployment uses EDA Controller for centralised management

**Common questions:**
- **Q:** How is this different from scheduled playbooks?
  **A:** Scheduled playbooks run at fixed times; EDA responds to events as they occur

- **Q:** What's the performance impact?
  **A:** Minimal - event sources use push notifications or efficient APIs (no polling)

- **Q:** Can multiple rules match the same event?
  **A:** Yes, all matching rules fire (useful for logging + action patterns)

- **Q:** How do you test rulebooks before production?
  **A:** Use ansible-rulebook command-line tool in dev, then deploy to EDA Controller

## License

These demonstrations are educational materials for Red Hat Ansible Automation Platform training.

Based on patterns from:
- DO274 - Introduction to Event-Driven Ansible
- Red Hat Customer Reference Architectures
- Community best practices
