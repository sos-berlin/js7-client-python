from typing import Any, Dict
from ...context import Context
from ....api.joc.http.v_2_6_5.settings.settings import settings, EndpointCall
from ....util.version_to_tuple import version_to_tuple


def get_settings_action(*, context: Context) -> Dict[str, Any]:
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        result = settings(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login()
        ))
        
        return result.model_dump(mode="json")
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")
