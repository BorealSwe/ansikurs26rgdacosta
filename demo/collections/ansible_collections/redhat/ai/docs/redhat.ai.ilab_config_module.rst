.. _redhat.ai.ilab_config_module:


*********************
redhat.ai.ilab_config
*********************

**Edit existing InstructLab configuration**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Edit existing InstructLab configuration.
- Additional python libraries are required on InstructLab VM. To install them use `pip install -r requirements.txt` or equivalent.
- Module removes comments from the configuration file. On first invocation, "<original_filename>.commented" file is created. Use it if you need to consult comments to explain configuration options.
- Module changes only selected parts of the configuration file. Currently only `serve` section in the configuration file is modified. Other section will be configured in a future release.
- If additional parts of configuration file need to be modified, a whole configuration file can be provided.




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
                    <b>backend</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>vllm</b>&nbsp;&larr;</div></li>
                                    <li>llama-cpp</li>
                        </ul>
                </td>
                <td>
                        <div>The model backend used by model service.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>config_file</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">""</div>
                </td>
                <td>
                        <div>Path to configuration file to be used.</div>
                        <div>File must already exists on managed node.</div>
                        <div>If set, all other parameters are ignored.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>gpu_count</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">1</div>
                </td>
                <td>
                        <div>Number of GPUs to use.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host_port</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"0.0.0.0:8000"</div>
                </td>
                <td>
                        <div>Host address and port the model service should listen on.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>model_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Path to model to be served by model service.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>token</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authorization token required to access the model service.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - We assume configuration file is at $HOME/.config/instructlab/config.yaml



Examples
--------

.. code-block:: yaml

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
                    <b>config_file</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>Path to InstructLab configuration file.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/var/home/ec2-user/.config/instructlab/config.yaml</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>diff</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>Difference between previous configuration and new configuration.</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Justin Cinkelj (@justinc1)
