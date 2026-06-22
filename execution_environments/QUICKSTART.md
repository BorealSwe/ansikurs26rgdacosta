# EE Automation Quick Start

Get the automated EE pipeline running in 15 minutes.

## Prerequisites

- GitLab repository with CI/CD enabled
- Quay.io account (free tier works)
- Red Hat Customer Portal account
- Local: `ansible-builder`, `podman`, `ansible-core`

## Step 1: Configure GitLab CI Variables

In GitLab → Settings → CI/CD → Variables, add:

| Variable | Value | Protected | Masked |
|----------|-------|-----------|--------|
| `QUAY_USERNAME` | Your Quay.io username | ✓ | ✗ |
| `QUAY_PASSWORD` | Your Quay.io token | ✓ | ✓ |
| `QUAY_ORG` | Your Quay.io org (default: username) | ✗ | ✗ |
| `RH_REGISTRY_USERNAME` | Red Hat portal username | ✓ | ✗ |
| `RH_REGISTRY_PASSWORD` | Red Hat portal password | ✓ | ✓ |
| `GITLAB_TRIGGER_URL` | (Optional) Pipeline trigger URL | ✓ | ✗ |
| `GITLAB_TRIGGER_TOKEN` | (Optional) Pipeline trigger token | ✓ | ✓ |
| `GITHUB_TOKEN` | (Optional) For collection update PRs | ✓ | ✓ |
| `AAP_CONTROLLER_URL` | (Optional) AAP instance URL | ✗ | ✗ |
| `AAP_CONTROLLER_USER` | (Optional) AAP admin user | ✓ | ✗ |
| `AAP_CONTROLLER_PASS` | (Optional) AAP admin password | ✓ | ✓ |

**Get Quay.io token**: Quay.io → Account Settings → CLI Password → Generate Encrypted Password

**Get GitLab trigger**: GitLab → Settings → CI/CD → Pipeline triggers → Add trigger

## Step 2: Copy GitLab CI Config

```bash
cp execution_environments/pipeline/.gitlab-ci.yml .gitlab-ci.yml
git add .gitlab-ci.yml
git commit -m "Add EE automation pipeline"
git push
```

## Step 3: Initialize Base Image Digest

```bash
# Pull the base image
podman pull registry.redhat.io/ansible-automation-platform-25/ee-supported-rhel9:latest

# Store its digest
podman inspect registry.redhat.io/ansible-automation-platform-25/ee-supported-rhel9:latest \
  --format '{{ .Digest }}' \
  > execution_environments/custom-ee/.base-image-digest

# Commit
git add execution_environments/custom-ee/.base-image-digest
git commit -m "Initialize base image digest"
git push
```

## Step 4: Test Manual Build

Trigger a manual build in GitLab UI:

1. GitLab → CI/CD → Pipelines → Run pipeline
2. Select branch: `main`
3. Click "Run pipeline"

Expected result: 5-stage pipeline (validate → build → test → publish → monitor) completes in ~8 minutes.

## Step 5: Configure Scheduled Monitors

### Daily Base Image Monitor

GitLab → CI/CD → Schedules → New schedule

- Description: `Daily base image monitor`
- Interval pattern: `0 2 * * *` (2am daily)
- Target branch: `main`
- Variables:
  - `SCHEDULE_TYPE` = `base-image-monitor`

### Weekly Collection Updates

GitLab → CI/CD → Schedules → New schedule

- Description: `Weekly collection updates`
- Interval pattern: `0 3 * * 6` (3am Saturday)
- Target branch: `main`
- Variables:
  - `SCHEDULE_TYPE` = `collection-updates`

## Step 6: Verify the Pipeline

### Test base image monitor locally

```bash
cd execution_environments/pipeline
ansible-playbook monitor-base-image.yml
```

Expected: "Base image unchanged" (unless Red Hat just published an update).

### Test collection updates locally

```bash
ansible-playbook update-collections.yml
```

Expected: Either "No updates required" or a PR is created with collection version bumps.

