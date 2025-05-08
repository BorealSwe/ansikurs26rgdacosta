.. _redhat.ai.ilab_model_download_module:


*****************************
redhat.ai.ilab_model_download
*****************************

**Download InstructLab AI model**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- AI model is downloaded into InstructLab.
- AI models are packaged as OCI images, and are stored in OCI registry.
- Typically a login for OCI registry is needed.
- Full OCI image URL is formed from O(registry_url), O(registry_namespace), model O(name) and model O(release).




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Model name.</div>
                        <div>E.g. &quot;granite-8b-starter-v1&quot; from &quot;docker://registry.redhat.io/rhelai1/granite-8b-starter-v1:latest&quot;</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>registry_namespace</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"rhelai1"</div>
                </td>
                <td>
                        <div>The OCI image namespace.</div>
                        <div>E.g. &quot;rhelai1&quot; from &quot;docker://registry.redhat.io/rhelai1/granite-8b-starter-v1:latest&quot;</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>registry_password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The username used to login to OCI registry.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>registry_url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"docker://registry.redhat.io"</div>
                </td>
                <td>
                        <div>The OCI registry URL.</div>
                        <div>E.g. &quot;docker://registry.redhat.io&quot; from &quot;docker://registry.redhat.io/rhelai1/granite-8b-starter-v1:latest&quot;</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>registry_username</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The username used to login to OCI registry.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>release</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"latest"</div>
                </td>
                <td>
                        <div>Model release (version).</div>
                        <div>E.g. &quot;latest&quot; from &quot;docker://registry.redhat.io/rhelai1/granite-8b-starter-v1:latest&quot;</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Only a single release/version of a model can be used at a time. Reason - download of new version will replace old version at $HOME/.cache/instructlab/models/$MODEL_NAME/.
   - The module stores model version in additional file. This allows idempotency when model is downloaded a second time.
   - Directories relevant to model download - $HOME/.cache/instructlab/models/${model_name} - $HOME/.cache/instructlab/oci/${model_name}



Examples
--------

.. code-block:: yaml

    - name: Create initial InstructLab configuration.
      redhat.ai.ilab_model_download:
        name: granite-8b-starter-v1
        registry_username: my_registry_username
        registry_password: my_registry_password



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>image_created</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>Create timestamp of the model OCI image.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2025-01-31T18:29:59Z</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>model_directory</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>Model destination directory.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/var/home/ec2-user/.cache/instructlab/models/granite-8b-starter-v1</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>stderr</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>stderr of command &quot;ilab model download&quot;.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Failed to run skopeo command:
    ...</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>stdout</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>stderr of command &quot;ilab model download&quot;.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Downloading model from OCI registry:
        Model: docker://registry.redhat.io/rhelai1/granite-8b-starter-v1@latest
        Destination: /var/home/ec2-user/.cache/instructlab/models
        ...
    Writing manifest to image destination</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Justin Cinkelj (@justinc1)
