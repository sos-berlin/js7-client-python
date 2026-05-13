from ...context import Context
from ....api.joc.http.v_2_6_5.joc.version import version, EndpointCall
from ....util.version_to_tuple import version_to_tuple


def get_version_action(*, context: Context) -> str:
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        result = version(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login()
        ))
        
        return result.version or "unknown"
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")
