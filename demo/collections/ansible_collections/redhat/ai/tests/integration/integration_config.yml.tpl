---
registry_username: $REGISTRY_USERNAME
registry_password: $REGISTRY_PASSWORD
ilab_user: $ILAB_USER
ilab_host: $ILAB_HOST
ilab_ssh_private_key_filename: id_rsa_redhat_ai_aws
ilab_ssh_private_key_content: |
$ILAB_SSH_PRIVATE_KEY___MULTILINE_YAML
ansible_ssh_extra_args: -o StrictHostKeyChecking=no -o ServerAliveInterval=60
ansible_python_interpreter: /usr/bin/python3
model_name: granite-8b-starter-v1
