.. _ansible_collections.redhat.ai.docsite.ai_intro:

Red Hat AI Guide
****************

The ``redhat.ai`` Ansible collection provides modules for managing Red Hat AI environments. This guide explains how to use these modules to automate MLOps and deploy models for inferencing on Red Hat Enterprise Linux AI (RHEL AI) with Ansible.

.. contents::
   :local:


Installing Red Hat Enterprise Linux AI
======================================

Please referer to the `Red Hat Enterprise Linux AI general availability <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux_ai/1.4/html/installing/installing_overview#installing_overview>`_
for more information for installing and deploying Red Hat Enterprise Linux AI.


RHEL AI on AWS
==============

For information on deploying RHEL AI on AWS, refer to: `RHEL AI on AWS Guide <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux_ai/1.4/html/installing/installing_on_aws>`_.

Authentication
--------------

Using Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set your AWS credentials as environment variables:

.. code-block:: bash

    export AWS_ACCESS_KEY_ID='AK123'
    export AWS_SECRET_ACCESS_KEY='abc123'

For temporary credentials, use:

.. code-block:: bash

    export AWS_SESSION_TOKEN='your-session-token'

Note: AWS_SECURITY_TOKEN is deprecated and only retained for backward compatibility.

Using Inventory Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Alternatively, define credentials in the inventory configuration file:

.. code-block:: yaml

    # aws_ec2.yml
    plugin: amazon.aws.aws_ec2

    # The access key for your AWS account.
    aws_access_key: <YOUR-AWS-ACCESS-KEY-HERE>
    # The secret access key for your AWS account.
    aws_secret_key: <YOUR-AWS-SECRET-KEY-HERE>

Using AWS Profiles
^^^^^^^^^^^^^^^^^^

If you use different credentials for various applications, consider using AWS profiles. The profile argument is mutually exclusive with aws_access_key, aws_secret_key, and security_token. When credentials are not explicitly provided, Ansible (via boto3) defaults to the AWS configuration file located at:

.. code-block:: bash

    ~/.aws/credentials

To specify a different credentials file, set:

.. code-block:: bash

    export AWS_SHARED_CREDENTIALS_FILE='/path/to/credentials'

Minimal Example
---------------

Option 1: Using the Dynamic AWS EC2 Inventory Plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a dynamic inventory file (``aws_ec2.yml``), use the following example:

.. code-block:: yaml

    plugin: amazon.aws.aws_ec2
    aws_access_key: <YOUR-AWS-ACCESS-KEY-HERE>
    aws_secret_key: <YOUR-AWS-SECRET-KEY-HERE>
    regions:
      - us-east-1
    keyed_groups:
      - key: tags.Name
        prefix: tag_
    hostnames:
      - public-ip-address
    compose:
      ansible_host: public_ip_address
      ansible_user: ec2-user
      ansible_ssh_private_key_file: ~/.ssh/my-aws-key.pem

For more details, refer to the `AWS Dynamic Inventory Plugin <https://github.com/ansible-collections/amazon.aws/blob/main/docs/docsite/rst/aws_ec2_guide.rst>`_.

Option 2: Using a Static Inventory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you prefer a static inventory approach where you manually specify the host details (including SSH key), here's how you can do it.

To create a dynamic inventory file (``inventory.yml``), use the following example:

.. code-block:: yaml

    all:
      children:
        aws_instances:
          hosts:
            ec2_instance_1:
              ansible_host: <HOST_PUBLIC_IP>  # Replace with your EC2 instance's public IP
              ansible_user: ec2-user  # Replace with your EC2 SSH user (e.g., ec2-user, ubuntu)
              ansible_ssh_private_key_file: ~/.ssh/my-aws-key.pem  # Path to your private SSH key
              ansible_python_interpreter: /usr/bin/python3  # Ensure the correct interpre

Create a ``playbook.yml`` file:

.. code-block:: yaml

    ---
    - name: Example Playbook using redhat.ai Ansible Collection
      hosts: all
      gather_facts: false

      tasks:
        - name: Create initial ilab config
          redhat.ai.ilab_init:

        - name: Download model
          redhat.ai.ilab_model_download:
            name: "granite-8b-starter-v1"
            release: "latest"
            registry_url: "docker://registry.redhat.io"
            registry_namespace: "rhelai1"
            registry_username: "<YOUR-USERNAME-HERE>"
            registry_password: "<YOUR-PASSWORD-HERE>"

Execute the playbook using:

.. code-block:: bash

    ansible-playbook -i aws_ec2.yml playbook.yml
