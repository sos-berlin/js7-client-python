from datetime import date
from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....api.joc.http.v_2_6_5.daily_plan.submissions.delete import delete, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    SubmissionsDeleteRequest as SubmissionsDeleteRequest_V_2_6_5,
    SubmissionsDeleteRequestFilter as SubmissionsDeleteRequestFilter_V_2_6_5
)


def delete_submissions_action(
    *,
    context: Context,
    controller_id: str,
    filter_date_for: Optional[date],
    filter_date_from: Optional[date],
    filter_date_to: Optional[date],
    audit_log: Optional[AuditLog]
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id,
            filter_date_for=filter_date_for,
            filter_date_from=filter_date_from,
            filter_date_to=filter_date_to,
            audit_log=audit_log
        )

        result = delete(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    controller_id: str,
    filter_date_for: Optional[date],
    filter_date_from: Optional[date],
    filter_date_to: Optional[date],
    audit_log: Optional[AuditLog],
) -> SubmissionsDeleteRequest_V_2_6_5:
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return SubmissionsDeleteRequest_V_2_6_5(
        controller_id=controller_id,
        filter=SubmissionsDeleteRequestFilter_V_2_6_5(
            date_for=filter_date_for,
            date_from=filter_date_from,
            date_to=filter_date_to
        ),
        audit_log=res_audit_log
    )
