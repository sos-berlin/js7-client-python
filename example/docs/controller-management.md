# Controller Management

## Register a Controller

```python
ok = client.controller.manage.register_controller(
    url="http://primary-controller-service:4444",
    title="PRIMARY",
    role="STANDALONE"
)
print(f"Operation 'register_controller' successful: {ok}")
```