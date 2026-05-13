from typing import List, Optional, Set, Tuple

from ...context import Context
from ....model.public.client.common.changes import Change, ChangeDependencies, ChangeStatus
from ....model.public.client.enum.object_types import ObjectType
from ....model.public.client.enum.operation_type import OperationType
from ....api.joc.http.v_2_6_5.inventory.dependencies import dependencies, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    GetDependenciesRequest as GetDependenciesRequest_V_2_6_5,
    GetDependenciesResponse as GetDependenciesResponse_V_2_6_5,
    OperationType as OperationType_V_2_6_5,
    RequestItem as RequestItem_V_2_6_5,
    ResponseObject as ResponseObject_V_2_6_5,
)


def get_change_dependencies_action(
    *,
    context: Context,
    operation_type: OperationType,
    changes: List[Tuple[str, ObjectType]],
    filter_paths: Optional[List[str]],
    filter_no_references: bool,
    filter_no_referencing: bool
) -> List[ChangeDependencies]:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            operation_type=operation_type, 
            changes=changes
        )

        result = dependencies(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return _build_v_2_6_5_response(
            response=result, 
            filter_paths=filter_paths, 
            filter_no_references=filter_no_references, 
            filter_no_referencing=filter_no_referencing
        )
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(*, operation_type: OperationType, changes: List[Tuple[str, ObjectType]]) -> GetDependenciesRequest_V_2_6_5:    
    # Validate: changes
    if not changes:
        raise ValueError("At least one change in 'changes' is required.")
    
    # Validate: changes
    for name, object_type in changes:
        if not name or not object_type:
            raise ValueError("'name' and 'object_type' are required in every change.")

        # Validate: Object Types
        if object_type in {"FOLDER", "JOBRESOURCE", "INCLUDESCRIPT", "REPORT", "DEPLOYMENTDESCRIPTOR", "DESCRIPTORFOLDER"}:
            raise ValueError(f"Object type '{object_type.value}' is not supported for dependency resolution.")
            
    return GetDependenciesRequest_V_2_6_5(
        operation_type=OperationType_V_2_6_5(operation_type.value), # Raises ValueError() if invalid.
        configurations=[
            RequestItem_V_2_6_5(name=name, type=object_type.value)
            for name, object_type in changes
        ]
    )

def _build_v_2_6_5_response(
    *,
    response: GetDependenciesResponse_V_2_6_5,
    filter_paths: Optional[List[str]],
    filter_no_references: bool,
    filter_no_referencing: bool,
) -> List[ChangeDependencies]:
    
    # No processable result: Return []
    if not response.objects or not response.requested_items:
        return []
    
    def _build_status(config: ResponseObject_V_2_6_5) -> Set[ChangeStatus]:
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