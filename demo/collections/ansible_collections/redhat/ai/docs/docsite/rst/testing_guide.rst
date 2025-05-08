.. _ansible_collections.redhat.ai.docsite.testing_guide:

Testing the redhat.ai Ansible Collection
****************************************

This collection is primarily tested using GitHub Actions. However, if you wish to run the integration tests locally, follow the steps outlined below.

Prerequisites
-------------

To run the integration tests locally, you'll need a virtual machine (VM) with Red Hat AI installed. For detailed instructions on installing and deploying Red Hat Enterprise Linux AI, refer to the `Red Hat Enterprise Linux AI general availability <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux_ai/1.4/html/installing/installing_overview#installing_overview>`_.

Required Environment Variables
------------------------------

Before running the integration tests, you need to create file ``tests/integration/integration_config.yml``.

.. code-block:: yaml

    ---
    registry_username: <Registry_Username>  # Username to download AI models
    registry_password: <Registry_Password>  # Password for downloading AI models
    ilab_user: <SSH_Username>  # SSH username for accessing the VM
    ilab_host: <VM_Public_IP>  # The public IP of the VM
    ilab_ssh_private_key_filename: id_rsa_redhat_ai_aws # Path to your SSH private key
    ilab_ssh_private_key_content: |
      -----BEGIN OPENSSH PRIVATE KEY-----
      ...
      -----END OPENSSH PRIVATE KEY-----
    ansible_ssh_extra_args: -o StrictHostKeyChecking=no
    ansible_python_interpreter: /usr/bin/python3
    model_name: granite-8b-starter-v1

To generate your ``registry_username`` and ``registry_password`` for ``registry.redhat.io``, follow the instructions provided at `Red Hat Registry Authentication <https://access.redhat.com/RegistryAuthentication>`_.

Running the Tests
-----------------

To run all integration tests, use the following command:

.. code-block:: bash

    ansible-test integration

Alternatively, if you wish to run a specific test or target, use:

.. code-block:: bash

    ansible-test integration ilab_init
