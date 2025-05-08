#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, XLAB Steampunk <steampunk@xlab.si>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ilab_model_download

author:
  - Justin Cinkelj (@justinc1)

short_description: Download InstructLab AI model

description:
  - AI model is downloaded into InstructLab.
  - AI models are packaged as OCI images, and are stored in OCI registry.
  - Typically a login for OCI registry is needed.
  - Full OCI image URL is formed from O(registry_url), O(registry_namespace), model O(name) and model O(release).

version_added: 1.0.0

notes:
  - Only a single release/version of a model can be used at a time.
    Reason - download of new version will replace old version at $HOME/.cache/instructlab/models/$MODEL_NAME/.
  - The module stores model version in additional file.
    This allows idempotency when model is downloaded a second time.
  - Directories relevant to model download
      - $HOME/.cache/instructlab/models/${model_name}
      - $HOME/.cache/instructlab/oci/${model_name}

options:
  name:
    description:
      - Model name.
      - E.g. "granite-8b-starter-v1" from "docker://registry.redhat.io/rhelai1/granite-8b-starter-v1:latest"
    type: str
    required: true
  release:
    description:
      - Model release (version).
      - E.g. "latest" from "docker://registry.redhat.io/rhelai1/granite-8b-starter-v1:latest"
    type: str
    default: "latest"
  registry_url:
    description:
      - The OCI registry URL.
      - E.g. "docker://registry.redhat.io" from "docker://registry.redhat.io/rhelai1/granite-8b-starter-v1:latest"
    type: str
    default: "docker://registry.redhat.io"
  registry_namespace:
    description:
      - The OCI image namespace.
      - E.g. "rhelai1" from "docker://registry.redhat.io/rhelai1/granite-8b-starter-v1:latest"
    type: str
    default: "rhelai1"
  registry_username:
    description:
      - The username used to login to OCI registry.
    type: str
    required: true
  registry_password:
    description:
      - The username used to login to OCI registry.
    type: str
    required: true
"""

EXAMPLES = r"""
- name: Create initial InstructLab configuration.
  redhat.ai.ilab_model_download:
    name: granite-8b-starter-v1
    registry_username: my_registry_username
    registry_password: my_registry_password
"""

# only standard return values are returned - changed, stdout, stderr
RETURN = r"""
stdout:
    description: stderr of command "ilab model download".
    returned: always
    type: str
    sample: |
      Downloading model from OCI registry:
          Model: docker://registry.redhat.io/rhelai1/granite-8b-starter-v1@latest
          Destination: /var/home/ec2-user/.cache/instructlab/models
          ...
      Writing manifest to image destination
stderr:
    description: stderr of command "ilab model download".
    returned: always
    type: str
    sample: |
      Failed to run skopeo command:
      ...
model_directory:
    description: Model destination directory.
    returned: success
    type: str
    sample: "/var/home/ec2-user/.cache/instructlab/models/granite-8b-starter-v1"
image_created:
    description: Create timestamp of the model OCI image.
    returned: success
    type: str
    sample: "2025-01-31T18:29:59Z"
"""


from ansible.module_utils.basic import AnsibleModule
import os
import json
from ..module_utils import errors

_oci_image_inspect_filename = "x-oci-image-inspect.json"


def podman_login(module):
    # we need to "podman login" also in check mode,
    # to be able to inspect_model_remote().
    registry_url = module.params["registry_url"]
    registry_username = module.params["registry_username"]
    registry_password = module.params["registry_password"]

    if registry_username and registry_password:
        registry_url_host = registry_url.replace("docker://", "")
        podman_login_cmd = [
            "podman",
            "login",
            "--username",
            registry_username,
            "--password",
            registry_password,
            registry_url_host,
        ]
        rc, out, err = module.run_command(podman_login_cmd)
        if rc != 0:
            raise errors.ILabRunCommandError(
                f"Unexpected output of command 'podman login', (rc, stdout, stderr): '{(rc, out, err)}'"
            )


# def list_models(module):
#     list_cmd = [
#         "ilab", "model", "list"
#     ]
#     rc, list_out, err = module.run_command(list_cmd)
#     if rc != 0:
#         raise errors.ILabRunCommandError(f"Unexpected output of command 'podman login', (rc, stdout, stderr): '{(rc, list_out, err)}'")
#     """
#     Output looks like:
#     +------------------------------+---------------------+---------+
#     | Model Name                   | Last Modified       | Size    |
#     +------------------------------+---------------------+---------+
#     | models/granite-8b-starter-v1 | 2025-03-19 20:52:17 | 15.2 GB |
#     +------------------------------+---------------------+---------+
#     """
#     list_lines = list_out.splitlines()
#     if not list_lines[0].startswith("+------------"):
#         raise errors.ILabAssertionError(f"Unexpected output (line 0) of command {list_cmd}: {list_out}")
#     if not list_lines[1].startswith("| Model Name "):
#         raise errors.ILabAssertionError(f"Unexpected output (line 1) of command {list_cmd}: {list_out}")
#     if not list_lines[2].startswith("+------------"):
#         raise errors.ILabAssertionError(f"Unexpected output (line 2) of command {list_cmd}: {list_out}")
#     if not list_lines[-1].startswith("+------------"):
#         raise errors.ILabAssertionError(f"Unexpected output (line -1) of command {list_cmd}: {list_out}")
#     list_lines_models = list_lines[3:-1]
#     list_models = [ln.split("|")[1].strip(" ") for ln in list_lines_models]
#     for list_model in list_models:
#         if not list_model.startswith("models/"):
#             raise errors.ILabAssertionError(f"Unexpected model name {list_model}")
#     models = [list_model.replace("models/", "") for list_model in list_models]
#     return models


