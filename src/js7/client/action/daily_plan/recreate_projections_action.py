from ...context import Context
from ....api.joc.http.v_2_6_5.daily_plan.projections.recreate import recreate, EndpointCall
from ....util.version_to_tuple import version_to_tuple


def recreate_projections_action(
    *,
    context: Context
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        result = recreate(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login()
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")
