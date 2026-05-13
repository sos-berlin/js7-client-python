from datetime import date
from typing import List, Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.filter.element.folder import Folder
from ....api.joc.http.v_2_6_5.daily_plan.orders.generate import generate, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    Folder as Folder_V_2_6_5,
    GenerateRequest as GenerateRequest_V_2_6_5,
    PathItem as PathItem_V_2_6_5,
    Folder as Folder_V_2_6_5,
    AuditParams as AuditParams_V_2_6_5
)


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
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
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

        result = generate(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
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
) -> GenerateRequest_V_2_6_5:    
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    # Validate: daily_plan_dates
    if not daily_plan_dates:
        raise ValueError("At least one date in 'daily_plan_dates' is required.")
    
    # Build: audit_log 
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None
    
    # Result
    return GenerateRequest_V_2_6_5(
        controller_id=controller_id,
        daily_plan_dates=[
            d for d in daily_plan_dates
        ],
        schedule_paths=PathItem_V_2_6_5(
            folders=[
                Folder_V_2_6_5(folder=f.folder_path, recursive=f.recursive)
                for f in schedule_folder_paths
            ] if schedule_folder_paths else None,
            singles=schedule_paths
        ),
        workflow_paths=PathItem_V_2_6_5(
            folders=[
                Folder_V_2_6_5(folder=f.folder_path, recursive=f.recursive)
                for f in workflow_folder_paths
            ] if workflow_folder_paths else None,
            singles=workflow_paths
        ),
        overwrite=overwrite,
        with_submit=with_submit,
        include_non_auto_planned_orders=include_non_auto_planned_orders,
        audit_log=res_audit_log
    )
