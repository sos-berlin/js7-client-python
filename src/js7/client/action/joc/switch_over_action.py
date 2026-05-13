from ...context import Context
from ....api.joc.http.v_2_6_5.controller.components import components, EndpointCall as ComponentsEndpointCall
from ....api.joc.http.v_2_6_5.joc.cluster.switch_member import switch_member, EndpointCall as SwitchMemberEndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    ControllerIdReq as ControllerIdReq_V_2_6_5,
    ClusterSwitchMember as ClusterSwitchMember_V_2_6_5
)


def switch_over_action(
    *,
    context: Context,
    controller_id: str
) -> bool:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(controller_id=controller_id)

        # (1) Get controller components
        result = components(ComponentsEndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))

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
        result = switch_member(SwitchMemberEndpointCall(
            http_service=context.http_service,
                payload=ClusterSwitchMember_V_2_6_5(member_id=member_id),
                access_token=context.auth_provider.login(),
        ))

        if not result.state:
            raise RuntimeError("Switch over failed: missing state in response.")

        if result.state.value != "SWITCH_MEMBER":
            raise RuntimeError(f"Switch over failed with state: {result.state.value}")

        return True
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(*, controller_id: str) -> ControllerIdReq_V_2_6_5:
    if not controller_id:
        raise ValueError("'controller_id' is required.")

    return ControllerIdReq_V_2_6_5(controller_id=controller_id)