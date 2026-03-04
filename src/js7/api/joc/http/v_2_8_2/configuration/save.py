from ......model.private.api.endpoint import EndpointDefinition, EndpointCall
from ......model.private.http.joc.joc_v_2_8_2 import Configuration, ConfigurationOk


def save(call: EndpointCall) -> ConfigurationOk:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    if not call.payload:
        raise ValueError("'payload' is required in function call.")
    
    if not isinstance(call.payload, Configuration):
        raise ValueError("'payload' is not an instance of model.http.joc_v_2_8_2.Configuration.")
    
    body = call.payload.model_dump_json(by_alias=True, exclude_none=True)
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/configuration/save", 
            body=body,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return ConfigurationOk.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="configuration/save",
    function=save,
    version=("2.6.5", "2.8.3"),
    payload_model=Configuration,
    response_model=ConfigurationOk,
    options=None
)