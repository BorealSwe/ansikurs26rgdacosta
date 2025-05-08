# ilab_serve

A role to setup systemd service for serving AI model.
The systemd service is a user service.
Name of systemd service is returned in **ilab_serve_service_name** variable.

## Requirements

N/A

## Role Variables

- **ilab_serve_state**:
  - Desired service state.
  - This is effective immediatelly, and lasts until reboot.
- **ilab_serve_enabled**:
  - Desired service state.
  - This is effective after reboot.
- **ilab_serve_restart_requested**:
  - Set this to true to request service restart for arbitrary reason.
    For example if configuration file was changed.
  - Precondition for restart is ``ilab_serve_state`` being true.

## Dependencies

- NA

## Example Playbook

    - hosts: ilabs
      tasks:
        - name: Start model service
          ansible.builtin.include_role:
            name: redhat.ai.ilab_serve
          vars:
            ilab_serve_state: started
            ilab_serve_enabled: true

## License

GNU General Public License v3.0 or later

See [LICENSE](https://github.com/ansible-collections/redhat.ai/blob/main/LICENSE) to see the full text.

## Author Information

- XLAB Steampunk <steampunk@xlab.si>