def inspect_model_remote(module, model_url, model_release):
    inspect_cmd = [
        "skopeo",
        "inspect",
        "--raw",
        f"{model_url}:{model_release}",
    ]
    rc, out, err = module.run_command(inspect_cmd)
    if rc != 0:
        raise errors.ILabRunCommandError(
            f"Unexpected output of command '{' '.join(inspect_cmd)}', (rc, stdout, stderr): '{(rc, out, err)}'"
        )
    try:
        data = json.loads(out)
    except json.JSONDecodeError as ex:
        raise errors.ILabRunCommandError(
            f"JSONDecodeError - failed to load output of command '{' '.join(inspect_cmd)}', ex={ex}"
        )
    image_created = data.get("annotations", {}).get("org.opencontainers.image.created")
    if not image_created:
        raise errors.ILabAssertionError(
            f"Missing 'annotations'.'org.opencontainers.image.created' in {' '.join(inspect_cmd)} json output."
        )
    return data, image_created


def inspect_model_local(module):
    model_name = module.params["name"]
    oci_dir = os.path.join(os.environ["HOME"], ".cache/instructlab/oci", model_name)
    x_oci_image_inspect_path = os.path.join(oci_dir, _oci_image_inspect_filename)
    try:
        with open(x_oci_image_inspect_path) as fin:
            data = json.load(fin)
    except FileNotFoundError as ex:
        data = {}
        module.warn(f"Cannot open file {x_oci_image_inspect_path}, ex={ex}")
    except json.JSONDecodeError as ex:
        module.warn(f"Cannot parse file {x_oci_image_inspect_path} as json, ex={ex}")
        data = {}
    image_created = ""
    if data:
        image_created = data.get("annotations", {}).get(
            "org.opencontainers.image.created"
        )
        if not image_created:
            raise errors.ILabAssertionError(
                f"Missing 'annotations'.'org.opencontainers.image.created' in file {x_oci_image_inspect_path}."
            )
    return data, image_created


def download_model(module, model_url, model_release):
    model_name = module.params["name"]
    oci_dir = os.path.join(os.environ["HOME"], ".cache/instructlab/oci", model_name)
    models_dir = os.path.join(os.environ["HOME"], ".cache/instructlab/models")
    model_dir = os.path.join(models_dir, model_name)

    model_info_remote, image_created_remote = inspect_model_remote(
        module, model_url, model_release
    )
    model_info_local, image_created_local = inspect_model_local(module)
    if image_created_local and image_created_local == image_created_remote:
        return False, "Model already downloaded", "", model_dir, image_created_remote

    download_cmd = [
        "ilab",
        "model",
        "download",
        "--repository",
        model_url,
        "--release",
        model_release,
    ]
    if module.check_mode:
        out = "\n".join(
            [
                "Downloading model from OCI registry:",
                f"    Model: {model_url}@{model_release}",
                f"    Destination: {models_dir}",
            ]
        )
        return True, out, "", model_dir, image_created_remote
    rc, out, err = module.run_command(download_cmd)
    if rc != 0:
        raise errors.ILabRunCommandError(
            f"Unexpected output of command 'ilab model download', (rc, stdout, stderr): '{(rc, out, err)}'"
        )

    # store extra 'skopeo inspect' output to filesystem
    x_oci_image_inspect_path = os.path.join(oci_dir, _oci_image_inspect_filename)
    with open(x_oci_image_inspect_path, "w") as fout:
        json.dump(model_info_remote, fout, indent=4)

    return True, out, err, model_dir, image_created_remote


def run(module):
    """
    ilab command runs inside podman container - we cannot check if file is already present there.
    """
    # force = module.params["force"]
    model_name = module.params["name"]
    model_release = module.params["release"]
    registry_url = module.params["registry_url"]
    registry_namespace = module.params["registry_namespace"]

    model_url = f"{registry_url}/{registry_namespace}/{model_name}"

    podman_login(module)

    # models = list_models(module)
    # if model_name in models:
    #     # But model_release might be wrong. We need to download model again.
    #     # return False, f"Model already downloaded - {model_name}.", ""
    #     module.warn(f"Model was already downloaded. But release is not known, downloading it again - {model_name}.")

    changed, stdout, stderr, model_directory, image_created = download_model(
        module, model_url, model_release
    )
    return changed, stdout, stderr, model_directory, image_created


def main():
    module_args = dict(
        name=dict(
            type="str",
            required=True,
        ),
        release=dict(
            type="str",
            default="latest",
        ),
        registry_url=dict(
            type="str",
            default="docker://registry.redhat.io",
        ),
        registry_namespace=dict(
            type="str",
            default="rhelai1",
        ),
        registry_username=dict(
            type="str",
            required=True,
        ),
        registry_password=dict(
            type="str",
            required=True,
            no_log=True,
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    try:
        changed, out, err, model_directory, image_created = run(module)
        module.exit_json(
            changed=changed,
            stdout=out,
            stderr=err,
            model_directory=model_directory,
            image_created=image_created,
        )
    except errors.ILabError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
