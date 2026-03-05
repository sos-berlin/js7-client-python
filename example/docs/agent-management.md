# Agent Management

## Store and Deploy a Standalone Agent

```python
ok = client.agent.manage.store_standalone_agents(
    controller_id="primary-controller",
    agents=[
        js7.model.StoreAgent(
            url="http://primary-agent-service:4445",
            id="primary-agent",
            name="primary-agent",
            aliases=["primary"]
        )
    ]
)
print(f"Operation 'store_standalone_agents' successful: {ok}")

ok = client.agent.deploy.standalone_agents(
    controller_id="primary-controller",
    agent_ids=["primary-agent"]
)
print(f"Operation 'deploy.standalone_agents' successful: {ok}")
```