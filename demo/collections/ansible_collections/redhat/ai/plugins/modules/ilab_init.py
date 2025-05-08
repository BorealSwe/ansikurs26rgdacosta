#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, XLAB Steampunk <steampunk@xlab.si>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ilab_init

author:
  - Justin Cinkelj (@justinc1)

short_description: Create initial InstructLab configuration

description:
  - Create initial InstructLab configuration.
  - Existing configuration file is not modified if it already exists.
version_added: 1.0.0

options:
  force:
    description:
      - If set to V(true), the configuration file will be re-created.
    type: bool
    default: false
#   path:
#     description:
#       - Path to InstructLab configuration file.
#       - Default is $HOME/.config/instructlab/config.yaml.
#     type: str
#     default: ""  # $HOME/.config/instructlab/config.yaml

notes:
  - Command `ilab` runs in podman container.
  - When started by root, whole /root is mounted as volume.
  - Command  `ilab config init --non-interactive --config /root/asfd.yml`
    fails. This is reason module uses only default configuration file path.
"""

EXAMPLES = r"""
- name: Create initial InstructLab configuration.
  redhat.ai.ilab_init:
"""

RETURN = r""" # """


from ansible.module_utils.basic import AnsibleModule
import os
from ..module_utils import errors


def run(module):
    """
    ilab command runs inside podman container - we cannot check if file is already present there.
    """
    force = module.params["force"]
    # config_file = module.params["path"]
    # Whole $HOME is mounted in ilab container.
    config_file = os.path.join(os.environ["HOME"], ".config/instructlab/config.yaml")
    if os.path.isfile(config_file):
        if not force:
            return False, f"Config file already exists ({config_file}).", ""
    cmd = [
        "ilab",
        "config",
        "init",
        "--non-interactive",
        # "--config", config_file,
    ]
    if module.check_mode:
        return True, "Generating config file (ansible check-mode)", ""
    rc, out, err = module.run_command(cmd)
    if rc != 0:
        raise errors.ILabRunCommandError(
            f"Unexpected output of command 'ilab config init', (rc, stdout, stderr): '{(rc, out, err)}'"
        )
    return True, out, err


def main():
    module_args = dict(
        force=dict(
            type="bool",
            default=False,
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    try:
        changed, out, err = run(module)
        module.exit_json(changed=changed, stdout=out, stderr=err)
    except errors.ILabError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
