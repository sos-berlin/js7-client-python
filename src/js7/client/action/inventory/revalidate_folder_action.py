from ....model.public.client.common.audit_log import AuditLog
from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    ValidateRequestFolder as ValidateRequestFolder_V_2_8_2,
    AuditParams as AuditParams_V_2_8_2,
    Report as Report_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def revalidate_folder_action(*, context: Context, path: str, audit_log: AuditLog) -> bool:
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(path=path, audit_log=audit_log)
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/revalidate/folder", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))
    
    if isinstance(result, Report_V_2_8_2):
        if not result.valid_objs:
            return False
        return True
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(*, path: str, audit_log: AuditLog) -> ValidateRequestFolder_V_2_8_2:
    return ValidateRequestFolder_V_2_8_2(
        path=path,
        recursive=True,
        audit_log=AuditParams_V_2_8_2(
            ticket_link=audit_log.ticket_link,
            comment=audit_log.comment,
            time_spent=audit_log.time_spent
        )
    )