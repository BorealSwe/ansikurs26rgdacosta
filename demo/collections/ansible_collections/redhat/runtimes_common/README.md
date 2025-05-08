# Ansible Collection - Common

## About

Collection containing runtimes_common utilities to support Ansible Middleware automation

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.14.0**.

## Python version compatibility

This collection has been tested against following Python versions: **>=3.6**.

<!--end requires_ansible-->


## Included content

### Modules

* `product_download`: downloads products from the JBoss Network API
* `product_search`: searches products from the JBoss Network API
* `maven_artifact`: downloads an Artifact from a Maven Repository
* `xml`: manage bits and pieces of XML files or strings

### Filters

* `version_sort`: sort a list of strings according to version ordering


## Installation

### Installing the Collection from Automation Hub

Before using the collection, you need to setup Ansible Automation Hub as galaxy server; then install it via the CLI:

    ansible-galaxy collection install redhat.runtimes_common


### Build and install locally

Clone the repository, checkout the tag you want to build, or pick the main branch for the development version; then:

    ansible-galaxy collection build .
    ansible-galaxy collection install redhat-runtimes_common-*.tar.gz


### Dependencies

#### Python:

* [jmespath](https://jmespath.org/)
* [lxml](https://lxml.de/)

To install all the dependencies via galaxy:

    pip install -r requirements.txt

## Support

redhat.runtimes_common collection v1.2.2 is for [Technical Preview](https://access.redhat.com/support/offerings/techpreview).
If you have any issues or questions related to collection, please don't hesitate to contact us on <Ansible-middleware-core@redhat.com> or open an issue on
<https://github.com/ansible-middleware/common/issues>


## License

[Apache License 2.0](https://github.com/ansible-middleware/runtimes_common/blob/main/LICENSE)
