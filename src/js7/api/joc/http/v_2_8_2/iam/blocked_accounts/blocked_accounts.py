from .......model.private.api.endpoint import EndpointCall, EndpointDefinition
from .......model.private.http.joc.joc_v_2_8_2 import BlockedAccountsFilter, BlockedAccounts


def blocked_accounts(call: EndpointCall) -> BlockedAccounts:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not isinstance(call.payload, BlockedAccountsFilter):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.BlockedAccountsFilter.")
        
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/iam/blockedAccounts", 
            body=body,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return BlockedAccounts.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="iam/blockedAccounts",
    function=blocked_accounts,
    version=("2.6.5", "2.8.3"),
    payload_model=BlockedAccountsFilter,
    response_model=BlockedAccounts,
    options=None
)
