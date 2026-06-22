# Execution Environment Automation Pipeline

Automated build pipeline for Ansible Execution Environments with base image tracking and collection maintenance.

## Problem Statement

Manual EE maintenance has three challenges:

1. **Base image drift** — Red Hat updates `ee-supported-rhel9:latest` to address CVEs, but you don't know when
2. **Collection staleness** — Ansible collections release updates, but tracking 15+ collections manually is tedious
3. **Build reproducibility** — Unpinned dependencies mean builds aren't deterministic across time

## Solution

A three-tier automation pipeline:

| Tier | Component | Trigger | Output |
|------|-----------|---------|--------|
| 1 | Base image monitor | Cron (daily) | SHA digest change detection → trigger build |
| 2 | Collection update bot | Cron (weekly) | PR with pinned collection updates |
| 3 | EE build pipeline | Git push / manual | Built & tagged EE image in Quay/ACR |

## Directory Structure

```
execution_environments/
├── custom-ee/
│   ├── execution-environment.yml    # EE definition (base image, deps)
│   ├── requirements.yml              # Collection dependencies (pinned versions)
│   ├── requirements.txt              # Python dependencies (pinned versions)
│   └── context/                      # Build context (custom scripts, configs)
├── pipeline/
│   ├── monitor-base-image.yml        # Cron job: check for base image updates
│   ├── update-collections.yml        # Bot: generate collection update PR
│   ├── build-ee.yml                  # CI/CD: build EE with ansible-builder
│   └── .gitlab-ci.yml                # GitLab CI pipeline definition
└── README.md                         # This file
```

## Component Details

### 1. Base Image Monitor (`monitor-base-image.yml`)

**Purpose**: Detect when Red Hat publishes an updated base image digest.

**How it works**:
- Runs daily via cron or CI schedule
- Queries `registry.redhat.io` for the current SHA256 digest of `ee-supported-rhel9:latest`
- Compares against stored digest in `.base-image-digest`
- If changed: commits new digest + triggers EE rebuild

**Why SHA digests**: `latest` tag is mutable — the same tag can point to different images over time. Digests are immutable and content-addressed.

### 2. Collection Update Bot (`update-collections.yml`)

**Purpose**: Keep collection versions current without manual tracking.

**How it works**:
- Runs weekly via cron
- Queries `galaxy.ansible.com` API for latest stable version of each collection in `requirements.yml`
- Compares against pinned versions
- If updates available: creates PR with version bumps + changelog summary

**Version pinning format**:
```yaml
collections:
  - name: community.kubernetes
    version: "3.2.1"  # Pinned — reproducible builds
```

### 3. EE Build Pipeline (`build-ee.yml` + `.gitlab-ci.yml`)

**Purpose**: Build, test, and publish EE images on demand or automatically.

**Trigger conditions**:
- Manual trigger (GitLab UI / API)
- Push to `main` branch with changes in `execution_environments/custom-ee/`
- Base image digest change (via monitor)
- Approved collection update PR merge

**Build stages**:
1. **Validate** — lint `execution-environment.yml`, check collection resolution
2. **Build** — `ansible-builder build` with layer caching
3. **Test** — run smoke test playbook inside the EE
4. **Tag** — semantic version + build date (e.g., `v1.2.3-20260619`)
5. **Push** — publish to Quay.io or Azure Container Registry
6. **Notify** — webhook to Slack/AAP Controller to refresh EE in projects

## Usage

### Initial Setup

1. Pin your collection versions:
```bash
cd execution_environments/custom-ee
# Generates requirements.yml with current latest versions pinned
ansible-galaxy collection list --format yaml > requirements.yml.new
```

2. Store the current base image digest:
```bash
podman inspect registry.redhat.io/ansible-automation-platform-25/ee-supported-rhel9:latest \
  --format '{{ .Digest }}' > .base-image-digest
```

3. Configure CI variables in GitLab:
```
QUAY_USERNAME=<your-quay-user>
QUAY_PASSWORD=<your-quay-token>
RH_REGISTRY_USERNAME=<your-rh-portal-user>
RH_REGISTRY_PASSWORD=<your-rh-portal-password>
```

### Manual Build

```bash
cd execution_environments/custom-ee
ansible-builder build -t quay.io/rgdacosta/custom-ee:latest -v3
podman push quay.io/rgdacosta/custom-ee:latest
```

### Automated Build (via GitLab CI)

Push to `main` or manually trigger in GitLab UI.

### Collection Updates

The bot creates a PR weekly if updates are available. Review the changelog, approve, and merge — the pipeline auto-rebuilds on merge.

## Best Practices

1. **Pin everything** — collections, python packages, ansible-core version
2. **Layer caching** — use `BUILDAH_LAYERS=true` to speed up incremental builds
3. **Multi-stage testing** — validate EE before pushing (run a test playbook)
4. **Semantic versioning** — tag EEs with semver (e.g., `v1.2.3`) for rollback capability
5. **Keep base image current** — automated monitor prevents CVE drift

## Rollback Strategy

If a new EE breaks production:

```bash
# In AAP Controller, revert project EE to previous version
# Or update the project to use a pinned tag instead of :latest
```

Keep 3-5 recent EE images in the registry for fast rollback.

## Maintenance

- **Monthly**: Review collection update PRs and test new versions
- **Quarterly**: Bump ansible-core version and test against your playbooks
- **On CVE alerts**: Manually trigger base image monitor + rebuild

## Example: Complete Workflow

1. **Week 1**: Red Hat publishes `ee-supported-rhel9` with RHEL 9.6 (CVE fixes)
2. **Day 1 (morning)**: Base image monitor detects new digest → commits → triggers build
3. **Day 1 (afternoon)**: Build pipeline produces `v1.2.4-20260619` → pushes to Quay
4. **Day 2**: AAP Controller pulls new EE for projects configured with `:latest`

5. **Week 2**: `community.kubernetes` releases 3.3.0 with new k8s_info filters
6. **Week 2 (Saturday)**: Collection bot creates PR with version bump + changelog
7. **Week 2 (Monday)**: You review, approve, merge
8. **Week 2 (Monday)**: Pipeline rebuilds → `v1.2.5-20260626`

Zero manual intervention for the CVE fix. One merge click for the collection update.

## Technical Deep Dive

### Why ansible-builder?

`ansible-builder` is Red Hat's official tool for creating EEs. It:
- Handles multi-stage Dockerfiles (builder + runtime layers)
- Manages Python/system dependencies automatically
- Integrates with ansible-navigator for local testing
- Produces OCI-compliant images for any registry

### Why not use Ansible Galaxy's dependency resolution?

`requirements.yml` without versions uses Galaxy's "latest stable" at build time. Two builds days apart can produce different images. Pinning versions makes builds **deterministic** and **auditable**.

### Why monitor the digest and not just rebuild on a schedule?

Rebuilding daily wastes CI resources 364 days a year. The digest monitor is a 5-second API call that only triggers heavy builds when there's actual change.

## Cost Analysis

| Approach | Manual effort/month | CI minutes/month | Build consistency |
|----------|---------------------|------------------|-------------------|
| Manual | 2-4 hours | 0 | Low (human error) |
| Scheduled rebuild (daily) | 0 | ~900 | Medium (untargeted) |
| Event-driven (this solution) | 10 min (PR reviews) | ~60 | High (targeted) |

**Savings**: ~3.5 hours/month of manual toil + faster response to CVEs.
