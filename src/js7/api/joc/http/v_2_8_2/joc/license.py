from ......model.private.api.endpoint import EndpointDefinition, EndpointCall
from ......model.private.http.joc.joc_v_2_8_2 import Js7LicenseInfo


def license(call: EndpointCall) -> Js7LicenseInfo:
    if not call.access_token:
        raise ValueError("'access_token' is required in function call.")
    
    with call.http_service as http:
        resp = http.post(
            path="/joc/api/joc/license", 
            body=None,
            headers={
                "X-Access-Token": call.access_token, 
                "Accept": "application/json"
            }
        )
        
        return Js7LicenseInfo.model_validate_json(resp)
    
ENDPOINT_DEFINITION = EndpointDefinition(
    id="joc/license",
    function=license,
    version=("2.6.5", "2.8.3"),
    payload_model=None,
    response_model=Js7LicenseInfo,
    options=None
)