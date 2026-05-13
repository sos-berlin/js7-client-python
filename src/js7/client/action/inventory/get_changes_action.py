from typing import List

from ...context import Context
from ....api.joc.http.v_2_6_5.inventory.changes.changes import changes, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.common.changes import Change
from ....model.public.client.enum.object_types import ObjectType
from ....model.private.http.joc.joc_v_2_6_5 import (
    ShowChangesFilter as ShowChangesFilter_V_2_6_5, 
    ShowChangesResponse as ShowChangesResponse_V_2_6_5,
    ChangeItem as ChangeItem_V_2_6_5
)


def get_changes_action(*, context: Context, names: List[str]) -> List[Change]:
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = ShowChangesFilter_V_2_6_5(
            details=True,
            names=names
        )

        result = changes(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return _build_v_2_6_5_response(result)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_response(response: ShowChangesResponse_V_2_6_5) -> List[Change]:
    if not response.changes:
        return []

    change_items: List[ChangeItem_V_2_6_5] = []
    for change in response.changes:
        if not change.configurations:
            continue

        for cfg in change.configurations:
            change_items.append(cfg)

    return [
        Change(
            path=item.path or "",
            name=item.name,
            object_type=ObjectType(item.object_type.value if item.object_type else "")
        )
        for item in change_items
    ]