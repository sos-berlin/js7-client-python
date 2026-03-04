from datetime import date, datetime
from typing import List, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.filter.element.folder import Folder
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    Folder as Folder_V_2_8_2,
    GenerateRequest as GenerateRequest_V_2_8_2,
    PathItem as PathItem_V_2_8_2,
    Folder as Folder_V_2_8_2,
    AuditParams as AuditParams_V_2_8_2,
    OK as OK_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def generate_orders_action(
    *,
    context: Context,
    controller_id: str,
    daily_plan_dates: List[date],
    schedule_folder_paths: Optional[List[Folder]],
    schedule_paths: Optional[List[str]],
    workflow_folder_paths: Optional[List[Folder]],
    workflow_paths: Optional[List[str]],
    overwrite: bool,
    with_submit: bool,
    include_non_auto_planned_orders: bool,
    audit_log: Optional[AuditLog]
) -> bool:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            controller_id=controller_id,
            daily_plan_dates=daily_plan_dates,
            schedule_folder_paths=schedule_folder_paths,
            schedule_paths=schedule_paths,
            workflow_folder_paths=workflow_folder_paths,
            workflow_paths=workflow_paths,
            overwrite=overwrite,
            with_submit=with_submit,
            include_non_auto_planned_orders=include_non_auto_planned_orders,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="daily_plan/orders/generate", call=EndpointCall(
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
    daily_plan_dates: List[date],
    schedule_folder_paths: Optional[List[Folder]],
    schedule_paths: Optional[List[str]],
    workflow_folder_paths: Optional[List[Folder]],
    workflow_paths: Optional[List[str]],
    overwrite: bool,
    with_submit: bool,
    include_non_auto_planned_orders: bool,
    audit_log: Optional[AuditLog]
) -> GenerateRequest_V_2_8_2:    
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: daily_plan_dates
    if not daily_plan_dates:
        raise ValueError("At least one date in 'daily_plan_dates' is required.")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return GenerateRequest_V_2_8_2(
        controller_id=controller_id,
        daily_plan_dates=[
            datetime.combine(d, datetime.min.time())
            for d in daily_plan_dates
        ],
        schedule_paths=PathItem_V_2_8_2(
            folders=[
                Folder_V_2_8_2(folder=f.folder_path, recursive=f.recursive)
                for f in schedule_folder_paths
            ] if schedule_folder_paths else None,
            singles=schedule_paths
        ),
        workflow_paths=PathItem_V_2_8_2(
            folders=[
                Folder_V_2_8_2(folder=f.folder_path, recursive=f.recursive)
                for f in workflow_folder_paths
            ] if workflow_folder_paths else None,
            singles=workflow_paths
        ),
        overwrite=overwrite,
        with_submit=with_submit,
        include_non_auto_planned_orders=include_non_auto_planned_orders,
        audit_log=res_audit_log
    )
