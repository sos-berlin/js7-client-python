from typing import List, Literal

from ...context import Context
from ....model.public.client.common.configurations import Configuration
from ....model.private.api.endpoint import EndpointCall
from ....model.public.client.enum.object_types import ObjectType
from ....model.private.http.joc.joc_v_2_8_2 import (
    ResponseFolder as ResponseFolder_V_2_8_2,
    ReadFromFilter as ReadFromFilter_V_2_8_2,
    Category as Category_V_2_8_2,
)

from ....util.check_matching_version import check_matching_version


def read_from_local_repository_action(
    *, 
    context: Context,
    folder_path: str, 
    category: Literal["LOCAL", "ROLLOUT"]
) -> List[Configuration]:

    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(folder_path=folder_path, category=category)
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")

    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/repository/read", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None
    ))

    if isinstance(result, ResponseFolder_V_2_8_2):
        if not result.items:
            return []
        
        return [
            Configuration(
                object_type=ObjectType(item.object_type.value if item.object_type else ""), 
                path=item.folder or ""
            )
            for item in result.items
        ]

    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(*, folder_path: str, category: Literal["LOCAL", "ROLLOUT"]) -> ReadFromFilter_V_2_8_2:
    # Validates controller id and category
    if not folder_path or not category:
        raise ValueError("'folder_path' and 'category' are required.")
    
    # Validate: category
    if category not in ("LOCAL", "ROLLOUT"):
        raise ValueError("'category' must be one of 'LOCAL' or 'ROLLOUT'.")
    
    # Result
    return ReadFromFilter_V_2_8_2(
        folder=folder_path,
        category=Category_V_2_8_2(category), # Raises ValueError() if invalid.
        recursive=True
    )