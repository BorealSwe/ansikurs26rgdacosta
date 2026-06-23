# Woodpecker CI Setup on belfast.zero-effort.net

## Infrastructure

- **Server**: belfast.zero-effort.net (192.168.1.43)
- **External URL**: http://seeker.zero-effort.net:8000
- **Port forwarding**: seeker.zero-effort.net:8000 → 192.168.1.43:8000
- **Containers**: Running as root via sudo podman

## Installed Components

```bash
# Server
sudo podman ps | grep woodpecker-server
# Agent  
sudo podman ps | grep woodpecker-agent
```

## GitLab OAuth Integration

**Application ID**: `677e47cae987768f07a68d7d364e8cd2f3ac168a32ce8a43910161f97162ba86`  
**Redirect URI**: `http://seeker.zero-effort.net:8000/authorize`

## First-Time Setup

1. **Access Woodpecker UI**: http://seeker.zero-effort.net:8000
2. **Sign in with GitLab** (OAuth flow)
3. **Activate the `ansible` repository**
4. **Add secrets** in repository settings:
   - `quay_username`: Your Quay.io username
   - `quay_password`: Your Quay.io password
   - `rh_registry_username`: Red Hat registry username
   - `rh_registry_password`: Red Hat registry password

## Pipeline File

The pipeline is defined in `.woodpecker.yml` at the repository root.

## Managing Woodpecker

### View logs
```bash
ssh rgdacosta@belfast 'sudo podman logs -f woodpecker-server'
ssh rgdacosta@belfast 'sudo podman logs -f woodpecker-agent'
```

### Restart services
```bash
ssh rgdacosta@belfast 'sudo podman restart woodpecker-server woodpecker-agent'
```

### Stop services
```bash
ssh rgdacosta@belfast 'sudo podman stop woodpecker-server woodpecker-agent'
```

### Start services
```bash
ssh rgdacosta@belfast 'sudo podman start woodpecker-server woodpecker-agent'
```

## Data Location

- **Database**: `/var/lib/woodpecker/woodpecker.sqlite`
- **Logs**: `sudo podman logs <container-name>`

## Upgrading

```bash
ssh rgdacosta@belfast 'sudo podman pull docker.io/woodpeckerci/woodpecker-server:v3'
ssh rgdacosta@belfast 'sudo podman pull docker.io/woodpeckerci/woodpecker-agent:v3'
ssh rgdacosta@belfast 'sudo podman restart woodpecker-server woodpecker-agent'
```

## Advantages Over GitLab CI

✅ **Privileged container builds** — ansible-builder can actually build images  
✅ **Runs on your infrastructure** — no shared runner limitations  
✅ **Simpler YAML syntax** — more concise than GitLab CI  
✅ **No vendor lock-in** — self-hosted, GitLab remains the source of truth  
✅ **Full podman support** — native container runtime

## Next Steps

1. Push `.woodpecker.yml` to trigger first build
2. Set up scheduled monitors (daily base image, weekly collection updates)
3. Optionally configure AAP Controller to use the new EE
