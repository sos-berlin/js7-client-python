# Authentication Examples

## Basic Authentication

```python
import js7

client = js7.Client(
    http_config=js7.model.HTTPConfiguration(
        host="192.168.1.14",
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

## Certificate Authentication & HTTPS

```python
import js7

client = js7.Client(
    http_config=js7.model.HTTPConfiguration(
        host="192.168.1.14",
        port=4443,
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