from typing import List, Optional

from ....model.public.client.enum.object_types import ReleaseObjectType
from ...context import Context
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    CommonConfigurationType as ConfigurationType_V_2_8_2,
    CommonRequestFolder as CommonRequestFolder_V_2_8_2,
    OK as OK_V_2_8_2,
)

from ....util.check_matching_version import check_matching_version


def recall_folder_action(
    *,
    context: Context,
    folder_path: str, 
    filter_object_types: Optional[List[ReleaseObjectType]],
    recursive: bool
) -> bool:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            folder_path=folder_path,
            filter_object_types=filter_object_types,
            recursive=recursive
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/releasables/recall/folder", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))  
    
    if isinstance(result, OK_V_2_8_2):
        return bool(result.ok)
    
    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(
    *,
    folder_path: str, 
    filter_object_types: Optional[List[ReleaseObjectType]],
    recursive: bool,
) -> CommonRequestFolder_V_2_8_2:
    
    # Validate: folder_path
    if not folder_path:
        raise ValueError("'folder_path' must not be empty.")
     
    # Build: res_object_types
    res_object_types = [
        ConfigurationType_V_2_8_2(obj_type.value)
        for obj_type in filter_object_types
    ] if filter_object_types else None

    # Result
    return CommonRequestFolder_V_2_8_2(
        path=folder_path,
        object_types=res_object_types,
        recursive=recursive,
    )