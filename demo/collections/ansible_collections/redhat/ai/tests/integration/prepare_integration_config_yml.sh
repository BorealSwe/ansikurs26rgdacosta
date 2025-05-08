# shellcheck shell=bash

# shellcheck disable=SC2001
ILAB_SSH_PRIVATE_KEY___MULTILINE_YAML="$(echo "$ILAB_SSH_PRIVATE_KEY" | sed 's/^/  /')"
export ILAB_SSH_PRIVATE_KEY___MULTILINE_YAML

envsubst <tests/integration/integration_config.yml.tpl >tests/integration/integration_config.yml
echo "------------------------------"
sed <tests/integration/integration_config.yml '/BEGIN OPENSSH PRIVATE KEY/,/END OPENSSH PRIVATE KEY/d'
echo "------------------------------"
