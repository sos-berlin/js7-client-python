from typing import List

from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.common.changes import Change
from ....model.public.client.enum.object_types import ObjectType
from ....model.private.http.joc.joc_v_2_8_2 import (
    ShowChangesFilter as ShowChangesFilter_V_2_8_2, 
    ShowChangesResponse as ShowChangesResponse_V_2_8_2,
    ChangeItem as ChangeItem_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def get_changes_action(*, context: Context, names: List[str]) -> List[Change]:
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = ShowChangesFilter_V_2_8_2(
            details=True,
            names=names
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    result = context.joc_api.dispatch(endpoint_id="inventory/changes", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))

    if isinstance(result, ShowChangesResponse_V_2_8_2):
        return _build_v_2_8_2_response(result)
        
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#----------------------#
# Build 2.8.2 response #
#----------------------#
def _build_v_2_8_2_response(response: ShowChangesResponse_V_2_8_2) -> List[Change]:
    if not response.changes:
        return []

    change_items: List[ChangeItem_V_2_8_2] = []
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