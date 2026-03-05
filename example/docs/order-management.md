# Order Management

## Cancel All Orders

```python
orders = client.order.manage.get_orders(
    controller_id="primary-controller",
    filter=js7.model.GetOrderFilter()
)

ok = client.order.operate.cancel_orders(
    controller_id="primary-controller", 
    workflow_paths=[o.workflow_path for o in orders]
)
print(f"Operation successful: {ok}")
```

