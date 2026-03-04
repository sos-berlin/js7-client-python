from datetime import date
from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2,
    SubmissionsDeleteRequest as SubmissionsDeleteRequest_V_2_8_2,
    SubmissionsDeleteRequestFilter as SubmissionsDeleteRequestFilter_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def delete_submissions_action(
    *,
    context: Context,
    controller_id: str,
    filter_date_for: Optional[date],
    filter_date_from: Optional[date],
    filter_date_to: Optional[date],
    audit_log: Optional[AuditLog]
) -> bool:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_id=controller_id,
            filter_date_for=filter_date_for,
            filter_date_from=filter_date_from,
            filter_date_to=filter_date_to,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="daily_plan/submissions/delete", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None
    ))

    if isinstance(result, OK_V_2_8_2):
        return bool(result.ok)

    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    controller_id: str,
    filter_date_for: Optional[date],
    filter_date_from: Optional[date],
    filter_date_to: Optional[date],
    audit_log: Optional[AuditLog],
) -> SubmissionsDeleteRequest_V_2_8_2:
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return SubmissionsDeleteRequest_V_2_8_2(
        controller_id=controller_id,
        filter=SubmissionsDeleteRequestFilter_V_2_8_2(
            date_for=filter_date_for,
            date_from=filter_date_from,
            date_to=filter_date_to
        ),
        audit_log=res_audit_log
    )
