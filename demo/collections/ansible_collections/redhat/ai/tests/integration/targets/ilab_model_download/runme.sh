#!/usr/bin/env bash

set -eux

function cleanup {
#    ansible-playbook -i "${INVENTORY_PATH}" cleanup.yml -e "output_dir=${OUTPUT_DIR}" -b "$@"
    ansible-playbook -i playbooks/inventory_ilab.yml -e @../../integration_config.yml playbooks/cleanup.yml "$@"
    unset ANSIBLE_CACHE_PLUGIN
    unset ANSIBLE_CACHE_PLUGIN_CONNECTION
}

trap 'cleanup "$@"' EXIT

ansible-playbook -e @../../integration_config.yml playbooks/create_inventory_and_vars.yml -vvv
echo "------------------------------"
cat playbooks/inventory_ilab.yml
echo "------------------------------"

ansible-playbook -i playbooks/inventory_ilab.yml -e @../../integration_config.yml playbooks/cleanup.yml "$@"
ansible-playbook -i playbooks/inventory_ilab.yml -e @../../integration_config.yml playbooks/prepare.yml "$@"
ansible-playbook -i playbooks/inventory_ilab.yml -e @../../integration_config.yml playbooks/run_main_tests.yml "$@"
