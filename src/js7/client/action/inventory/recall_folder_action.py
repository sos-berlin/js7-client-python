from typing import List, Optional

from ....model.public.client.enum.object_types import ReleaseObjectType
from ...context import Context
from ....api.joc.http.v_2_6_5.inventory.releasables.recall.folder import folder, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    CommonConfigurationType as ConfigurationType_V_2_6_5,
    CommonRequestFolder as CommonRequestFolder_V_2_6_5
)


def recall_folder_action(
    *,
    context: Context,
    folder_path: str, 
    filter_object_types: Optional[List[ReleaseObjectType]],
    recursive: bool
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            folder_path=folder_path,
            filter_object_types=filter_object_types,
            recursive=recursive
        )

        result = folder(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    folder_path: str, 
    filter_object_types: Optional[List[ReleaseObjectType]],
    recursive: bool,
) -> CommonRequestFolder_V_2_6_5:
    
    # Validate: folder_path
    if not folder_path:
        raise ValueError("'folder_path' must not be empty.")
     
    # Build: res_object_types
    res_object_types = [
        ConfigurationType_V_2_6_5(obj_type.value)
        for obj_type in filter_object_types
    ] if filter_object_types else None

    # Result
    return CommonRequestFolder_V_2_6_5(
        path=folder_path,
        object_types=res_object_types,
        recursive=recursive,
    )