from typing import List, Optional, Set

from ...context import Context
from ....model.public.client.common.changes import Change, ChangeDependencies, ChangeStatus
from ....model.public.client.enum.object_types import ObjectType
from ....model.public.client.enum.operation_type import OperationType
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    GetDependenciesRequest as GetDependenciesRequest_V_2_8_2,
    GetDependenciesResponse as GetDependenciesResponse_V_2_8_2,
    OperationType as OperationType_V_2_8_2,
    RequestItem as RequestItem_V_2_8_2,
    ResponseObject as ResponseObject_V_2_8_2,
)

from ....util.check_matching_version import check_matching_version


def get_change_dependencies_action(
    *,
    context: Context,
    operation_type: OperationType,
    changes: List[Change],
    filter_paths: Optional[List[str]],
    filter_no_references: bool,
    filter_no_referencing: bool
) -> List[ChangeDependencies]:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(operation_type=operation_type, changes=changes)
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    result = context.joc_api.dispatch(endpoint_id="inventory/dependencies", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=request_data,
        options=None,
    ))

    if isinstance(result, GetDependenciesResponse_V_2_8_2):
        return _build_v_2_8_2_response(
            response=result, 
            filter_paths=filter_paths, 
            filter_no_references=filter_no_references, 
            filter_no_referencing=filter_no_referencing
        )

    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")

#---------------------#
# Build 2.8.2 request #
#---------------------#
def _build_v_2_8_2_request(*, operation_type: OperationType, changes: List[Change]) -> GetDependenciesRequest_V_2_8_2:    
    # Validate: changes
    if not changes:
        raise ValueError("At least one change in 'changes' is required.")
    
    # Validate: changes
    for c in changes:
        if not (c.name and c.object_type):
            raise ValueError("'name' and 'object_type' are required in every change.")
    
    return GetDependenciesRequest_V_2_8_2(
        operation_type=OperationType_V_2_8_2(operation_type.value), # Raises ValueError() if invalid.
        configurations=[
            RequestItem_V_2_8_2(name=c.name, type=c.object_type)
            for c in changes
            if c.name and c.object_type # Process only valid changes
        ]
    )

#----------------------#
# Build 2.8.2 response #
#----------------------#
def _build_v_2_8_2_response(
    *,
    response: GetDependenciesResponse_V_2_8_2,
    filter_paths: Optional[List[str]],
    filter_no_references: bool,
    filter_no_referencing: bool,
) -> List[ChangeDependencies]:
    
    # No processable result: Return []
    if not response.objects or not response.requested_items:
        return []
    
    def _build_status(config: ResponseObject_V_2_8_2) -> Set[ChangeStatus]:
        status: Set[ChangeStatus] = set()
        if config.valid is True:
            status.add("VALID")
        if config.deployed is True:
            status.add("DEPLOYED")
        if config.released is True:
            status.add("RELEASED")
        return status
    
    result: List[ChangeDependencies] = [] # root_id: value
    
    for req_id in response.requested_items:
        found_parent: Optional[Change] = None
        found_dependencies: List[Change] = []
        
        for id, config in response.objects.items():
            # Found: Parent configuration
            if float(id) == req_id:
                if not config.object_type:
                    raise RuntimeError("'object_type' is required in response.")
                
                found_parent = Change(
                    path=config.path,
                    name=config.name,
                    object_type=ObjectType(config.object_type.value),
                    status=_build_status(config)
                )
                
                continue
            
            in_references = bool(config.references and req_id in config.references)
            in_referenced_by = bool(config.referenced_by and req_id in config.referenced_by)
            in_enforced_references = bool(config.enforced_references and req_id in config.enforced_references)
            in_enforced_referenced_by = bool(config.enforced_referenced_by and req_id in config.enforced_referenced_by)
            
            # Append filter logic
            if filter_no_references:
                in_references = False
            if filter_no_referencing:
                in_referenced_by = False
            
            # Skips configurations starting with 'filter_paths'
            if config.path and filter_paths:
                skip = False
                for p in filter_paths:
                    if config.path.startswith(p):
                        skip = True
                        break
                
                if skip:
                    continue
                
            if in_references or in_referenced_by or in_enforced_references or in_enforced_referenced_by:
                if not config.object_type:
                    raise RuntimeError("'object_type' is required in response.")
                
                found_dependencies.append(Change(
                    path=config.path,
                    name=config.name,
                    object_type=ObjectType(config.object_type.value),
                    status=_build_status(config)
                ))
            
        if found_parent:
            result.append(ChangeDependencies(
                path=found_parent.path,
                name=found_parent.name,
                object_type=found_parent.object_type,
                status=found_parent.status,
                dependencies=found_dependencies  
            ))
    
    return result