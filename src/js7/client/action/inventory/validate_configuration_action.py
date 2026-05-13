import json
from pathlib import Path
from typing import Any, Dict, Union

from ...context import Context
from ....api.joc.http.v_2_6_5.inventory.validate import validate, EndpointCall, Options
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.enum.object_types import ObjectType


def validate_configuration_action(
    *, 
    context: Context, 
    object_type: ObjectType,
    file: Union[Path, str, Dict[str, Any]]
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(file)
        
        result = validate(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
            options=Options(object_type=object_type)
        ))
        
        if result.valid is True:
            return True

        if result.invalid_msg:
            raise ValueError(result.invalid_msg.split(".executable.script ", 1)[1])
        
        return False
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(file: Union[Path, str, Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(file, Path):
        with open(file, encoding="utf-8") as f:
            return json.load(f)
        
    if isinstance(file, str):
        with open(Path(file), encoding="utf-8") as f:
            return json.load(f)
        
    return file