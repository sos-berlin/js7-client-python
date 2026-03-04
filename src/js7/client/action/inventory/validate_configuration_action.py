import json
from pathlib import Path
from typing import Any, Dict, Union

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.enum.object_types import ObjectType
from ....model.private.http.joc.joc_v_2_8_2 import (
    Validate as Validate_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def validate_configuration_action(
    *, 
    context: Context, 
    object_type: ObjectType,
    file: Union[Path, str, Dict[str, Any]]
) -> bool:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(file)
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
        
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/validate", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options={ "object_type": object_type },
    ))
    
    if isinstance(result, Validate_V_2_8_2):
        if result.valid is True:
            return True

        if result.invalid_msg:
            raise ValueError(result.invalid_msg.split(".executable.script ", 1)[1])
        
        return False
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(file: Union[Path, str, Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(file, Path):
        with open(file, encoding="utf-8") as f:
            return json.load(f)
        
    if isinstance(file, str):
        with open(Path(file), encoding="utf-8") as f:
            return json.load(f)
        
    return file