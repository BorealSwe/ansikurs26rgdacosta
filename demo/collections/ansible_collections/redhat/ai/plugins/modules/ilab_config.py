#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, XLAB Steampunk <steampunk@xlab.si>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ilab_config

author:
  - Justin Cinkelj (@justinc1)

short_description: Edit existing InstructLab configuration

description:
  - Edit existing InstructLab configuration.
  - Additional python libraries are required on InstructLab VM.
    To install them use `pip install -r requirements.txt` or equivalent.
  - Module removes comments from the configuration file.
    On first invocation, "<original_filename>.commented" file is created.
    Use it if you need to consult comments to explain configuration options.
  - Module changes only selected parts of the configuration file.
    Currently only `serve` section in the configuration file is modified.
    Other section will be configured in a future release.
  - If additional parts of configuration file need to be modified,
    a whole configuration file can be provided.
version_added: 1.0.0

notes:
  - We assume configuration file is at $HOME/.config/instructlab/config.yaml

options:
  config_file:
    description:
      - Path to configuration file to be used.
      - File must already exists on managed node.
      - If set, all other parameters are ignored.
    type: str
    default: ""
  model_path:
    description:
      - Path to model to be served by model service.
    type: str
  host_port:
    description:
      - Host address and port the model service should listen on.
    type: str
    default: 0.0.0.0:8000
  token:
    description:
      - Authorization token required to access the model service.
    type: str
  backend:
    description:
      - The model backend used by model service.
    type: str
    default: vllm
    choices:
      - vllm
      - llama-cpp
  gpu_count:
    description:
      - Number of GPUs to use.
    type: int
    default: 1
"""

EXAMPLES = r"""
- name: Configure InstructLab - replace complete config file
  redhat.ai.ilab_config:
    config_file: "{{ ansible_env.HOME }}/.config/instructlab/config.yaml.example"

- name: Configure InstructLab - change selected setting only
  redhat.ai.ilab_config:
    host_port: "0.0.0.0:8000"
    token: "demo-token"
    backend: vllm
    model_path: "{{ ansible_env.HOME }}/.cache/instructlab/models/granite-8b-starter-v1"
    gpu_count: 4
"""

RETURN = r"""
config_file:
  description: Path to InstructLab configuration file.
  returned: success
  type: str
  sample: "/var/home/ec2-user/.config/instructlab/config.yaml"
diff:
  description: Difference between previous configuration and new configuration.
  returned: always
  type: dict
  sample: {}
