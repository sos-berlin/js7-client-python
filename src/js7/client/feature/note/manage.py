from typing import Any, Dict, Literal, Optional

from js7.model.public.client.common.audit_log import AuditLog

from ....model.public.client.enum.object_types import ObjectType

from ...context import Context

from ...action.note.get_note_action import get_note_action
from ...action.note.post_to_note_action import post_to_note_action


class Manage:
    def __init__(self, context: Context):
        self._ctx = context
        
    def get_note(
        self,
        name: str,
        object_type: ObjectType
    ) -> Dict[str, Any]:
        """
        Gets a note.
        
        Args:
            name (str):
                Object name of the configuration item.
                
            object_type (ObjectType):
                Object type of the configuration item.
                
        Returns:
            Dict[str, Any]:
                A list of posts.
                
        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version is incompatible.
        """
        
        return get_note_action(context=self._ctx, name=name, object_type=object_type)
        
    def post_to_note(
        self,
        name: str,
        object_type: ObjectType,
        content: str,
        severity: Literal["INFO", "LOW", "NORMAL", "HIGH", "CRITICAL"] = "NORMAL",
        audit_log: Optional[AuditLog] = None
    ) -> Dict[str, Any]:
        """
        Adds a post to a note and returns the updated note.
        
        Args:
            name (str):
                Object name of the configuration item.
                
            object_type (ObjectType):
                Object type of the configuration item.
        
            content (str):
                Content of a post in markdown format.
                
            severity (Literal["INFO", "LOW", "NORMAL", "HIGH", "CRITICAL"]):
                Severity of a post.
                
            audit_log (Optional[AuditLog]):
                Creates an audit log entry for this operation.
                
        Returns:
            Dict[str, Any]:
                A list of posts.
                
        Raises:
            ValueError:
                If required arguments are missing or invalid.

            RuntimeError:
                If the operation fails or the server version is incompatible.
        """
        
        return post_to_note_action(
            context=self._ctx,
            name=name,
            object_type=object_type,
            content=content,
            severity=severity,
            audit_log=audit_log
        )