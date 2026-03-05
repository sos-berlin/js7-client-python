# JS7 Python Client

[![PyPI version](https://img.shields.io/pypi/v/js7-client-python.svg)](https://pypi.org/project/js7-client-python/)
[![Python versions](https://img.shields.io/pypi/pyversions/js7-client-python)](https://pypi.org/project/js7-client-python/)

The JS7 Python Client provides methods for accessing the JS7 JOC REST API.
It offers functionality similar to the JS7 Unix CLI: [JS7 Unix CLI](https://github.com/sos-berlin/js7-cli-unix).

## Requirements

- Python version 3.8 or later
- A JS7 installation with version 2.6.5–2.8.3
- A Java JVM version 17 or later for encryption and decryption functionality

## Installation

```sh
pip install js7-client-python
```

## Quick Start

The following example shows how to create a client instance and perform an operation.

### Client Initialization

Client initialization begins with configuring the JOC API endpoint and the user’s credentials.

```python
import js7

client = js7.Client(
    http_config=js7.model.HTTPConfiguration(
        host="192.168.1.14",
        port=4443
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

The code snippet above shows authentication using Basic Auth.
However, the JS7 Python Client also supports certificate-based authentication and client certificates for HTTPS connections.

```python
client = js7.Client(
    http_config=js7.model.HTTPConfiguration(
        host="192.168.1.14",
        port=4446,
        ssl=True,
        cafile_path="./certificate.crt"
    ),
    auth_config=js7.model.AuthConfiguration(
        cert_auth=js7.model.CertAuth(
            certfile_path="./client.crt",
            keyfile_path="./client.key"
        )
    )
)
```

### Import Inventory Configurations

A common use case is importing inventory configurations into JS7 JOC.
We use the previously created client instance to import configurations.

```python
ok = client.inventory.manage.import_configurations(
    file_path="/path/to/file/or/folder",
    inventory_target_folder="/test-folder"
)

print(f"Operation successful: {ok}")
```

## Namespaces

The Client class follows the domains of the JS7 JOC API, but groups its methods into three namespaces:

- **Manage**: Used to manage configurations and resources, such as importing, updating, or removing them.
- **Operate**: Used to control runtime behavior, such as resuming a workflow or canceling an order.
- **Deploy**: Used to deploy configurations, such as workflows.

## Resources

- **Docs**: [JS7 Python Client](https://kb.sos-berlin.com/display/JS7/JS7+-+Python+Client)
- **Issues**: [JOC-2175 - Python Client for JS7 REST API](https://change.sos-berlin.com/browse/JOC-2175)
