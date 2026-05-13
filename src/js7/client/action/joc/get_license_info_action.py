from typing import Any, Dict, Tuple

from ...context import Context
from ....api.joc.http.v_2_6_5.joc.license import license, EndpointCall
from ....util.version_to_tuple import version_to_tuple


def get_license_info_action(*, context: Context) -> Tuple[bool, Dict[str, Any]]:
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        result = license(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login()
        ))
        
        return bool(result.valid), result.model_dump(mode="json")
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")
