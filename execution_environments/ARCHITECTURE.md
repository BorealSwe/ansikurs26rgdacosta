# EE Automation Architecture

## High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                      TRIGGER SOURCES                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Red Hat      │  │ Ansible      │  │ Developer    │             │
│  │ publishes    │  │ Galaxy       │  │ pushes to    │             │
│  │ base image   │  │ releases     │  │ main branch  │             │
│  │ update       │  │ collection   │  │              │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
│         │                  │                  │                      │
│         │                  │                  │                      │
└─────────┼──────────────────┼──────────────────┼──────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     DETECTION LAYER                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────┐  ┌──────────────────────────┐        │
│  │  Base Image Monitor      │  │  Collection Update Bot   │        │
│  │  (Cron: daily 2am)       │  │  (Cron: Sat 3am)        │        │
│  │                          │  │                          │        │
│  │  • Query registry API    │  │  • Query Galaxy API     │        │
│  │  • Compare SHA digest    │  │  • Compare versions     │        │
│  │  • Detect changes        │  │  • Create PR if updates │        │
│  └─────────┬────────────────┘  └─────────┬────────────────┘        │
│            │                              │                          │
│            └──────────┬───────────────────┘                          │
│                       │                                              │
└───────────────────────┼──────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     BUILD PIPELINE                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Stage 1: VALIDATE                                                  │
│  ┌────────────────────────────────────────────────────┐            │
│  │ • Lint execution-environment.yml                   │            │
│  │ • Verify requirements-pinned.yml syntax            │            │
│  │ • Check collection name resolution                 │            │
│  └────────────────────────────────────────────────────┘            │
│                        │                                             │
│                        ▼                                             │
│  Stage 2: BUILD                                                     │
│  ┌────────────────────────────────────────────────────┐            │
│  │ • ansible-builder build                            │            │
│  │ • Layer caching for speed                          │            │
│  │ • Tag: commit-SHA + :latest                        │            │
│  └────────────────────────────────────────────────────┘            │
│                        │                                             │
│                        ▼                                             │
│  Stage 3: TEST                                                      │
│  ┌────────────────────────────────────────────────────┐            │
│  │ • Run smoke test playbook inside EE                │            │
│  │ • Verify ansible version                           │            │
│  │ • Check collection inventory                       │            │
│  │ • Validate Python dependencies                     │            │
│  └────────────────────────────────────────────────────┘            │
│                        │                                             │
│                        ▼                                             │
│  Stage 4: PUBLISH                                                   │
│  ┌────────────────────────────────────────────────────┐            │
│  │ • Push to Quay.io (or ACR/ECR)                     │            │
│  │ • Tag :commit-SHA for immutability                 │            │
│  │ • Update :latest for convenience                   │            │
│  └────────────────────────────────────────────────────┘            │
│                        │                                             │
│                        ▼                                             │
│  Stage 5: NOTIFY                                                    │
│  ┌────────────────────────────────────────────────────┐            │
│  │ • POST to AAP Controller API                       │            │
│  │ • Trigger project sync (manual gate)               │            │
│  │ • Webhook to Slack (optional)                      │            │
│  └────────────────────────────────────────────────────┘            │
│                                                                      │
└───────────────────────┬──────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     DEPLOYMENT                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────┐  ┌──────────────────────────┐        │
│  │  Quay.io Registry        │  │  AAP Controller          │        │
│  │                          │  │                          │        │
│  │  custom-ee:abc123       │  │  Projects pull new EE    │        │
│  │  custom-ee:latest       │  │  on next sync            │        │
│  └──────────────────────────┘  └──────────────────────────┘        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### Base Image Monitor

**Input**: Red Hat registry API  
**Output**: Git commit if digest changed → pipeline trigger  
**Frequency**: Daily (cron)  
**Duration**: ~30 seconds  

**Logic**:
```python
current_digest = podman_inspect(base_image).digest
stored_digest = read_file('.base-image-digest')

if current_digest != stored_digest:
    write_file('.base-image-digest', current_digest)
    git_commit_and_push()
    trigger_pipeline()
```

### Collection Update Bot

**Input**: Ansible Galaxy API  
**Output**: Pull request with version updates  
**Frequency**: Weekly (cron)  
**Duration**: ~2 minutes  

**Logic**:
```python
for collection in requirements:
    latest_version = galaxy_api.get_latest(collection.name)
    if latest_version > collection.version:
        updates.append({
            'name': collection.name,
            'from': collection.version,
            'to': latest_version
        })

if updates:
    create_pr(updates)
```

### Build Pipeline

**Input**: Git push or trigger  
**Output**: Tagged EE image in registry  
**Frequency**: Event-driven  
**Duration**: ~6-8 minutes  

**Stages**:
1. **Validate** (30s): Syntax checks, no heavy lifting
2. **Build** (4-5min): Multi-stage Dockerfile build with layer caching
3. **Test** (1min): Smoke test playbook run
4. **Publish** (1min): Registry push
5. **Notify** (manual): Optional AAP sync trigger

## Data Flow

### Base Image Update Scenario

