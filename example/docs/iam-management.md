# IAM Management

## Create Identity Service and User

```python
ok = client.iam.manage.store_identity_service(
    identity_service=js7.model.IdentityService(
        identity_service_name="TEST-IDENTITY-SERVICE",
        identity_service_type="CERTIFICATE",
        service_authentication_scheme="SINGLE-FACTOR"
    )
)
print(f"Operation 'store_identity_service' successful: {ok}")

ok = client.iam.manage.store_role(
    identity_service_name="TEST-IDENTITY-SERVICE",
    role_name="test-role"
)
print(f"Operation 'store_role' successful: {ok}")

ok = client.iam.manage.store_account(
    account=js7.model.Account(
        account_name="test-user",
        identity_service_name="TEST-IDENTITY-SERVICE",
        password="changeit",
        roles=["test-role"]
    )
)
print(f"Operation 'store_account' successful: {ok}")
```