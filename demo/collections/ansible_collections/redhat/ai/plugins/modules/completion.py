#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, XLAB Steampunk <steampunk@xlab.si>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: completion

author:
  - Justin Cinkelj (@justinc1)

short_description: Interact with deployed AI model

description:
  - Interact with deployed AI model.
  - AI model can be Red Hat AI model or other model server compatible with OpenAI API.
  - A simple question can be asked using a O(prompt) as input.
  - If additional control over interaction is required the O(raw_input) param should be used.
version_added: 1.0.0

options:
  base_url:
    description:
      - URL of the Red Hat AI server.
    type: str
    required: true
  validate_certs:
    description:
      - Set to false to disable TLS certificate validation.
    type: bool
    default: true
  token:
    description:
      - Authentication token for accessing the Red Hat AI server.
    type: str
    required: true
  prompt:
    description:
      - AI prompt.
      - Use this for asking a question with minimun control of payload sent to Red Hat AI server.
    type: str
    required: false
  model_path:
    description:
      - Filesystem path to AI model prompt.
    type: str
    required: false
  raw_input:
    description:
      - AI prompt.
      - Use this for asking a question with full control of payload sent to Red Hat AI server.
    type: dict
    required: false
"""

EXAMPLES = r"""
- name: Ask model a question
  redhat.ai.completion:
    base_url: "http://1.2.3.4:8000"
    token: mytoken
    prompt: "\n\n### Instructions:\nCapital of India?\n\n### Response:\n"
    model_path: /var/home/ec2-user/.cache/instructlab/models/granite-8b-starter-v1
  delegate_to: localhost

- name: Ask model a question
  redhat.ai.completion:
    base_url: "http://1.2.3.4:8000"
    token: mytoken
    raw_input:
      model: /var/home/ec2-user/.cache/instructlab/models/granite-8b-starter-v1
      prompt: "\n\n### Instructions:\nCapital of India?\n\n### Response:\n"
      stop:
        - "\n"
        - "###"
  delegate_to: localhost
"""

RETURN = r"""
raw_response:
  description: Raw JSON response from AI server.
  returned: success
  type: dict
  sample: |
    choices:
    - finish_reason: stop
      index: 0
      logprobs: null
      prompt_logprobs: null
      stop_reason: null
      text: New Delhi
    created: 1744795009
    id: cmpl-4306a46d19b04d869b5008544d7c3cd0
    model: /var/home/ec2-user/.cache/instructlab/models/granite-8b-starter-v1
    object: text_completion
    usage:
      completion_tokens: 4
      prompt_tokens: 17
      total_tokens: 21
choice_0_text:
  description: The first answer.
  returned: success
  type: str
  sample: "New Delhi"
"""


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import Request
import urllib
from ..module_utils import errors
import json


def run_high_level(module):
    prompt = module.params["prompt"]
    model_path = module.params["model_path"]
    request_data = {"model": model_path, "prompt": prompt, "stop": ["\n", "###"]}
    return run_any(module, request_data)


def run_low_level(module):
    request_data = module.params["raw_input"]
    return run_any(module, request_data)


def run_any(module, request_data):
    token = module.params["token"]
    validate_certs = module.params["validate_certs"]
    base_url = module.params["base_url"]
    base_url.rstrip("/")

    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    req = Request(headers=headers)
    url = f"{base_url}/v1/completions"
    try:
        response = req.post(
            url, data=json.dumps(request_data), validate_certs=validate_certs
        )
    except urllib.error.HTTPError as e:
        module.fail_json(msg=str(e))
    raw_response = json.load(response)
    choice_0_text = raw_response["choices"][0]["text"]
    return False, "", choice_0_text, raw_response


def run(module):
    if module.params.get("raw_input"):
        return run_low_level(module)
    else:
        return run_high_level(module)


def main():
    module_args = dict(
        base_url=dict(
            type="str",
            required=True,
        ),
        validate_certs=dict(
            type="bool",
            default=True,
        ),
        token=dict(
            type="str",
            no_log=True,
            required=True,
        ),
        prompt=dict(
            type="str",
            required=False,
        ),
        model_path=dict(
            type="str",
            required=False,
        ),
        raw_input=dict(
            type="dict",
            required=False,
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[
            ("raw_input", "prompt"),
            ("raw_input", "model_path"),
        ],
        required_one_of=[
            ["raw_input", "prompt"],
            ["raw_input", "model_path"],
        ],
        required_together=[
            ["prompt", "model_path"],
        ],
    )

    try:
        changed, stderr, choice_0_text, raw_response = run(module)
        module.exit_json(
            changed=changed,
            stderr=stderr,
            choice_0_text=choice_0_text,
            raw_response=raw_response,
        )
    except errors.ILabError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
