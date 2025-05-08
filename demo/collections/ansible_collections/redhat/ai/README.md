# redhat.ai

The ``redhat.ai`` Ansible Collection provides automation tools to manage Red Hat AI environments, streamline MLOps workflows, and deploy AI models efficiently on Red Hat Enterprise Linux AI (RHEL AI). This collection enables seamless AI model inferencing and automation using Ansible.

## Our mission

<!-- Put your collection's mission statement in here. Example follows. -->

Our mission is to provide an easy-to-use and powerful Ansible collection for deploying and managing AI models on Red Hat AI infrastructure. By leveraging automation, we reduce manual effort and improve efficiency for organizations implementing AI solutions.

We encourage contributions from all levels of expertise! Whether you're an AI/ML engineer, sysadmin, or Ansible enthusiast, your contributions help improve the collection and drive AI automation forward.

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## Communication

* Join the Ansible forum:
  * [Get Help](https://forum.ansible.com/c/help/6): get help or help others. Please add appropriate tags if you start new discussions.
  * [Social Spaces](https://forum.ansible.com/c/chat/4): gather and interact with fellow enthusiasts.
  * [News & Announcements](https://forum.ansible.com/c/news/5): track project-wide announcements including social events. The [Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn), which is used to announce releases and important changes, can also be found here.

For more information about communication, see the [Ansible communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Requirements

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.16.0**.
<!--end requires_ansible-->

### Python version compatibility

This collection requires Python 3.10 or newer.

<!-- ### Additional dependencies -->

<!-- List any external resources the collection depends on, for example minimum versions of an OS, libraries, or utilities. Do not list other Ansible collections here. -->

## Installing the Collection from Ansible Galaxy

To consume this Collection from Automation Hub, please ensure that you add the following lines to your ansible.cfg file.

```
[galaxy]
server_list = automation_hub

[galaxy_server.automation_hub]
url=https://cloud.redhat.com/api/automation-hub/
auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
token=<SuperSecretToken>
```
The token can be obtained from the [Automation Hub Web UI](https://console.redhat.com/ansible/automation-hub/token).

Once the above steps are done, you can run the following command to install the collection.

```bash
  ansible-galaxy collection install redhat.ai
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: redhat.ai
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:

```bash
ansible-galaxy collection install redhat.ai --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `1.0.0`:

```bash
ansible-galaxy collection install redhat.ai:==1.0.0
```

See [using Ansible collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

## Using this collection

You can either call modules, rulebooks and playbooks by their Fully Qualified Collection Name (FQCN), such as `redhat.ai.ilab_init`, or you can call modules by their short name if you list the redhat.ai collection in the playbook's collections keyword:

```yaml
---
- name: Create initial ilab config
  redhat.ai.ilab_init:
  register: init_result

- name: Download model
  redhat.ai.ilab_model_download:
    name: granite-8b-starter-v1
    release: latest
    registry_url: docker://registry.redhat.io
    registry_namespace: rhelai1
    registry_username: "username"
    registry_password: "password"
```

<!-- Refer the following for more details: [redhat.ai Collection Guide](docs/docsite/rst/collection_guide.rst).

## Testing

Refer the following for more details: [redhat.ai Collection Testing Guide](docs/docsite/rst/testing_guide.rst). -->

## Contributing to this collection

The content of this collection is made by people like you, a community of individuals collaborating on making the world better through developing automation software.

We are actively accepting new contributors and all types of contributions are very welcome.

Don't know how to start? Refer to the [Ansible community guide](https://docs.ansible.com/ansible/devel/community/index.html)!

Want to submit code changes? Take a look at the [Quick-start development guide](https://docs.ansible.com/ansible/devel/community/create_pr_quick_start.html).

We also use the following guidelines:

* [Collection review checklist](https://docs.ansible.com/ansible/devel/community/collection_contributors/collection_reviewing.html)
* [Ansible development guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible collection development guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)

## Release notes

Consult the CHANGELOG.rst included in the collection for details.

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible user guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible collections requirements](https://docs.ansible.com/ansible/devel/community/collection_contributors/collection_requirements.html)
- [Ansible community Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible contributor newsletter)](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn)
- [Important announcements for maintainers](https://github.com/ansible-collections/news-for-maintainers)

## Licensing

<!-- Include the appropriate license information here and a pointer to the full licensing details. If the collection contains modules migrated from the ansible/ansible repo, you must use the same license that existed in the ansible/ansible repo. See the GNU license example below. -->

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
