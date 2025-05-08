Changes for 1.14.6 since 1.14.5
-------------------------------

  - infra/image/shcontainer: Fix log message in container_tee (#1355)
  - infra/image/shcontainer: Volume support and new container_tee (#1354)
  - test container: Add DAC_READ_SEARCH capability (#1352)
  - infra/image/shdefaults: Add SYS_PTRACE to CAP_DEFAULTS (#1351)
  - ipareplica: Don't rely on pkg_resources whenever possible (#1350)
  - Fix flake8 7 2 0 (#1349)
  - Fix CA certificates iteration (#1348)
  - Use ubuntu 24.04 for testing (#1301)

Detailed changelog for 1.14.6 since 1.14.5 by author
----------------------------------------------------
  3 authors, 13 commits

Alexander Bokovoy (1)

  - Fix CA certificates iteration

Rafael Guterres Jeffman (6)

  - test container: Add DAC_READ_SEARCH capability
  - infra/image/shcontainer: Fix log message in container_tee
  - ipareplica: Don't rely on pkg_resources whenever possible
  - Fix linter issues related to 'global'
  - Unpin flake8 version from requirements-dev.txt
  - pre-commit: Bump flake8 version to 7.2.0

Thomas Woerner (6)

  - infra/image/shcontainer: Fix processing of multi item CAP_DEFAULTS
  - infra/image/shdefaults: Add SYS_PTRACE to CAP_DEFAULTS
  - infra/image/shcontainer: Volume support and new container_tee
  - infra/image/shcontainer: Ensure '/ect/shadow' is readable
  - utils/setup_test_container.sh: Wait till systemd-journald is running
  - Use ubuntu 24.04 for testing