"""


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.common.dict_transformations import recursive_diff
import os
import shutil
import copy
from ..module_utils import errors

try:
    import yaml
except ImportError as imp_exc:
    YAML_IMPORT_ERROR = imp_exc
else:
    YAML_IMPORT_ERROR = None

_ilab_config_file = os.path.join(os.environ["HOME"], ".config/instructlab/config.yaml")

if YAML_IMPORT_ERROR is None:
    # this section is inside "if" only to make "ansible-test sanity" happy

    class MyDumper(yaml.Dumper):
        # fixes indent for lists
        def increase_indent(self, flow=False, indentless=False):
            return super(MyDumper, self).increase_indent(flow, False)

    def represent_none(self, data):
        # "key:" can be represented as "key:" or as "key: null"
        # "ilab config init" produces "key:", we want to keep this.
        return self.represent_scalar("tag:yaml.org,2002:null", "")

    yaml.add_representer(type(None), represent_none)


def run_high_level(module):
    """
    ilab command runs inside podman container - we cannot check if file is already present there.
    """

    def update_param(key, changed, *, value=None, ignore_missing_key=False):
        # New value is direct input parameter, or optionaly computed in code.
        key_last = key[-1]
        if value is None:
            value = module.params.get(key_last)

        # Find sub-object that needs to be updated.
        destination_value = cfg
        for kk in key[:-1]:
            if kk not in destination_value:
                if ignore_missing_key:
                    # do not create extra entries in configuratoin file
                    # RHAI 1.3 does not have serve.server.host and serve.server.port, it has serve.host_port instead.
                    return changed
                else:
                    raise errors.ILabAssertionError(
                        f"sub-key {kk} not found in configuration file, complete key={key}"
                    )
            destination_value = destination_value[kk]

        if destination_value.get(key_last) != value:
            changed = True
            destination_value[key_last] = value
        return changed

    config_file = _ilab_config_file
    # Keep a commented version of file.
    commented_config_file = config_file + ".commented"
    if not os.path.exists(commented_config_file):
        if not module.check_mode:
            shutil.copyfile(config_file, commented_config_file)

    with open(config_file) as fin:
        cfg = yaml.safe_load(fin)
    changed = False
    cfg_before = copy.deepcopy(cfg)

    changed = update_param(["serve", "model_path"], changed)
    #
    # RHAI 1.3 - uses serve.host_port
    # RHAI 1.4 - uses serve.server.host and uses serve.server.port
    # We can blindly just set both variants
    changed = update_param(["serve", "host_port"], changed)
    host, port = module.params.get("host_port").split(":")
    port = int(port)
    changed = update_param(
        ["serve", "server", "host"], changed, value=host, ignore_missing_key=True
    )
    changed = update_param(
        ["serve", "server", "port"], changed, value=port, ignore_missing_key=True
    )
    #
    changed = update_param(["serve", "backend"], changed)
    vllm_args = []
    if module.params.get("gpu_count"):
        vllm_args += ["--tensor-parallel-size", f"{module.params.get('gpu_count')}"]
    if module.params.get("token"):
        vllm_args += ["--api-key", f"{module.params.get('token')}"]
    changed = update_param(["serve", "vllm", "vllm_args"], changed, value=vllm_args)
    changed = update_param(
        ["serve", "vllm", "gpus"], changed, value=module.params.get("gpu_count")
    )
    cfg_after = cfg

    if not module.check_mode:
        with open(config_file, "w") as fout:
            yaml.dump(
                cfg,
                fout,
                Dumper=MyDumper,
                indent=2,
                default_flow_style=False,
                sort_keys=False,
            )

    diff = {}
    diff_tuple = recursive_diff(cfg_before, cfg_after)
    if diff_tuple:
        diff["before"] = diff_tuple[0]
        diff["after"] = diff_tuple[1]
    return changed, diff


def run_low_level(module):
    """
    ilab command runs inside podman container - we cannot check if file is already present there.
    """
    input_config_file = module.params["config_file"]
    ilab_config_file = _ilab_config_file
    diff = {}

    with open(input_config_file) as fin:
        input_cfg = yaml.safe_load(fin.read())
    with open(ilab_config_file) as fin:
        ilab_cfg = yaml.safe_load(fin.read())

    if input_cfg == ilab_cfg:
        changed = False
        return changed, diff

    if not module.check_mode:
        shutil.copyfile(input_config_file, ilab_config_file)
    changed = True

    diff_tuple = recursive_diff(ilab_cfg, input_cfg)
    if diff_tuple:
        diff["before"] = diff_tuple[0]
        diff["after"] = diff_tuple[1]

    return changed, diff


def run(module):
    if module.params.get("config_file"):
        return run_low_level(module)
    else:
        return run_high_level(module)


def main():
    module_args = dict(
        config_file=dict(
            type="str",
            default="",
        ),
        model_path=dict(
            type="str",
        ),
        host_port=dict(
            type="str",
            default="0.0.0.0:8000",
        ),
        token=dict(
            type="str",
            no_log=True,
        ),
        backend=dict(
            type="str",
            default="vllm",
            choices=[
                "vllm",
                "llama-cpp",
            ],
        ),
        gpu_count=dict(
            type="int",
            default=1,
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[
            ("config_file", "model_path"),
            ("config_file", "host_port"),
            ("config_file", "token"),
            ("config_file", "backend"),
            ("config_file", "gpu_count"),
        ],
    )

    if YAML_IMPORT_ERROR:
        module.fail_json(
            msg=missing_required_lib("pyyaml"), exception=YAML_IMPORT_ERROR
        )

    try:
        changed, diff = run(module)
        module.exit_json(changed=changed, diff=diff, config_file=_ilab_config_file)
    except errors.ILabError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
