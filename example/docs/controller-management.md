# Controller Management

## Register a Controller

```python
ok = client.controller.manage.register_controller(
    controllers=[
        js7.model.Controller(
            url="http://primary-controller-service:4444",
            role="PRIMARY",
            title="PRIMARY",
            cluster_url="http://primary-controller-service:4444"
        ),
        js7.model.Controller(
            url="http://secondary-controller-service:4444",
            role="BACKUP",
            title="BACKUP",
            cluster_url="http://primary-controller-service:4444"
        )
    ]
)
print(f"Operation 'register_controller' successful: {ok}")
```