```
Day 0:
  Red Hat: Publishes ee-supported-rhel9 with RHEL 9.6 security patch
  Digest: sha256:abc123... → sha256:def456...

Day 1, 2:00 AM:
  Monitor: Cron triggers monitor-base-image.yml
  Monitor: Queries registry API
  Monitor: Detects digest mismatch
  Monitor: Commits new digest to .base-image-digest
  Monitor: Pushes to main branch
  GitLab: Detects push → triggers build pipeline

Day 1, 2:08 AM:
  Pipeline: Validate + Build + Test stages pass
  Pipeline: Publishes custom-ee:abc123 to Quay

Day 1, 8:00 AM:
  SRE: Reviews GitLab pipeline logs
  SRE: Approves publish:notify-aap stage
  AAP: Syncs projects using custom-ee
  AAP: Pulls custom-ee:latest from Quay
  Result: Production workloads now run on patched base image
```

### Collection Update Scenario

```
Week 1, Saturday 3:00 AM:
  Bot: Cron triggers update-collections.yml
  Bot: Queries Galaxy API for 14 collections
  Bot: Detects community.kubernetes 3.2.0 → 3.3.0
  Bot: Creates PR with version bump + changelog
  Bot: Labels PR "dependencies,automated"

Week 1, Monday:
  SRE: Reviews PR changelog
  SRE: Checks for breaking changes
  SRE: Merges PR
  GitLab: Detects merge to main → triggers build pipeline
  Pipeline: Builds EE with updated collection

Week 1, Monday 10 minutes later:
  Pipeline: Publishes custom-ee:def789 to Quay
  AAP: Projects pull updated EE on next sync
```

## Security Model

### Credential Flow

```
GitLab CI Variables (encrypted at rest)
    │
    ├─> QUAY_PASSWORD ──────> podman login quay.io
    ├─> RH_REGISTRY_PASSWORD > podman login registry.redhat.io
    └─> AAP_CONTROLLER_PASS -> curl AAP API

No credentials in:
  - Git repository
  - Build logs (masked)
  - EE image layers
```

### Image Provenance

Every EE image is traceable:

- **Git commit SHA**: Which code built this image
- **Build timestamp**: When it was built
- **Base image digest**: Exact base layer used
- **Collection versions**: Pinned in requirements-pinned.yml

Example tag: `custom-ee:abc1234` → Git log shows:
- Requirements file at that commit
- Base image digest at that commit
- CI pipeline logs for that build

## Scalability

### Multiple EEs

To manage multiple EEs (e.g., `network-ee`, `cloud-ee`, `linux-ee`):

```
execution_environments/
├── network-ee/
│   ├── execution-environment.yml
│   ├── requirements-pinned.yml
│   └── .base-image-digest
├── cloud-ee/
│   ├── execution-environment.yml
│   ├── requirements-pinned.yml
│   └── .base-image-digest
└── pipeline/
    ├── monitor-base-image.yml      # Loop over EE dirs
    ├── update-collections.yml       # Loop over EE dirs
    └── build-ee.yml                 # Parameterize EE name
```

Modify `.gitlab-ci.yml` workflow rules to trigger builds per directory:

```yaml
workflow:
  rules:
    - changes:
        - execution_environments/network-ee/**/*
      variables:
        EE_DIR: execution_environments/network-ee
        EE_NAME: network-ee
```

### Multi-Registry Publishing

To publish to multiple registries (Quay + ACR + ECR):

```yaml
publish:quay:
  script:
    - podman push quay.io/$QUAY_ORG/custom-ee:$CI_COMMIT_SHORT_SHA

publish:acr:
  script:
    - podman push $ACR_REGISTRY/custom-ee:$CI_COMMIT_SHORT_SHA

publish:ecr:
  script:
    - podman push $ECR_REGISTRY/custom-ee:$CI_COMMIT_SHORT_SHA
```

Run in parallel for faster publishing.

## Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| Monitor cron misses run | Delayed detection (24h) | Next cron catches it |
| Build fails | Latest EE unchanged | Fix code → manual trigger |
| Registry unreachable | Publish fails | Retry via manual pipeline |
| AAP API down | Notification fails | Manual sync in AAP UI |
| Collection removed from Galaxy | Build fails | Update requirements to remove it |

**No single point of failure**: Every automated component has a manual override path.

## Observability

### Metrics to Track

- **Base image updates/month**: Trend shows Red Hat release cadence
- **Collection updates/month**: Trend shows ecosystem activity
- **Build success rate**: Should be >95%
- **Build duration**: Baseline ~6min, spike indicates performance regression
- **EE image size**: Track bloat over time

### Alerting

Set up GitLab notifications for:
- Pipeline failures (build stage)
- Scheduled job failures (monitors)
- Collection update PRs created

Slack webhook example in `.gitlab-ci.yml`:

```yaml
after_script:
  - |
    if [ "$CI_JOB_STATUS" == "failed" ]; then
      curl -X POST $SLACK_WEBHOOK_URL -d "{'text': 'EE build failed: $CI_PIPELINE_URL'}"
    fi
```

## Cost Optimization

### Layer Caching

`BUILDAH_LAYERS=true` enables layer caching — subsequent builds reuse unchanged layers.

Example timings:
- **Cold build** (no cache): 6m 30s
- **Warm build** (collection change only): 2m 15s

Savings: ~65% faster incremental builds.

### Artifact Cleanup

GitLab retains artifacts by default. Configure retention in `.gitlab-ci.yml`:

```yaml
artifacts:
  expire_in: 1 day  # Delete after 24h
```

EE images in Quay: Enable auto-pruning to keep last 5 tags only.

## References

- [ansible-builder docs](https://ansible.readthedocs.io/projects/builder/)
- [Execution Environments (AAP 2.5)](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/creating_and_consuming_execution_environments/index)
- [GitLab CI Best Practices](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html)
- [Quay.io Security Scanning](https://docs.quay.io/guides/security-scanning.html)
