# JS7 Python Client

[![PyPI version](https://img.shields.io/pypi/v/js7-client-python.svg)](https://pypi.org/project/js7-client-python/)
[![Python versions](https://img.shields.io/pypi/pyversions/js7-client-python)](https://pypi.org/project/js7-client-python/)

The JS7 Python Client provides methods for accessing the JS7 JOC REST API.
Its functionality is based on the JS7 UNIX CLI: [JS7 UNIX CLI](https://github.com/sos-berlin/js7-cli-unix)

## Requirements

- Python version 3.8 or later
- A JS7 installation with version 2.6.5 to 2.8.3
- A Java JVM version 17 or later for (en/de)cryption functionality

## Installation

```sh
pip install js7-client-python
```

## Quick Start

The following example shows how to create a client instance and execute the first operation.

### Client Initialization

Client initialization begins with configuring the JOC API endpoint and the user’s credentials.

```python
import js7

client = js7.Client(
    http_config=js7.model.HTTPConfiguration(
        host="192.168.1.1",
        port=4446
    ),
    auth_config=js7.model.AuthConfiguration(
        basic_auth=js7.model.BasicAuth(
            username="root",
            password="changeit"
        )
    )
)
```

#### SSL and Certificate-Based Authentication

>The code snippet shows authentication using Basic Auth.
>However, the JS7 Python Client also supports certificate-based authentication, provided that a corresponding identity provider and account exist in JS7 JOC.
>
>If an HTTPS certificate is required for a secure SSL connection, it can be specified in the `http_config`.

### Import Configurations

A common use case is the import of inventory configurations into JS7 JOC.
We use the previously created client instance to import configurations.

```python
client.inventory.manage.import_configurations(
    file_path="/path/to/file/or/folder",
    inventory_target_folder="/test-folder"
)
```

## Namespaces

The Client class follows the domains of the JS7 JOC API, but groups its methods into three different namespaces:

- **Manage**: Used to manage existing configurations and resources or to import new ones.
- **Operate**: Used to change the state of the system, for example to resume a workflow or cancel an order.
- **Deploy**: Used to deploy configurations such as workflows.

## Help

- **Docs**: [JS7 Python Client](https://kb.sos-berlin.com/display/JS7/JS7+-+Python+Client)
- **Issues**: [JOC-2175 - Python Client for JS7 REST API](https://change.sos-berlin.com/browse/JOC-2175)