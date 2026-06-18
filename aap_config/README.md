# AAP Controller Organization Export/Import

Export and import a complete AAP Controller organization configuration, including all resources needed for students to replicate an instructor's demo environment.

## What gets exported

| Resource | File |
|----------|------|
| Organization | `export/<org>/organization.yml` |
| Credentials | `export/<org>/credentials/all.yml` |
| Inventories, hosts, groups | `export/<org>/inventories/` |
| Projects | `export/<org>/projects/all.yml` |
| Job templates | `export/<org>/job_templates/all.yml` |
| Job template surveys | `export/<org>/job_templates/surveys.yml` |
| Workflow templates + nodes | `export/<org>/workflow_templates/all.yml` |
| Workflow template surveys | `export/<org>/workflow_templates/surveys.yml` |
| Notification templates | `export/<org>/notification_templates/all.yml` |
| Notification associations | `export/<org>/notification_templates/associations.yml` |
| Schedules | `export/<org>/schedules/all.yml` |
| Users (non-admin) | `export/<org>/users/all.yml` |
| Teams + members | `export/<org>/teams/all.yml` |
| Org role assignments | `export/<org>/roles/all.yml` |

## Prerequisites

- Ansible 2.15+ on the control node
- Admin credentials for the AAP Controller instance
- SSH private key at `~/.ssh/lab_rsa` (used to inject functional machine credentials)

## Configuration

Edit `host_vars/localhost/vars.yml`:

```yaml
controller_host: "https://aap.lab.example.com"
controller_user: "admin"
controller_pass: "redhat"
controller_verify_tls: false
org_name: "Linux"                # Source organization to export
import_org_name: "Linux-Test"    # Target organization for import
ssh_key_file: "~/.ssh/lab_rsa"   # SSH key injected into machine credentials
```

## Usage

### Export

```bash
ansible-playbook aap_config/export_org.yml
```

Exports the organization specified by `org_name` to `aap_config/export/<org>/`.

### Import

```bash
ansible-playbook aap_config/import_org.yml
```

Imports into the organization specified by `import_org_name`. To import into a different org, override at runtime:

```bash
ansible-playbook aap_config/import_org.yml -e import_org_name="My-Org"
```

All imported users are created with password `redhat`.

### Cleanup

Delete the target organization in the AAP UI or via API. This cascade-deletes all child resources (credentials, inventories, templates, etc.):

```bash
# Find the org ID
curl -sk -u admin:redhat \
  "https://aap.lab.example.com/api/controller/v2/organizations/?name=Linux-Test" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['results'][0]['id'])"

# Delete it
curl -sk -u admin:redhat -X DELETE \
  "https://aap.lab.example.com/api/controller/v2/organizations/<ID>/"
```

## Notes

- Credential secrets (passwords, SSH keys) are stored as `$encrypted$` in the export. The import playbook injects the SSH key from `ssh_key_file` and filters out encrypted placeholders.
- The import playbook accepts `status_code: [201, 400]` for user creation, so re-runs are safe when users already exist globally.
- Workflow node topology (success/failure/always edges) and approval nodes are fully preserved.
- Notification associations cover all four types: started, success, error, and approval.
