from typing import List, Literal

from ...context import Context
from ....model.public.client.common.configurations import Configuration
from ....api.joc.http.v_2_6_5.inventory.repository.read import read, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.enum.object_types import ObjectType
from ....model.private.http.joc.joc_v_2_6_5 import (
    ReadFromFilter as ReadFromFilter_V_2_6_5,
    Category as Category_V_2_6_5,
)


def read_from_local_repository_action(
    *, 
    context: Context,
    folder_path: str, 
    category: Literal["LOCAL", "ROLLOUT"]
) -> List[Configuration]:

    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            folder_path=folder_path, 
            category=category
        )

        result = read(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        if not result.items:
            return []
        
        return [
            Configuration(
                object_type=ObjectType(item.object_type.value if item.object_type else ""), 
                path=item.folder or ""
            )
            for item in result.items
        ]
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(*, folder_path: str, category: Literal["LOCAL", "ROLLOUT"]) -> ReadFromFilter_V_2_6_5:
    # Validates controller id and category
    if not folder_path or not category:
        raise ValueError("'folder_path' and 'category' are required.")
    
    # Validate: category
    if category not in ("LOCAL", "ROLLOUT"):
        raise ValueError("'category' must be one of 'LOCAL' or 'ROLLOUT'.")
    
    # Result
    return ReadFromFilter_V_2_6_5(
        folder=folder_path,
        category=Category_V_2_6_5(category), # Raises ValueError() if invalid.
        recursive=True
    )