from datetime import datetime, timezone
import json
from typing import Any, Dict, Optional

from pydantic import ValidationError
from ...model.error.http.joc_exceptions import (
    ApprovalRequired, 
    AuthenticationFailed, 
    FourEyesResponse, 
    JocOperationFailed, 
    AuthenticationResponse, 
    PermissionDenied, 
    SessionExpired,
    Err420,
    Err419,
    JocError,
    JocErr,
    JocValidationFailed
)


def joc_http_status_validator(path: str, status: int, raw_bytes: bytes) -> None:
    if status == 200:
        return

    data: Optional[Dict[str, Any]] = None
    if raw_bytes:
        try:
            data = json.loads(raw_bytes)
        except (ValueError, TypeError):
            data = None


    #------------------#
    # 401 Unauthorized #
    #------------------#
    if status == 401:
        if isinstance(data, dict):
            try:
                response = AuthenticationResponse.model_validate(data)
                raise AuthenticationFailed(response, path=path)
            except ValidationError:
                pass

        raise AuthenticationFailed(
            AuthenticationResponse(is_authenticated=False, message="Authentication failed"),
            path=path,
        )


    #---------------#
    # 403 Forbidden #
    #---------------#
    if status == 403:
        if isinstance(data, dict):
            try:
                response = AuthenticationResponse.model_validate(data)
                raise PermissionDenied(response, path=path)
            except ValidationError:
                pass

        raise PermissionDenied(
            AuthenticationResponse(is_authenticated=True, message="Permission denied"),
            path=path,
        )


    #--------------------------#
    # 420 JOC operation failed #
    #--------------------------#
    if status == 420:
        if isinstance(data, dict):
            try:
                err = Err420.model_validate(data)
                raise JocOperationFailed(err, path=path)
            except ValidationError:
                pass

        raise JocOperationFailed(
            Err420(
                delivery_date=datetime.now(timezone.utc),
                error=JocErr(code="UNKNOWN", message="Operation failed"),
            ),
            path=path,
        )


    #------------------------------#
    # 419 Validation / Object error #
    #------------------------------#
    if status == 419:
        if isinstance(data, dict):
            try:
                errors = data.get("errors")
                if isinstance(errors, list) and errors:
                    err = Err419.model_validate(errors[0])
                    raise JocValidationFailed(err, path=path)
            except ValidationError:
                pass
        
        raise JocValidationFailed(
            Err419(
                survey_date=datetime.now(timezone.utc),
                path=path,
                code="UNKNOWN",
                message="Validation failed",
            ),
            path=path,
        )

    #---------------------------------#
    # 433 Four-eyes approval required #
    #---------------------------------#
    if status == 433:
        if isinstance(data, dict):
            try:
                response = FourEyesResponse.model_validate(data)
                raise ApprovalRequired(response, path=path)
            except ValidationError:
                pass

        raise ApprovalRequired(
            FourEyesResponse(
                delivery_date=datetime.now(timezone.utc),
                message="Approval required",
                approvers=[],
            ),
            path=path,
        )
        
    
    #---------------------#
    # 440 Session expired #
    #---------------------#
    if status == 440:
        if isinstance(data, dict):
            try:
                response = AuthenticationResponse.model_validate(data)
                raise SessionExpired(response, path=path)
            except ValidationError:
                pass

        raise SessionExpired(
            AuthenticationResponse(is_authenticated=False, message="Session expired"),
            path=path,
        )


    #---------#
    # Unknown #
    #---------#
    raise JocError(
        f"Unhandled HTTP status {status}",
        path=path,
    )