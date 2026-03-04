from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    ControllerIdReq as ControllerIdReq_V_2_8_2,
    Components as Components_V_2_8_2,
    ClusterSwitchMember as ClusterSwitchMember_V_2_8_2,
    ClusterResponse as ClusterResponse_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def switch_over_action(
    *,
    context: Context,
    controller_id: str
) -> bool:

    if not check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        raise RuntimeError(
            f"Version {context.version} is not compatible with switch over."
        )

    request_data = _build_v_2_8_2_request(controller_id=controller_id)

    # (1) Get controller components
    result = context.joc_api.dispatch(
        endpoint_id="controller/components",
        call=EndpointCall(
            http_service=context.http_service,
            payload=request_data,
            access_token=context.auth_provider.login(),
            options=None
        )
    )

    if not isinstance(result, Components_V_2_8_2):
        raise RuntimeError(f"Unexpected response type from controller/components: {type(result).__name__}")

    if not result.jocs:
        raise ValueError("No JOC Cockpit instances found.")

    # (2) Find exactly one standby JOC (severity == 1)
    standby_members = [
        j.member_id
        for j in result.jocs
        if j.member_id
        and j.cluster_node_state
        and j.cluster_node_state.severity == 1
    ]

    if not standby_members:
        raise ValueError("Switch over failed: no standby JOC Cockpit instance found.")

    if len(standby_members) > 1:
        raise ValueError(f"Switch over failed: multiple standby JOCs found: {standby_members}")

    member_id = standby_members[0]

    # (3) Switch to standby member
    result = context.joc_api.dispatch(
        endpoint_id="joc/cluster/switch_member",
        call=EndpointCall(
            http_service=context.http_service,
            payload=ClusterSwitchMember_V_2_8_2(member_id=member_id),
            access_token=context.auth_provider.login(),
            options=None
        )
    )

    if not isinstance(result, ClusterResponse_V_2_8_2):
        raise RuntimeError(f"Unexpected response type from switch_member: {type(result).__name__}")

    if not result.state:
        raise RuntimeError("Switch over failed: missing state in response.")

    if result.state.value != "SWITCH_MEMBER":
        raise RuntimeError(f"Switch over failed with state: {result.state.value}")

    return True

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(*, controller_id: str) -> ControllerIdReq_V_2_8_2:
    if not controller_id:
        raise ValueError("'controller_id' is required.")

    return ControllerIdReq_V_2_8_2(controller_id=controller_id)