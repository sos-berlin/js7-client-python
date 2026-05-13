from ....model.public.client.common.audit_log import AuditLog
from ...context import Context
from ....api.joc.http.v_2_6_5.inventory.revalidate.folder import folder, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    ValidateRequestFolder as ValidateRequestFolder_V_2_6_5,
    AuditParams as AuditParams_V_2_6_5
)


def revalidate_folder_action(*, context: Context, path: str, audit_log: AuditLog) -> bool:
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            path=path, 
            audit_log=audit_log
        )

        result = folder(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        if not result.valid_objs:
            return False
        return True
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(*, path: str, audit_log: AuditLog) -> ValidateRequestFolder_V_2_6_5:
    return ValidateRequestFolder_V_2_6_5(
        path=path,
        recursive=True,
        audit_log=AuditParams_V_2_6_5(
            ticket_link=audit_log.ticket_link,
            comment=audit_log.comment,
            time_spent=audit_log.time_spent
        )
    )