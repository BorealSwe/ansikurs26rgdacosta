Role Name
=========

The webserver role is from the rgdacosta.general collection and allows you to manage either httpd (apache) or nginx.

Requirements
------------

RHEL 8
RHEL 9 
RHEL 10

Role Variables
--------------

my_webservice -> Set to either httpd or nginx

my_action -> install (default) or uninstall

Dependencies
------------

Collections:

- ansible.posix

Roles:

none

Example Playbook
----------------
---
- name: Manage webserver 
  hosts: "{{ my_host | default('webservers') }}"
  roles:
    - webserver

License
-------

BSD

Author Information
------------------

Ricardo da Costa <rdacosta@redhat.com>