### Test build locally

```bash
cd execution_environments/custom-ee
ansible-builder build -t quay.io/rgdacosta/custom-ee:test -v3
podman run --rm quay.io/rgdacosta/custom-ee:test ansible --version
```

Expected: Build succeeds, ansible version displays.

## Step 7: Configure AAP Controller (Optional)

If you want AAP to auto-sync projects when a new EE is published:

1. Add the AAP variables to GitLab (see Step 1)
2. In GitLab pipeline, manually trigger the `publish:notify-aap` stage after a successful build
3. AAP projects configured with your EE will sync and pull the new image

## Workflow Summary

### Automated (no human intervention)

1. **Red Hat publishes base image update**
   - Monitor detects digest change (2am daily check)
   - Commits new digest → triggers build pipeline
   - New EE published to Quay within 10 minutes

2. **Collection maintainer releases new version**
   - Bot checks Galaxy API (3am Saturday)
   - Creates PR with version bumps + changelog
   - You review + merge → build pipeline runs
   - New EE published to Quay

### Manual

1. **You push code to `execution_environments/custom-ee/`**
   - Pipeline auto-runs on push to main
   - New EE built and published

2. **You trigger manual build**
   - GitLab UI → Run pipeline
   - Useful for testing changes

## Troubleshooting

### Build fails: "Failed to pull base image"

**Cause**: Red Hat registry credentials invalid or expired.

**Fix**: Regenerate credentials at https://access.redhat.com/terms-based-registry/ and update `RH_REGISTRY_USERNAME` / `RH_REGISTRY_PASSWORD` in GitLab.

### Build fails: "Collection X not found"

**Cause**: Collection was removed from Galaxy or namespace changed.

**Fix**: Update `requirements-pinned.yml` to remove the collection or use the new namespace.

### Monitor playbook fails: "podman: command not found"

**Cause**: Monitor runs in a CI container without podman.

**Fix**: The `.gitlab-ci.yml` uses `registry.access.redhat.com/ubi9/ubi:latest` which includes podman. If running locally, install podman.

### Collections bot creates empty PR

**Cause**: All collections are already at latest versions.

**Fix**: This is expected. The bot will skip PR creation when no updates are available.

## Cost Estimate

| Component | CI minutes/month | Estimated cost (GitLab SaaS) |
|-----------|------------------|------------------------------|
| Daily base monitor (30 runs) | ~15 min | $0 (free tier) |
| Weekly collection bot (4 runs) | ~8 min | $0 (free tier) |
| Event-driven builds (~4/month) | ~32 min | $0 (free tier) |
| **Total** | **~55 min/month** | **$0** |

GitLab free tier includes 400 CI minutes/month — this pipeline uses ~14% of that.

## Next Steps

- **Pin Python packages**: Add versions to `requirements.txt` for full reproducibility
- **Add smoke tests**: Expand `build-ee.yml` test stage with playbook runs
- **Multi-arch builds**: Build for `amd64` and `arm64` if deploying to Apple Silicon
- **Semantic versioning**: Tag EEs with semver instead of commit SHA
- **Rollback procedure**: Keep 5 recent EE images in Quay for fast rollback

## Demo for Customers

To demonstrate this to a customer:

1. **Show the current state**: `git log execution_environments/custom-ee/.base-image-digest` — shows automated digest updates
2. **Trigger a build**: GitLab UI → Run pipeline → show the 5 stages completing
3. **Show Quay.io**: Display the published image with build tag + `:latest`
4. **Show a collection PR**: If one exists, walk through the changelog and merge → auto-rebuild
5. **Show GitLab schedules**: Demonstrate the cron configuration for monitors

**Key talking points**:
- Zero manual toil for CVE response
- Reproducible builds via pinned versions
- Audit trail via git commits
- Event-driven (not wasteful scheduled rebuilds)

**ROI pitch**: "Manual EE maintenance: 3-4 hours/month. Automated: 10 minutes/month reviewing PRs. That's 35 hours/year saved per team."
