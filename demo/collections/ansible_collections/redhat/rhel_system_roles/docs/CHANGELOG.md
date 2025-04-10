Changelog
=========

[1.95.7] - 2025-03-06
----------------------------

### New Features

- [aide - New role aide to manage system integrity checking [rhel-10]](https://issues.redhat.com/browse/RHEL-67411)
- [ha_cluster - [RFE] rhel_system_roles.ha_cluster - export corosync configuration](https://issues.redhat.com/browse/RHEL-46219)
- [logging - [RFE] Add methods to define and set up custom templates in the logging role of RHEL systems roles [rhel-10]](https://issues.redhat.com/browse/RHEL-67286)
- [network - Support autoconnect_retries in the network role [rhel-10]](https://issues.redhat.com/browse/RHEL-67416)
- [network - Support may-fail in the network role [rhel-10]](https://issues.redhat.com/browse/RHEL-67415)
- [podman - support the pod quadlet type [rhel-10]](https://issues.redhat.com/browse/RHEL-67417)
- [postfix - feat: support postfix_default_database_type [rhel-10]](https://issues.redhat.com/browse/RHEL-70554)
- [sshd - fix: rename var sshd -> sshd_config and deprecate the former [rhel-10]](https://issues.redhat.com/browse/RHEL-73440)
- [sudo - feat: Add variable that handles semantic check for sudoers [rhel-10]](https://issues.redhat.com/browse/RHEL-67419)
- [systemd - support management of user units [rhel-10]](https://issues.redhat.com/browse/RHEL-67420)

### Bug Fixes

- [certificate - rhel-system-roles.certificate with IPA backend hangs processes when repeating playbook [rhel-10]](https://issues.redhat.com/browse/RHEL-70536)
- [firewall - fix: Prevent interface definitions overriding 'changed' value when other elements are changed [rhel-10]](https://issues.redhat.com/browse/RHEL-67412)
- [ha_cluster - list cloud agent packages by architecture [rhel-10]](https://issues.redhat.com/browse/RHEL-70549)
- [ha_cluster - rhel_system_roles.ha_cluster - adapt the role for pcs-0.12](https://issues.redhat.com/browse/RHEL-45303)
- [metrics - fix: add support for Valkey [rhel-10]](https://issues.redhat.com/browse/RHEL-67413)
- [network - fix: Prioritize find link info by permanent MAC address, with fallback to current address [rhel-10]](https://issues.redhat.com/browse/RHEL-73442)
- [podman - fix: get user information for secrets [rhel-10]](https://issues.redhat.com/browse/RHEL-73443)
- [postgresql - postgresql role: The postgresql_cert_name variable doesn't work with existing certificates [rhel-10]](https://issues.redhat.com/browse/RHEL-67418)
- [rhc - rhc: does not enable content in EL10 systems [rhel-10]](https://issues.redhat.com/browse/RHEL-82525)
- [sshd - fix: use quote with command, shell and validate with variable [rhel-10]](https://issues.redhat.com/browse/RHEL-73441)
- [sshd - fix: Reload the service when needed [rhel-10]](https://issues.redhat.com/browse/RHEL-73439)
- [storage - Ansible storage role 'grow_to_fill' option on LVM pools always failing with LVM resize failure due to miscalculation of free extents. [rhel-10]](https://issues.redhat.com/browse/RHEL-76504)
- [storage - "Make sure required packages are installed' task fails because Blivet requires the kmod-kvdo package, which is no longer available on RHEL-10 [rhel-10]](https://issues.redhat.com/browse/RHEL-82526)
- [systemd - fix: Always become user we are managing [rhel-10]](https://issues.redhat.com/browse/RHEL-70571)
- [vpn - no ansible-doc for redhat.rhel_system_roles.vpn_ipaddr [rhel-10]](https://issues.redhat.com/browse/RHEL-67421)

[1.88.9] - 2024-09-13
---------------------

### New Features

- [bootloader - bootloader role tests do not work on ostree [rhel-10]](https://issues.redhat.com/browse/RHEL-34881)
- [gfs2 - add gfs2 system role [rhel-10]](https://issues.redhat.com/browse/RHEL-34828)
- [ha_cluster - [RFE] rhel_system_roles.ha_cluster - ACL Support [rhel-10]](https://issues.redhat.com/browse/RHEL-34898)
- [ha_cluster - [RFE] make it easier to install cloud agents [rhel-10]](https://issues.redhat.com/browse/RHEL-34894)
- [ha_cluster - [RFE] ha_cluster_node_options allows per-node addresses and SBD options to be set [rhel-10]](https://issues.redhat.com/browse/RHEL-34893)
- [ha_cluster - [RFE] rhel_system_roles.ha_cluster - Utilization Support [rhel-10]](https://issues.redhat.com/browse/RHEL-34885)
- [ha_cluster - alerts support](https://issues.redhat.com/browse/RHEL-45285)
- [journald - feat: Add options for rate limit interval and burst [rhel-10]](https://issues.redhat.com/browse/RHEL-34892)
- [logging - RFE - system-roles - logging: Add truncate options for local file inputs](https://issues.redhat.com/browse/RHEL-48609)
- [logging - redhat.rhel_system_roles.logging role fails to process logging_outputs: of type: "custom"](https://issues.redhat.com/browse/RHEL-50288)
- [logging - [RFE] Add the umask settings or enable a variable in linux-system-roles.logging](https://issues.redhat.com/browse/RHEL-50289)
- [nbde_client - feat: Allow initrd configuration to be skipped](https://issues.redhat.com/browse/RHEL-45718)
- [network - support route src parameter](https://issues.redhat.com/browse/RHEL-53901)
- [podman - podman role should support containers-auth.json [rhel-10]](https://issues.redhat.com/browse/RHEL-34891)
- [podman - podman role should support default credentials and per-unit credentials [rhel-10]](https://issues.redhat.com/browse/RHEL-34890)
- [podman - feat: manage TLS cert/key files for registry connections and validate certs [rhel-10]](https://issues.redhat.com/browse/RHEL-34884)
- [postfix - feat: Added postfix_files feature as a simple means to add extra files/maps to config](https://issues.redhat.com/browse/RHEL-46855)
- [snapshot - feat: rewrite snapshot.py as an Ansible module / add support for thin origins](https://issues.redhat.com/browse/RHEL-48230)
- [ssh - feat: Add new configuration options and remove false positives in the test](https://issues.redhat.com/browse/RHEL-40181)
- [storage - Fingerprint storage RHEL System Role managed config files](https://issues.redhat.com/browse/RHEL-50291)
- [storage - [RFE] manage stratis [rhel-10]](https://issues.redhat.com/browse/RHEL-40798)
- [storage - [RHEL9][RFE] resize LVM PVs [rhel-10]](https://issues.redhat.com/browse/RHEL-40797)
- [sudo - Add sudo system role EL10](https://issues.redhat.com/browse/RHEL-37551)

### Bug Fixes

- [ - package rhel-system-roles.noarch does not provide docs for ansible-doc [rhel-10]](https://issues.redhat.com/browse/RHEL-34897)
- [ad_integration - fix: Sets domain name lower case in realmd.conf section header [rhel-10]](https://issues.redhat.com/browse/RHEL-34883)
- [bootloader - fix: Set user.cfg path to /boot/grub2/ on EL 9 UEFI [rhel-10]](https://issues.redhat.com/browse/RHEL-40759)
- [cockpit - cockpit install all wildcard match does not work in newer el9](https://issues.redhat.com/browse/RHEL-45944)
- [ha_cluster - Fix inconsistent approach for multiple `attributes.attrs` in `ha_cluster_node_options` [rhel-10]](https://issues.redhat.com/browse/RHEL-34886)
- [ha_cluster - Fixes for new pcs and ansible](https://issues.redhat.com/browse/RHEL-55296)
- [kdump - [RHEL-10] rhel-system-roles should depend on kdump-utils](https://issues.redhat.com/browse/RHEL-40071)
- [kernel_settings - fix: Use tuned files instead of using it as a module](https://issues.redhat.com/browse/RHEL-53897)
- [logging - Setup imuxsock using rhel-system-roles.logging causing an error EL10](https://issues.redhat.com/browse/RHEL-38456)
- [network - Make sure that the network role CI is solid robust [rhel-10]](https://issues.redhat.com/browse/RHEL-34896)
- [network - Fix testing Failures due to connection.autoconnect-ports Unknown Property [rhel-10]](https://issues.redhat.com/browse/RHEL-34887)
- [podman - Create podman secret when skip_existing=True and it does not exist [rhel-10]](https://issues.redhat.com/browse/RHEL-40795)
- [podman - fix: proper cleanup for networks; ensure cleanup of resources](https://issues.redhat.com/browse/RHEL-50104)
- [podman - fix: grab name of network to remove from quadlet file](https://issues.redhat.com/browse/RHEL-40760)
- [podman - fix: use correct user for cancel linger file name [rhel-10]](https://issues.redhat.com/browse/RHEL-34889)
- [podman - fix: do not use become for changing hostdir ownership, and expose subuid/subgid info [rhel-10]](https://issues.redhat.com/browse/RHEL-34888)
- [podman - fails to configure and run containers with podman rootless using different username and groupname](https://issues.redhat.com/browse/RHEL-57100)
- [rhc - fix: drop usage of "auto_attach" of the "redhat_subscription" module](https://issues.redhat.com/browse/RHEL-53905)
- [sshd - second SSHD service broken [rhel-10]](https://issues.redhat.com/browse/RHEL-34879)
- [storage - [RHEL8 ] var unused_disks get different sector size disks    [rhel-10]](https://issues.redhat.com/browse/RHEL-40796)
- [storage - rhel-system-role.storage is not idempotent [rhel-10]](https://issues.redhat.com/browse/RHEL-34895)

[1.23.0] - 2024-01-15
----------------------------

### New Features

- [Use .README.html in spec instead of generating it](https://issues.redhat.com/browse/RHEL-5346)
- [RHEL for Edge support in system roles](https://issues.redhat.com/browse/RHEL-3253)
- [ad_integration - feat: Add sssd custom settings](https://issues.redhat.com/browse/RHEL-17668)
- [ad_integration - Enable AD dynamic DNS updates](https://issues.redhat.com/browse/RHEL-1118)
- [ad_integration - feat: add ad_integration_preserve_authselect_profile](https://issues.redhat.com/browse/RHEL-21382)
- [ad_integration - feat: Add SSSD parameters support](https://issues.redhat.com/browse/RHEL-21133)
- [bootloader - Create bootloader role (MVP)](https://issues.redhat.com/browse/RHEL-16336)
- [fapolicyd - feat: Import code for fapolicyd system role](https://issues.redhat.com/browse/RHEL-16541)
- [ha_cluster - [RFE] HA Cluster system role should be able to enable Resilient Storage repository](https://issues.redhat.com/browse/RHEL-15910)
- [ha_cluster - [FutureFeature] Allow ha_cluster role to configure all qdevice options](https://issues.redhat.com/browse/RHEL-15908)
- [ha_cluster - [FutureFeature] Allow ha_cluster role to configure fencing topology](https://issues.redhat.com/browse/RHEL-15876)
- [ha_cluster - Setting cluster members attributes](https://issues.redhat.com/browse/RHEL-22106)
- [journald - feat: Add support for ForwardToSyslog](https://issues.redhat.com/browse/RHEL-21117)
- [logging - feat: Add support for the global config option preserveFQDN](https://issues.redhat.com/browse/RHEL-15932)
- [logging - feat: Add support for general queue and general action parameters](https://issues.redhat.com/browse/RHEL-15439)
- [metrics - [RFE] Metrics system role support for configuring PMIE webhooks](https://issues.redhat.com/browse/RHEL-13760)
- [network - Add blackhole type route](https://issues.redhat.com/browse/RHEL-19579)
- [postgresql - feat: Enable support for Postgresql 16](https://issues.redhat.com/browse/RHEL-18962)
- [rhc - support RHEL 7 managed nodes](https://issues.redhat.com/browse/RHEL-16976)
- [rhc - new rhc_insights.ansible_host parameter](https://issues.redhat.com/browse/RHEL-16974)
- [rhc - new rhc_insights.display_name parameter](https://issues.redhat.com/browse/RHEL-16964)
- [snapshot - New Role for storage snapshot management (lvm, etc.)](https://issues.redhat.com/browse/RHEL-16552)
- [sshd - ansible-sshd Manage SSH certificates](https://issues.redhat.com/browse/RHEL-5972)
- [storage - feat: Support for creating volumes without a FS](https://issues.redhat.com/browse/RHEL-16212)
- [storage - Basic support for creating shared logical volumes](https://issues.redhat.com/browse/RHEL-1535)

### Bug Fixes

- [ha_cluster - high-availability firewall service is not added on qdevice node](https://issues.redhat.com/browse/RHEL-17875)
- [ha_cluster - Timeout issue between SBD with delay-start and systemd unit](https://issues.redhat.com/browse/RHEL-18026)
- [kdump - fix: retry read of kexec_crash_size](https://issues.redhat.com/browse/RHEL-3353)
- [keylime_server - won't detect registrar start failure](https://issues.redhat.com/browse/RHEL-15909)
- [logging - fix: check that logging_max_message_size is set, not rsyslog_max_message_size](https://issues.redhat.com/browse/RHEL-15037)
- [logging - fix: avoid conf of RatelimitBurst when RatelimitInterval is zero](https://issues.redhat.com/browse/RHEL-19046)
- [nbde_server - fix: Allow tangd socket override directory to be managed outside of the role](https://issues.redhat.com/browse/RHEL-25508)
- [network - Ansible RHEL network system role issue with ipv6.routing-rules the prefix length for 'from' cannot be zero"](https://issues.redhat.com/browse/RHEL-1683)
- [podman - fix: add no_log: true for tasks that can log secret data](https://issues.redhat.com/browse/RHEL-19241)
- [podman - fix: cast secret data to string in order to allow JSON valued strings](https://issues.redhat.com/browse/RHEL-22309)
- [podman - fix: name of volume quadlet service should be basename-volume.service](https://issues.redhat.com/browse/RHEL-21401)
- [podman - fix: user linger needed before secrets](https://issues.redhat.com/browse/RHEL-22228)
- [postgresql - unable to install PostgreSQL version 15 on RHEL](https://issues.redhat.com/browse/RHEL-5274)
- [selinux - fix: Use `ignore_selinux_state` module option](https://issues.redhat.com/browse/RHEL-15870)
- [selinux - fix: Print an error message when module to be created doesn't exist](https://issues.redhat.com/browse/RHEL-19043)
- [selinux - fix: no longer use "item" as a loop variable](https://issues.redhat.com/browse/RHEL-19040)

[1.22.0] - 2023-08-15
----------------------------

### New Features

- [ALL - fingerprint in config files managed by roles](https://bugzilla.redhat.com/show_bug.cgi?id=2185062)
- [ad_integration - add ad_integration_force_rejoin](https://bugzilla.redhat.com/show_bug.cgi?id=2186253)
- [certificate - add mode parameter to change permissions for cert files](https://bugzilla.redhat.com/show_bug.cgi?id=2180902)
- [firewall - missing module in linux-system-roles.firewall to create an ipset](https://bugzilla.redhat.com/show_bug.cgi?id=2229802)
- [firewall - should have option to disable conflicting services](https://bugzilla.redhat.com/show_bug.cgi?id=2222761)
- [ha_cluster - Add possibility to load SBD watchdog kernel modules](https://bugzilla.redhat.com/show_bug.cgi?id=2185067)
- [ha_cluster - support for resource and operation defaults](https://bugzilla.redhat.com/show_bug.cgi?id=2185065)
- [kdump - support auto_reset_crashkernel, dracut_args, deprecate /etc/sysconfig/kdump](https://bugzilla.redhat.com/show_bug.cgi?id=2211187)
- [keylime_server - New role - system role for managing keylime servers](https://bugzilla.redhat.com/show_bug.cgi?id=2224385)
- [network - Support no-aaaa DNS option](https://bugzilla.redhat.com/show_bug.cgi?id=2218592)
- [network - Support configuring auto-dns setting](https://bugzilla.redhat.com/show_bug.cgi?id=2211194)
- [podman - support quadlet units](https://bugzilla.redhat.com/show_bug.cgi?id=2179455)
- [podman - allow container networking configuration](https://bugzilla.redhat.com/show_bug.cgi?id=2161712)
- [podman - support for healthchecks and healthcheck actions](https://bugzilla.redhat.com/show_bug.cgi?id=2179457)
- [podman - use getsubids to look for subuid, subgid for IdM support](https://issues.redhat.com/browse/RHEL-865)
- [podman - allow to not pull images, continue if image pull fails](https://issues.redhat.com/browse/RHEL-857)
- [postgresql - New role - system role for PostgreSQL management](https://bugzilla.redhat.com/show_bug.cgi?id=2151373)
- [rhc - implement rhc_proxy.scheme](https://bugzilla.redhat.com/show_bug.cgi?id=2211748)
- [selinux - use restorecon -T 0 on supported platforms](https://bugzilla.redhat.com/show_bug.cgi?id=2179460)
- [ssh - add ssh_backup option with default true](https://bugzilla.redhat.com/show_bug.cgi?id=2216753)
- [storage - mounted devices that are in use cannot be resized](https://bugzilla.redhat.com/show_bug.cgi?id=2168692)
- [storage - support configuring the stripe size for RAID LVM volumes](https://bugzilla.redhat.com/show_bug.cgi?id=2181656)
- [storage - user-specified mount point owner and permissions](https://bugzilla.redhat.com/show_bug.cgi?id=2181657)
- [systemd - New role - system role for managing systemd units](https://bugzilla.redhat.com/show_bug.cgi?id=2224384)

### Bug Fixes

- [ALL - facts being gathered unnecessarily](https://bugzilla.redhat.com/show_bug.cgi?id=2223032)
- [ad_integration - leaks credentials when in check_mode](https://bugzilla.redhat.com/show_bug.cgi?id=2232758)
- [certificate - does not re-issue after updating key_size](https://bugzilla.redhat.com/show_bug.cgi?id=2224138)
- [firewall - fix: reload on resetting to defaults](https://bugzilla.redhat.com/show_bug.cgi?id=2223764)
- [firewall - Check mode fails with replacing previous rules](https://issues.redhat.com/browse/RHEL-898)
- [firewall - Check mode fails when creating new firewall service](https://bugzilla.redhat.com/show_bug.cgi?id=2222428)
- [firewall - Ansible RHEL firewall system role not idempotent when configuring the interface using the role in rhel9](https://issues.redhat.com/browse/RHEL-885)
- [firewall - Don't install python(3)-firewall it's a dependency of firewalld](https://bugzilla.redhat.com/show_bug.cgi?id=2216520)
- [firewall - fix: files: overwrite firewalld.conf on previous replaced](https://issues.redhat.com/browse/RHEL-1495)
- [kdump - use failure_action instead of default on EL9 and later](https://issues.redhat.com/browse/RHEL-906)
- [kdump - "Write new authorized_keys if needed" task idempotency issues](https://bugzilla.redhat.com/show_bug.cgi?id=2232241)
- [kdump - system role fails if kdump_ssh_user doesn't have a .ssh/authorized_keys file in home directory](https://bugzilla.redhat.com/show_bug.cgi?id=2232231)
- [kdump - fix: ensure .ssh directory exists for kdump_ssh_user on kdump_ssh_server](https://issues.redhat.com/browse/RHEL-1397)
- [kdump - fix: Ensure authorized_keys management works with multiple hosts](https://issues.redhat.com/browse/RHEL-1499)
- [podman - Podman system role:  Unable to use podman_registries_conf to set unqualified-search-registries](https://bugzilla.redhat.com/show_bug.cgi?id=2211984)
- [rhc - system role does not apply Insights tags](https://bugzilla.redhat.com/show_bug.cgi?id=2209200)
- [storage - RAID volume pre cleanup - remove existing data from member disks as needed before creation](https://bugzilla.redhat.com/show_bug.cgi?id=2224090)
- [storage - Cannot set chunk size for RAID: Unsupported parameters for (blivet) module: pools.raid_chunk_size](https://bugzilla.redhat.com/show_bug.cgi?id=2193058)
- [storage - fix: use stat.pw_name, stat.gr_name instead of owner, group](https://issues.redhat.com/browse/RHEL-1497)
- [tlog - use the proxy provider - the files provider is deprecated in sssd](https://bugzilla.redhat.com/show_bug.cgi?id=2179458)

[1.21.1] - 2023-03-16
----------------------------

### New Features

- [rhc - New Role - Red Hat subscription management, insights management](https://bugzilla.redhat.com/show_bug.cgi?id=2141330)

### Bug Fixes

- none

[1.21.0] - 2023-02-20
----------------------------

### New Features

- [ad_integration - New role - manage AD integration, join to AD domain](https://bugzilla.redhat.com/show_bug.cgi?id=2140795)
- [cockpit - convert cockpit role to use firewall, selinux role, and certificate role](https://bugzilla.redhat.com/show_bug.cgi?id=2137663)
- [ha_cluster - Allow quorum device configuration](https://bugzilla.redhat.com/show_bug.cgi?id=2140804)
- [ha_cluster - convert ha_cluster role to use firewall, selinux and certificate role](https://bugzilla.redhat.com/show_bug.cgi?id=2130010)
- [journald - New role - manage systemd-journald](https://bugzilla.redhat.com/show_bug.cgi?id=2165175)
- [logging - convert logging role to use firewall, selinux role, and certificate role](https://bugzilla.redhat.com/show_bug.cgi?id=2130357)
- [metrics - convert metrics role to use firewall and selinux role](https://bugzilla.redhat.com/show_bug.cgi?id=2133528)
- [nbde_server - convert nbde_server role to use firewall and selinux role](https://bugzilla.redhat.com/show_bug.cgi?id=2133930)
- [network - Support cloned MAC address](https://bugzilla.redhat.com/show_bug.cgi?id=2143768)
- [network - Support setting the metric of the default route for initscripts provider](https://bugzilla.redhat.com/show_bug.cgi?id=2134202)
- [network - Support the DNS priority](https://bugzilla.redhat.com/show_bug.cgi?id=2133858)
- [network - Support looking up named route table in routing rule](https://bugzilla.redhat.com/show_bug.cgi?id=2131293)
- [podman - New role - manage podman containers and systemd](https://bugzilla.redhat.com/show_bug.cgi?id=2143427)
- [postfix - convert postfix role to use firewall and selinux role](https://bugzilla.redhat.com/show_bug.cgi?id=2130329)
- [selinux - add support for the 'local' parameter](https://bugzilla.redhat.com/show_bug.cgi?id=2128843)
- [vpn - Add parameters shared_key_content, ike, esp, type, leftid, rightid](https://bugzilla.redhat.com/show_bug.cgi?id=2119102)
- [vpn - convert vpn role to use firewall and selinux role](https://bugzilla.redhat.com/show_bug.cgi?id=2130344)

### Bug Fixes

- [ha_cluster - use no_log in tasks looping over pot. secret parameters](https://bugzilla.redhat.com/show_bug.cgi?id=2143816)
- [ha_cluster - Allow enabled SBD on disabled cluster](https://bugzilla.redhat.com/show_bug.cgi?id=2153030)
- [ha_cluster - Fix stonith watchdog timeout](https://bugzilla.redhat.com/show_bug.cgi?id=2167528)
- [nbde_client - must handle clevis-luks-askpass and clevis-luks-askpass@ systemd unit names](https://bugzilla.redhat.com/show_bug.cgi?id=2126959)
- [nbde_client - nbde_client_clevis fails with a traceback and prints sensitive data](https://bugzilla.redhat.com/show_bug.cgi?id=2162782)
- [network - should route traffic via correct bond](https://bugzilla.redhat.com/show_bug.cgi?id=2168735)
- [selinux - managing modules is not idempotent](https://bugzilla.redhat.com/show_bug.cgi?id=2160152)
- [sshd,ssh,timesync - Unexpected templating type error - expected str instance, int found](https://bugzilla.redhat.com/show_bug.cgi?id=2129401)
- [tlog - Unconditionally enable the files provider](https://bugzilla.redhat.com/show_bug.cgi?id=2153043)

[1.20.1] - 2022-09-27
----------------------------

### New Features

- [ssh,sshd - Sync on final OpenSSH option name RequiredRSASize in ssh and sshd roles](https://bugzilla.redhat.com/show_bug.cgi?id=2129873)

### Bug Fixes

- none

[1.20.0] - 2022-08-05
----------------------------

### New Features

- [cockpit - Add customization of port](https://bugzilla.redhat.com/show_bug.cgi?id=2115152)
- [firewall - RFE: firewall-system-role: add ability to add interface to zone by PCI device ID](https://bugzilla.redhat.com/show_bug.cgi?id=2100942)
- [firewall - support for firewall_config - gather firewall facts](https://bugzilla.redhat.com/show_bug.cgi?id=2115154)
- [logging - [RFE] Support startmsg.regex and endmsg.regex in the files inputs](https://bugzilla.redhat.com/show_bug.cgi?id=2112145)
- [selinux - Added setting of seuser and selevel for completeness](https://bugzilla.redhat.com/show_bug.cgi?id=2115157)

### Bug Fixes

- [nbde_client - Sets proper spacing for parameter rd.neednet=1](https://bugzilla.redhat.com/show_bug.cgi?id=2115156)
- [network - fix IPRouteUtils.get_route_tables_mapping() to accept any whitespace sequence](https://bugzilla.redhat.com/show_bug.cgi?id=2115886)
- [ssh sshd - ssh, sshd: RSAMinSize parameter definition is missing](https://bugzilla.redhat.com/show_bug.cgi?id=2109998)
- [storage - [RHEL9] [WARNING]: The loop variable 'storage_test_volume' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable collisions and unexpected behavior.](https://bugzilla.redhat.com/show_bug.cgi?id=2082736)

[1.19.3] - 2022-07-01
----------------------------

### New Features

- [firewall - support add/modify/delete services](https://bugzilla.redhat.com/show_bug.cgi?id=2100292)
- [network - [RFE] [network] Support managing the network through nmstate schema](https://bugzilla.redhat.com/show_bug.cgi?id=2072385)
- [storage - support for adding/removing disks to/from storage pools](https://bugzilla.redhat.com/show_bug.cgi?id=2072742)
- [storage - support for attaching cache volumes to existing volumes](https://bugzilla.redhat.com/show_bug.cgi?id=2072746)

### Bug Fixes

- [firewall - forward_port should accept list of string or list of dict](https://bugzilla.redhat.com/show_bug.cgi?id=2100605)
- [metrics - document minimum supported redis version required by rhel-system-roles](https://bugzilla.redhat.com/show_bug.cgi?id=2100286)
- [metrics - restart pmie, pmlogger if changed, do not wait for handler](https://bugzilla.redhat.com/show_bug.cgi?id=2100294)
- [storage - [RHEL9] _storage_test_pool_pvs get wrong data type in  test-verify-pool-members.yml](https://bugzilla.redhat.com/show_bug.cgi?id=2044119)

[1.19.2] - 2022-06-15
----------------------------

### New Features

- [sshd - system role should be able to optionally manage /etc/ssh/sshd_config on RHEL 9](https://bugzilla.redhat.com/show_bug.cgi?id=2052086)

### Bug Fixes

- none

[1.19.1] - 2022-06-13
----------------------------

### New Features

- [storage - support for creating and managing LVM thin pools/LVs](https://bugzilla.redhat.com/show_bug.cgi?id=2072745)
- [All roles should support running with gather_facts: false](https://bugzilla.redhat.com/show_bug.cgi?id=2078989)

### Bug Fixes

- none

[1.19.0] - 2022-06-06
----------------------------

### New Features

- [storage - support for creating and managing LVM thin pools/LVs](https://bugzilla.redhat.com/show_bug.cgi?id=2072745)
- [firewall - state no longer required for masquerade and ICMP block inversion](https://bugzilla.redhat.com/show_bug.cgi?id=2093423)

### Bug Fixes

- [storage - role raid_level "striped" is not supported](https://bugzilla.redhat.com/show_bug.cgi?id=2083410)

[1.18.0] - 2022-05-02
----------------------------

### New Features

- [firewall - [Improvement] Allow System Role to reset to default Firewalld Settings](https://bugzilla.redhat.com/show_bug.cgi?id=2043010)
- [metrics - [RFE] add an option to the metrics role to enable postfix metric collection](https://bugzilla.redhat.com/show_bug.cgi?id=2051737)
- [network - Rework the infiniband support](https://bugzilla.redhat.com/show_bug.cgi?id=2086965)
- [sshd - system role should not assume that RHEL 9 /etc/ssh/sshd_config has "Include > /etc/ssh/sshd_config.d/*.conf"](https://bugzilla.redhat.com/show_bug.cgi?id=2052081)
- [sshd - system role should be able to optionally manage /etc/ssh/sshd_config on RHEL 9](https://bugzilla.redhat.com/show_bug.cgi?id=2052086)

### Bug Fixes

- [storage - role cannot set mount_options for volumes](https://bugzilla.redhat.com/show_bug.cgi?id=2083376)

[1.17.0] - 2022-04-25
----------------------------

### New Features

- [All roles should support running with gather_facts: false](https://bugzilla.redhat.com/show_bug.cgi?id=2078989)
- [ha_cluster - support advanced corosync configuration](https://bugzilla.redhat.com/show_bug.cgi?id=2065337)
- [ha_cluster - support SBD fencing](https://bugzilla.redhat.com/show_bug.cgi?id=2079626)
- [ha_cluster - add support for configuring bundle resources](https://bugzilla.redhat.com/show_bug.cgi?id=2073519)
- [logging - Logging - RFE - support template, severity and facility options](https://bugzilla.redhat.com/show_bug.cgi?id=2075119)
- [metrics - consistently use ansible_managed in configuration files managed by role [rhel-9.1.0]](https://bugzilla.redhat.com/show_bug.cgi?id=2065392)
- [metrics - [RFE] add an option to the metrics role to enable postfix metric collection](https://bugzilla.redhat.com/show_bug.cgi?id=2051737)
- [network - [RFE] Extend rhel-system-roles.network feature set to support routing rules](https://bugzilla.redhat.com/show_bug.cgi?id=2079622)
- [postfix - Postfix RHEL System Role should provide the ability to replace config and reset configuration back to default [rhel-9.1.0]](https://bugzilla.redhat.com/show_bug.cgi?id=2065383)
- [storage - RFE storage Less verbosity by default](https://bugzilla.redhat.com/show_bug.cgi?id=2079627)

### Bug Fixes

- [firewall - Firewall system role Ansible deprecation warning related to "include"](https://bugzilla.redhat.com/show_bug.cgi?id=2061511)
- [kernel_settings - error configobj not found on RHEL 8.6 managed hosts](https://bugzilla.redhat.com/show_bug.cgi?id=2060525)
- [logging - tests fail during cleanup if no cloud-init on system](https://bugzilla.redhat.com/show_bug.cgi?id=2058799)
- [metrics - Metrics role, with "metrics_from_mssql" option does not configure /var/lib/pcp/pmdas/mssql/mssql.conf on first run](https://bugzilla.redhat.com/show_bug.cgi?id=2060523)
- [nbde_client - NBDE client system role does not support servers with static IP addresses [rhel-9.1.0]](https://bugzilla.redhat.com/show_bug.cgi?id=2070462)
- [network - bond: fix typo in supporting the infiniband ports in active-backup mode [rhel-9.1.0]](https://bugzilla.redhat.com/show_bug.cgi?id=2065394)
- [network - consistently use ansible_managed in configuration files managed by role [rhel-9.1.0]](https://bugzilla.redhat.com/show_bug.cgi?id=2065382)
- [postfix - consistently use ansible_managed in configuration files managed by role [rhel-9.1.0]](https://bugzilla.redhat.com/show_bug.cgi?id=2065393)
- [sshd - FIPS mode detection in SSHD role is wrong](https://bugzilla.redhat.com/show_bug.cgi?id=2073605)
- [tlog - Tlog role - Enabling session recording configuration does not work due to RHEL9 SSSD files provider default](https://bugzilla.redhat.com/show_bug.cgi?id=2071804)

[1.16.3] - 2022-04-07
----------------------------

### New Features

- none

### Bug Fixes

- [tlog - Tlog role - Enabling session recording configuration does not work due to RHEL9 SSSD files provider default](https://bugzilla.redhat.com/show_bug.cgi?id=2072749)

[1.16.2] - 2022-04-06
----------------------------

### New Features

- [nbde_client - NBDE client system role does not support servers with static IP addresses](https://bugzilla.redhat.com/show_bug.cgi?id=1985022)

### Bug Fixes

- none

[1.16.1] - 2022-03-29
----------------------------

### New Features

- [nbde_client - NBDE client system role does not support servers with static IP addresses](https://bugzilla.redhat.com/show_bug.cgi?id=1985022)

### Bug Fixes

- none

[1.16.0] - 2022-03-22
----------------------------

### New Features

- [network - consistently use ansible_managed in configuration files managed by role](https://bugzilla.redhat.com/show_bug.cgi?id=2057656)
- [metrics - consistently use ansible_managed in configuration files managed by role](https://bugzilla.redhat.com/show_bug.cgi?id=2057645)
- [postfix - consistently use ansible_managed in configuration files managed by role](https://bugzilla.redhat.com/show_bug.cgi?id=2057661)
- [postfix - Postfix RHEL System Role should provide the ability to replace config and reset configuration back to default](https://bugzilla.redhat.com/show_bug.cgi?id=2044657)

### Bug Fixes

- [network - bond: fix typo in supporting the infiniband ports in active-backup mode](https://bugzilla.redhat.com/show_bug.cgi?id=2064388)

[1.15.1] - 2022-03-03
----------------------------

### New Features

- none

### Bug Fixes

- [kernel_settings - error configobj not found on RHEL 8.6 managed hosts](https://bugzilla.redhat.com/show_bug.cgi?id=2058772)
- [timesync - timesync: basic-smoke test failure in timesync/tests_ntp.yml](https://bugzilla.redhat.com/show_bug.cgi?id=2058645)

[1.15.0] - 2022-03-01
----------------------------

### New Features

- [firewall - [RFE] - Firewall RHEL System Role should be able to set default zone](https://bugzilla.redhat.com/show_bug.cgi?id=2022458)

### Bug Fixes

- [metrics - Metrics role, with "metrics_from_mssql" option does not configure /var/lib/pcp/pmdas/mssql/mssql.conf on first run](https://bugzilla.redhat.com/show_bug.cgi?id=2058655)
- [firewall - ensure target changes take effect immediately](https://bugzilla.redhat.com/show_bug.cgi?id=2057172)

[1.14.0] - 2022-02-21
----------------------------

### New Features

- [network - [RFE] Add more bonding options to rhel-system-roles.network](https://bugzilla.redhat.com/show_bug.cgi?id=2008931)
- [certificate - should consistently use ansible_managed in hook scripts](https://bugzilla.redhat.com/show_bug.cgi?id=2054364)
- [tlog - consistently use ansible_managed in configuration files managed by role](https://bugzilla.redhat.com/show_bug.cgi?id=2054363)
- [vpn - consistently use ansible_managed in configuration files managed by role](https://bugzilla.redhat.com/show_bug.cgi?id=2054365)

### Bug Fixes

- [ha_cluster - set permissions for haclient group](https://bugzilla.redhat.com/show_bug.cgi?id=2049747)

[1.13.0] - 2022-02-14
----------------------------

### New Features

- [storage - RFE: Add support for RAID volumes (lvm-only)](https://bugzilla.redhat.com/show_bug.cgi?id=2016514)
- [storage - RFE: Add support for cached volumes (lvm-only)](https://bugzilla.redhat.com/show_bug.cgi?id=2016511)
- [nbde_client - NBDE client system role does not support servers with static IP addresses](https://bugzilla.redhat.com/show_bug.cgi?id=1985022)
- [ha_cluster - [RFE] ha_cluster - Support for creating resource constraints (Location, Ordering, etc.)](https://bugzilla.redhat.com/show_bug.cgi?id=2041635)
- [network - RFE: Support Routing Tables in static routes in Network Role](https://bugzilla.redhat.com/show_bug.cgi?id=2031521)

### Bug Fixes

- [metrics - role can't be re-run if the Grafana admin password has been changed](https://bugzilla.redhat.com/show_bug.cgi?id=1967321)
- [network - Failure to activate connection: nm-manager-error-quark: No suitable device found for this connection](https://bugzilla.redhat.com/show_bug.cgi?id=2034908)
- [network - Set DNS search setting only for enabled IP protocols](https://bugzilla.redhat.com/show_bug.cgi?id=2041627)

[1.12.1] - 2022-02-08
----------------------------

### New Features

- none

### Bug Fixes

- [vpn - vpn: template error while templating string: no filter named 'vpn_ipaddr'](https://bugzilla.redhat.com/show_bug.cgi?id=2050341)
- [kdump - kdump: Unable to start service kdump: Job for kdump.service failed because the control process exited with error code.](https://bugzilla.redhat.com/show_bug.cgi?id=2052105)

[1.12.0] - 2022-02-03
----------------------------

### New Features

- [Support ansible-core 2.11+](https://bugzilla.redhat.com/show_bug.cgi?id=2012316)

### Bug Fixes

- [logging - Logging role "logging_purge_confs" option not properly working](https://bugzilla.redhat.com/show_bug.cgi?id=2040812)
- [kernel_settings - role should use ansible_managed in its configuration file](https://bugzilla.redhat.com/show_bug.cgi?id=2047504)

[1.11.0] - 2022-01-20
----------------------------

### New Features

- [Support ansible-core 2.11+](https://bugzilla.redhat.com/show_bug.cgi?id=2012316)
- [cockpit - Please include "cockpit" role](https://bugzilla.redhat.com/show_bug.cgi?id=2021661)
- [ssh - ssh/tests_all_options.yml: "assertion": "'StdinNull yes' in config.content | b64decode ", failure](https://bugzilla.redhat.com/show_bug.cgi?id=2029614)

### Bug Fixes

- [timesync - timesync: Failure related to missing ntp/ntpd package/service on RHEL-9 host](https://bugzilla.redhat.com/show_bug.cgi?id=2029463)
- [logging - role missing quotes for immark module interval value](https://bugzilla.redhat.com/show_bug.cgi?id=2021678)
- [kdump - kdump: support reboot required and reboot ok](https://bugzilla.redhat.com/show_bug.cgi?id=2029605)
- [sshd - should detect FIPS mode and handle tasks correctly in FIPS mode](https://bugzilla.redhat.com/show_bug.cgi?id=1979714)

[1.10.0] - 2021-11-08
----------------------------

### New Features

- [cockpit - Please include "cockpit" role](https://bugzilla.redhat.com/show_bug.cgi?id=2021661)
- [firewall - Ansible Roles for RHEL Firewall](https://bugzilla.redhat.com/show_bug.cgi?id=1854988)
- [firewall - RFE: firewall-system-role: add ability to add-source](https://bugzilla.redhat.com/show_bug.cgi?id=1932678)
- [firewall - RFE: firewall-system-role: allow user defined zones](https://bugzilla.redhat.com/show_bug.cgi?id=1850768)
- [firewall - RFE: firewall-system-role: allow specifying the zone](https://bugzilla.redhat.com/show_bug.cgi?id=1850753)
- [Support ansible-core 2.11+](https://bugzilla.redhat.com/show_bug.cgi?id=2012316)
- [network - role: Allow to specify PCI address to configure profiles](https://bugzilla.redhat.com/show_bug.cgi?id=1695634)
- [network - [RFE] support wifi Enhanced Open (OWE)](https://bugzilla.redhat.com/show_bug.cgi?id=1993379)
- [network - [RFE] support WPA3 Simultaneous Authentication of Equals(SAE)](https://bugzilla.redhat.com/show_bug.cgi?id=1993311)
- [network - [Network] RFE: Support ignoring default gateway retrieved by DHCP/IPv6-RA](https://bugzilla.redhat.com/show_bug.cgi?id=1897565)
- [logging - [RFE]  logging - Add user and password](https://bugzilla.redhat.com/show_bug.cgi?id=2010327)

### Bug Fixes

- [Replace `# {{ ansible_managed }}` with `{{ ansible_managed | comment }}`](https://bugzilla.redhat.com/show_bug.cgi?id=2006230)
- [logging - role missing quotes for immark module interval value](https://bugzilla.redhat.com/show_bug.cgi?id=2021678)
- [logging - Logging - Performance improvement](https://bugzilla.redhat.com/show_bug.cgi?id=2005727)
- [nbde_client - add regenerate-all to the dracut command](https://bugzilla.redhat.com/show_bug.cgi?id=2021682)
- [certificate - certificates: "group" option keeps certificates inaccessible to the group](https://bugzilla.redhat.com/show_bug.cgi?id=2021683)

[1.9.0] - 2021-10-26
----------------------------

### New Features

- [logging - [RFE]  logging - Add user and password](https://bugzilla.redhat.com/show_bug.cgi?id=1990490)

### Bug Fixes

- [Replace `# {{ ansible_managed }}` with `{{ ansible_managed | comment }}`](https://bugzilla.redhat.com/show_bug.cgi?id=2006230)

[1.8.3] - 2021-08-26
----------------------------

### New Features

- [storage - RFE: Request that VDO be added to the Ansible (redhat-system-roles)](https://bugzilla.redhat.com/show_bug.cgi?id=1978488)

### Bug Fixes

- none

[1.8.2] - 2021-08-24
----------------------------

### New Features

- none

### Bug Fixes

- [logging - Update the certificates copy tasks](https://bugzilla.redhat.com/show_bug.cgi?id=1996777)

[1.8.1] - 2021-08-16
----------------------------

### New Features

- none

### Bug Fixes

- [metrics - role: the bpftrace role does not properly configure bpftrace agent](https://bugzilla.redhat.com/show_bug.cgi?id=1994180)

[1.8.0] - 2021-08-12
----------------------------

### New Features

- [drop support for Ansible 2.8](https://bugzilla.redhat.com/show_bug.cgi?id=1989197)

### Bug Fixes

- [sshd - sshd: failed to validate: error:Missing Match criteria for all Bad Match condition](https://bugzilla.redhat.com/show_bug.cgi?id=1991598)

[1.7.5] - 2021-08-10
----------------------------

### New Features

- [logging - [RFE] logging - Add a support for list value to server_host in the elasticsearch output](https://bugzilla.redhat.com/show_bug.cgi?id=1986460)

### Bug Fixes

- none

[1.7.4] - 2021-08-06
----------------------------

### New Features

- none

### Bug Fixes

- [metrics - role: Grafana dashboard not working after metrics role run unless services manually restarted](https://bugzilla.redhat.com/show_bug.cgi?id=1984150)

[1.7.0] - 2021-07-28
----------------------------

### New Features

- [logging - [RFE] logging - Add a support for list value to server_host in the elasticsearch output](https://bugzilla.redhat.com/show_bug.cgi?id=1986460)
- [storage - [RFE] storage: support volume sizes as a percentage of pool](https://bugzilla.redhat.com/show_bug.cgi?id=1984583)

### Bug Fixes

- none

[1.6.0] - 2021-07-15
----------------------------

### New Features

- [ha_cluster - RFE: ha_cluster - add pacemaker cluster properties configuration](https://bugzilla.redhat.com/show_bug.cgi?id=1982913)

### Bug Fixes

- none

[1.5.0] - 2021-07-15
----------------------------

### New Features

- [crypto_policies - rename 'policy modules' to 'subpolicies'](https://bugzilla.redhat.com/show_bug.cgi?id=1982896)

### Bug Fixes

- none

[1.4.2] - 2021-07-15
----------------------------

### New Features

- [storage - storage: relabel doesn't support](https://bugzilla.redhat.com/show_bug.cgi?id=1876315)

### Bug Fixes

- none

[1.4.1] - 2021-07-09
----------------------------

### New Features

- none

### Bug Fixes

- [network - Re-running the network system role results in "changed: true" when nothing has actually changed](https://bugzilla.redhat.com/show_bug.cgi?id=1980871)

[1.4.0] - 2021-07-08
----------------------------

### New Features

- [storage - RFE: Request that VDO be added to the Ansible (redhat-system-roles)](https://bugzilla.redhat.com/show_bug.cgi?id=1882475)

### Bug Fixes

- none

[1.3.0] - 2021-06-23
----------------------------

### New Features

- [storage - RFE: Request that VDO be added to the Ansible (redhat-system-roles)](https://bugzilla.redhat.com/show_bug.cgi?id=1978488)
- [sshd - RFE: sshd - support for appending a snippet to configuration file](https://bugzilla.redhat.com/show_bug.cgi?id=1978752)
- [timesync - RFE: timesync support for Network Time Security (NTS)](https://bugzilla.redhat.com/show_bug.cgi?id=1978753)

### Bug Fixes

- [postfix - Postfix RHEL system role README.md missing variables under the "Role Variables" section](https://bugzilla.redhat.com/show_bug.cgi?id=1978734)
- [postfix - the postfix role is not idempotent](https://bugzilla.redhat.com/show_bug.cgi?id=1978760)
- [selinux - task for semanage says Fedora in name but also runs on RHEL/CentOS 8](https://bugzilla.redhat.com/show_bug.cgi?id=1978740)
- [metrics - role task to enable logging for targeted hosts not working](https://bugzilla.redhat.com/show_bug.cgi?id=1978746)
- [sshd ssh - Unable to set sshd_hostkey_group and sshd_hostkey_mode](https://bugzilla.redhat.com/show_bug.cgi?id=1978745)

[1.2.3] - 2021-06-17
----------------------------

### New Features

- [main.yml: Add EL 9 support for all roles](https://bugzilla.redhat.com/show_bug.cgi?id=1952887)

### Bug Fixes

- none

[1.2.2] - 2021-06-15
----------------------------

### New Features

- none

### Bug Fixes

- [Internal links in README.md are broken](https://bugzilla.redhat.com/show_bug.cgi?id=1962976)

[1.2.1] - 2021-05-21
----------------------------

### New Features

- none

### Bug Fixes

- [Internal links in README.md are broken](https://bugzilla.redhat.com/show_bug.cgi?id=1962976)

[1.2.0] - 2021-05-21
----------------------------

### New Features

- [network - role: Support ethtool -G|--set-ring options](https://bugzilla.redhat.com/show_bug.cgi?id=1959649)

### Bug Fixes

- [postfix - the postfix role is not idempotent](https://bugzilla.redhat.com/show_bug.cgi?id=1960375)
- [postfix - postfix: Use FQRN in README](https://bugzilla.redhat.com/show_bug.cgi?id=1958963)
- [postfix - Documentation error in rhel-system-roles postfix readme file](https://bugzilla.redhat.com/show_bug.cgi?id=1866544)
- [storage - storage: calltrace observed when set type: partition for storage_pools](https://bugzilla.redhat.com/show_bug.cgi?id=1854187)
- [ha_cluster - cannot read preshared key in binary format](https://bugzilla.redhat.com/show_bug.cgi?id=1952620)

[1.1.0] - 2021-05-13
----------------------------

### New Features

- [timesync - [RFE] support for free form configuration for chrony](https://bugzilla.redhat.com/show_bug.cgi?id=1938023)
- [timesync - [RFE] support for timesync_max_distance to configure maxdistance/maxdist parameter](https://bugzilla.redhat.com/show_bug.cgi?id=1938016)
- [timesync - [RFE] support for ntp xleave, filter, and hw timestamping](https://bugzilla.redhat.com/show_bug.cgi?id=1938020)
- [selinux - [RFE] Ability to install custom SELinux module via Ansible](https://bugzilla.redhat.com/show_bug.cgi?id=1848683)
- [network - support for ipv6_disabled to disable ipv6 for address](https://bugzilla.redhat.com/show_bug.cgi?id=1939711)
- [vpn - [RFE] Release Ansible role for vpn in rhel-system-roles](https://bugzilla.redhat.com/show_bug.cgi?id=1943679)

### Bug Fixes

- [Bug fixes for Collection/Automation Hub](https://bugzilla.redhat.com/show_bug.cgi?id=1954747)
- [timesync - do not use ignore_errors in timesync role](https://bugzilla.redhat.com/show_bug.cgi?id=1938014)
- [selinux - rhel-system-roles should not reload the SELinux policy if its not changed](https://bugzilla.redhat.com/show_bug.cgi?id=1757869)

[0.6] - 2018-05-11
----------------------------

### New Features

- [RFE: Ansible rhel-system-roles.network: add ETHTOOL_OPTS, LINKDELAY, IPV4_FAILURE_FATAL](https://bugzilla.redhat.com/show_bug.cgi?id=1478576)

### Bug Fixes

- none
