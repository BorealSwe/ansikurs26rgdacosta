# Customer Demo Script: EE Automation Pipeline

**Duration**: 20 minutes  
**Audience**: Platform teams, SREs, Ansible admins  
**Goal**: Demonstrate event-driven EE automation that eliminates manual maintenance toil

---

## Setup (Pre-Demo)

1. Have GitLab project open with this pipeline configured
2. Have Quay.io repository page ready (https://quay.io/repository/rgdacosta/custom-ee)
3. Have one existing collection update PR ready (if available)
4. Have AAP Controller UI open to Projects page (optional)

---

## Demo Flow

### Introduction (2 minutes)

**You say**:

> "Today I'm showing you how we've automated Execution Environment maintenance at scale. The traditional approach has three problems:
> 
> 1. **Reactive CVE response** — you find out about base image vulnerabilities from security scanners AFTER deployment
> 2. **Collection staleness** — tracking updates across 15+ collections manually is tedious and error-prone
> 3. **Build inconsistency** — unpinned dependencies mean today's build differs from yesterday's
>
> This pipeline solves all three by detecting changes upstream and automatically rebuilding with full audit trails."

---

### Part 1: Show the Current State (3 minutes)

#### 1.1 Show Pinned Dependencies

**Navigate to**: `execution_environments/custom-ee/requirements-pinned.yml`

**You say**:

> "First, let's look at our collection dependencies. Notice every collection has an explicit version pinned — this gives us reproducible builds. If I run `ansible-builder build` today or next month with the same commit, I get byte-identical images."

**Point out**:
- Version pinning format: `name` + `version`
- Collection count (14 in the example)

#### 1.2 Show Base Image Digest Tracking

**Navigate to**: `execution_environments/custom-ee/.base-image-digest`

**You say**:

> "Here's how we track the Red Hat base image. This file stores the SHA256 digest — a cryptographic hash of the image contents. When Red Hat publishes a security patch, this digest changes, and our monitor detects it."

**Show**: `git log .base-image-digest` — demonstrate the commit history

**You say**:

> "See these commits? Each one represents an automated detection of a base image update. The pipeline rebuilds within 10 minutes of Red Hat publishing."

---

### Part 2: The Automated Monitors (5 minutes)

#### 2.1 Base Image Monitor

**Navigate to**: GitLab → CI/CD → Schedules

**You say**:

> "We run two scheduled monitors. The first checks Red Hat's registry API daily at 2 AM. Let me show you what it does."

**Navigate to**: `execution_environments/pipeline/monitor-base-image.yml`

**Walk through the playbook** (high-level, don't read every line):

1. "It pulls the current digest from the registry API"
2. "Compares it to our stored digest"
3. "If they differ, it commits the new digest and triggers a build"

**You say**:

> "This is event-driven, not polling. We don't rebuild daily 'just in case' — we only rebuild when there's actual change. That saves CI resources and gives us a clear audit trail."

#### 2.2 Collection Update Bot

**Navigate to**: `execution_environments/pipeline/update-collections.yml`

**You say**:

> "The second monitor runs weekly and checks Ansible Galaxy for collection updates. When it finds updates, it creates a pull request."

**If you have a PR ready**: Show it

**Navigate to**: GitLab → Merge Requests → (show collection update PR)

**You say**:

> "Here's an example. The bot detected that `community.kubernetes` released version 3.3.0, and we're on 3.2.0. It created this PR with:
> 
> - Version bump in requirements-pinned.yml
> - Changelog summary extracted from Galaxy
> - Automated label 'dependencies'
>
> A human reviews this — we don't blindly merge — but the detection and PR creation are fully automated. This used to take 2 hours a month; now it's 10 minutes."

---

### Part 3: The Build Pipeline (6 minutes)

#### 3.1 Trigger a Manual Build

**Navigate to**: GitLab → CI/CD → Pipelines → Run pipeline

**You say**:

> "Let me trigger a build manually to show you the pipeline in action."

**Click**: "Run pipeline" on `main` branch

**While it queues**:

> "In production, this would trigger automatically when:
> - The base image digest changes
> - A collection update PR is merged
> - Someone pushes to the execution_environments directory
>
> But I can also trigger it manually for testing."

#### 3.2 Walk Through Pipeline Stages

**Navigate to**: The running pipeline

**You say**:

> "The pipeline has 5 stages. Let's walk through each."

**Stage 1: Validate** (show it running)

> "First, we validate the EE definition syntax and check that all collections resolve on Galaxy. This catches typos before we waste time building."

**Stage 2: Build** (show it running)

> "Next, ansible-builder generates a multi-stage Containerfile and builds the image. We're using layer caching here — if only collections changed, it reuses the base image layers. That takes a 6-minute build down to 2 minutes."

**Stage 3: Test** (show it running)

> "Once built, we run a smoke test playbook inside the EE to verify:
> - Ansible version is correct
> - All collections are installed
> - Python dependencies work
>
> If this fails, we don't publish — catching issues before they hit AAP."

**Stage 4: Publish** (show it running)

> "After testing passes, we push to Quay.io with two tags:
> - The git commit SHA for immutability
> - ':latest' for convenience
>
> AAP projects configured with ':latest' will pull the new image on their next sync."

**Stage 5: Notify** (manual gate)

> "The final stage is manual — it triggers AAP Controller to sync projects using this EE. We gate this because you might want to test the new EE in dev first before promoting to production."

#### 3.3 Show the Published Image

**Navigate to**: https://quay.io/repository/rgdacosta/custom-ee

**You say**:

> "Here's the result in Quay. Notice the tags:
> - abc1234 (the commit SHA) — immutable, traceable
> - latest — always points to the most recent build
>
> Quay also runs security scanning on every image and flags CVEs. If a vulnerability is detected, it appears here, and we can trigger a rebuild."

---

### Part 4: The Value Proposition (3 minutes)

#### 4.1 Show the Audit Trail

**Navigate to**: GitLab → Repository → Commits → filter by `execution_environments/custom-ee/.base-image-digest`

**You say**:

> "Every EE build has a complete audit trail. If I need to answer 'what base image was in production on March 15th?', I just check this commit history. No spreadsheets, no guessing."

#### 4.2 Cost Analysis

**Show a slide or narrate**:

> "Let's talk ROI. Manual EE maintenance for a team with 3 EEs and 15 collections each:
> 
> - Checking for base image updates: 30 min/week
> - Checking for collection updates: 1 hour/week
> - Building and testing: 1 hour/week
> - **Total: ~2.5 hours/week, or 10 hours/month, or 120 hours/year**
>
> With this pipeline:
> - Base image monitoring: automated
> - Collection update PRs: automated
> - Builds: automated
> - **Human time: 20 minutes/month reviewing PRs**
>
> Savings: **118 hours/year per team**. At $100/hour burdened cost, that's **$11,800/year** in avoided toil.
>
> Plus faster CVE response — we're not waiting for a human to check the registry."

#### 4.3 Demonstrate Reproducibility

**You say**:

> "One more benefit: reproducible builds. If I checkout this commit from last month and run `ansible-builder build`, I get the exact same EE — same collections, same Python packages, same base image digest. That's critical for debugging 'it worked last week' issues."

**Show**: `git checkout <old-commit>` then `cat requirements-pinned.yml` to show the pinned versions from that time

---

### Wrap-Up (1 minute)

**You say**:

> "To summarize, this pipeline gives you:
> 
> 1. **Proactive CVE response** — rebuilds within 10 minutes of Red Hat publishing a patch
> 2. **Automated collection maintenance** — PRs for updates, not spreadsheet tracking
> 3. **Reproducible builds** — pinned versions + digest tracking
> 4. **Full audit trail** — git log shows every build trigger
> 5. **~120 hours/year** time savings per team
>
> It runs on GitLab CI free tier, uses open-source tools (ansible-builder, podman), and works with any registry (Quay, ACR, ECR, Artifactory).
>
> Questions?"

---

## Common Questions & Answers

### Q: "What if a collection is removed from Galaxy?"

**A**: "The build would fail at the validate stage — ansible-builder can't resolve the collection. You'd get a GitLab pipeline failure notification, update `requirements-pinned.yml` to remove or replace the collection, and re-trigger the build. The failure happens in CI, not production."

### Q: "How do we roll back if a new EE breaks something?"

**A**: "Two ways:
1. In AAP Controller, change the project to use the previous EE tag (e.g., switch from `:latest` to `:abc1234`)
2. Or revert the git commit that triggered the build, and the pipeline will rebuild the old version

We keep the last 5 EE images in Quay for fast rollback."

### Q: "Can this work with Tekton instead of GitLab CI?"

**A**: "Yes. The three playbooks (`monitor-base-image.yml`, `update-collections.yml`, `build-ee.yml`) are CI-agnostic — they're just Ansible playbooks. You'd rewrite `.gitlab-ci.yml` as Tekton Tasks and Pipelines, but the playbooks themselves are reusable."

### Q: "What about air-gapped environments?"

**A**: "You'd run the monitors inside the air gap, pointed at your internal mirror of Red Hat's registry and a private Ansible Galaxy instance. The pipeline logic is the same; you're just changing the API endpoints."

### Q: "How do we test a new EE before promoting to production?"

**A**: "The manual gate on the `publish:notify-aap` stage is for exactly that. After the build, you can:
1. Manually run a test playbook using the new EE tag
2. Point a dev AAP instance at the new EE
3. Once validated, approve the notify stage to sync production projects"

### Q: "Can we customize the smoke test?"

**A**: "Absolutely. The smoke test playbook in `build-ee.yml` is just a starting point — you'd add tasks that exercise the collections you care about. For example, if you're building a network EE, run a playbook that hits `cisco.ios` modules against a test device."

---

## Demo Environment Setup (For Presenters)

### Prerequisites

1. GitLab account (free tier works)
2. Quay.io account (free tier works)
3. Red Hat Customer Portal account (for registry access)
4. This repository cloned locally

### One-Time Setup

1. Create a Quay.io repository named `custom-ee` (public or private)
2. Generate a Quay.io CLI password (robot account or personal)
3. Add GitLab CI variables (see QUICKSTART.md Step 1)
4. Copy `.gitlab-ci.yml` to repo root
5. Initialize base image digest (see QUICKSTART.md Step 3)
6. Commit and push

### Before the Demo

1. Test the pipeline manually to ensure it works
2. Optionally: manually create a collection update PR by running `update-collections.yml` locally and force-bumping a version
3. Rehearse the flow — know where to click

### During the Demo

- **Don't**: Wait for a 6-minute build to complete live — show a pre-recorded video or a screenshot of a completed pipeline
- **Do**: Trigger the build to show the "Run pipeline" flow, but don't sit in silence waiting
- **Do**: Have terminal windows pre-positioned with useful commands (`git log`, `podman images`, etc.)

---

## Presentation Slide Deck (Optional)

If presenting to executives or non-technical stakeholders, use these slides:

1. **Problem Statement**: Manual EE toil (3 pain points)
2. **Solution Overview**: Event-driven automation architecture diagram
3. **Demo**: Live walkthrough (this script)
4. **ROI**: Time savings + faster CVE response
5. **Roadmap**: Next steps (multi-EE, semantic versioning, etc.)
