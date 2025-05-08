.. _redhat.ai.ilab_init_module:


*******************
redhat.ai.ilab_init
*******************

**Create initial InstructLab configuration**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Create initial InstructLab configuration.
- Existing configuration file is not modified if it already exists.




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
                    <b>force</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>If set to V(true), the configuration file will be re-created.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Command `ilab` runs in podman container.
   - When started by root, whole /root is mounted as volume.
   - Command  `ilab config init --non-interactive --config /root/asfd.yml` fails. This is reason module uses only default configuration file path.



Examples
--------

.. code-block:: yaml

    - name: Create initial InstructLab configuration.
      redhat.ai.ilab_init:




Status
------


Authors
~~~~~~~

- Justin Cinkelj (@justinc1)
