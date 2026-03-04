from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.git_credentials import GitCredentials
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    AuditParams as AuditParams_V_2_8_2,
    AddCredentialsFilter as AddCredentialsFilter_V_2_8_2,
    GitCredentials as GitCredentials_V_2_8_2,
    OK as OK_V_2_8_2
)

from ....util.check_matching_version import check_matching_version


def store_git_credentials_action(
    *, 
    context: Context, 
    credentials: GitCredentials,
    audit_log: Optional[AuditLog]
) -> bool:
    
    if check_matching_version(min="2.6.5", max="2.8.3", check=context.version):
        request_data = _build_v_2_8_2_request(
            credentials=credentials,
            audit_log=audit_log
        )
    else:
        raise RuntimeError(f"Version {context.version} is not compatible with building the request.")
    
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/repository/git/credentials/add", call=EndpointCall(
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
    credentials: GitCredentials,
    audit_log: Optional[AuditLog]
) -> AddCredentialsFilter_V_2_8_2:
    
    # Validate: git_account
    if not credentials.git_account:
        raise ValueError("'git_account' is required.")
    
    # Validate: username
    if not credentials.username:
        raise ValueError("'username' is required.")
    
    # Validate: email
    if not credentials.email:
        raise ValueError("'email' is required.")
    
    # Validate: password, personal_access_token and key_file_path
    auth_methods = [credentials.password, credentials.personal_access_token, credentials.keyfile_path]
    if sum(value is not None for value in auth_methods) != 1:
        raise ValueError(
            "Exactly one authentication method must be provided: "
            "'password', 'personal_access_token', or 'keyfile_path'."
        )
    
    # Validate: git_server
    if not credentials.git_server:
        raise ValueError("'git_server' is required.")
    
    # Build: Audit Log
    res_audit_log = AuditParams_V_2_8_2(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return AddCredentialsFilter_V_2_8_2(
        audit_log=res_audit_log,
        credentials=[
            GitCredentials_V_2_8_2(
                email=credentials.email,
                git_account=credentials.git_account,
                git_server=credentials.git_server,
                keyfile_path=credentials.keyfile_path,
                password=credentials.password,
                personal_access_token=credentials.personal_access_token,
                username=credentials.username
            )
        ]
    )