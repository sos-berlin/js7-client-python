from typing import Any, Dict

from ...context import Context
from ....api.joc.http.v_2_6_5.note.note import note, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.public.client.enum.object_types import ObjectType
from ....model.private.http.joc.joc_v_2_6_5 import (
    NoteIdentifier as NoteIdentifier_V_2_6_5,
    CommonConfigurationType as CommonConfigurationType_V_2_6_5
)


def get_note_action(
    *,
    context: Context,
    name: str,
    object_type: ObjectType
) -> Dict[str, Any]:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            name=name,
            object_type=object_type
        )

        result = note(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))

        return result.model_dump(mode="json").get("posts") or {}
        
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *,
    name: str,
    object_type: ObjectType
) -> NoteIdentifier_V_2_6_5:

    # Validate: controller_id
    if not name:
        raise ValueError("'name' is required.")
    
    # Result
    return NoteIdentifier_V_2_6_5(
        name=name,
        object_type=CommonConfigurationType_V_2_6_5(object_type.value) # Raises ValueError() if invalid.
    )
