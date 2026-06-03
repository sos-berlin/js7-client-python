from ...context import Context
from ....api.joc.http.v_2_6_5.task.log import log, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    TaskFilter as TaskFilter_V_2_6_5
)


def get_task_log_action(*, context: Context, controller_id: str, task_id: int) -> str:
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            controller_id=controller_id,
            task_id=task_id
        )

        result = log(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return result
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    controller_id: str,
    task_id: int
) -> TaskFilter_V_2_6_5:
    
    # Validate: controller_id
    if not controller_id:
        raise ValueError("'controller_id' is required.")
    
    return TaskFilter_V_2_6_5(
        controller_id=controller_id,
        task_id=task_id
    )