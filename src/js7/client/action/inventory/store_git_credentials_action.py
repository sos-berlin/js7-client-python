from typing import Optional

from ...context import Context
from ....model.public.client.common.audit_log import AuditLog
from ....model.public.client.common.git_credentials import GitCredentials
from ....api.joc.http.v_2_6_5.inventory.repository.git.credentials.add import add, EndpointCall
from ....util.version_to_tuple import version_to_tuple
from ....model.private.http.joc.joc_v_2_6_5 import (
    AuditParams as AuditParams_V_2_6_5,
    AddCredentialsFilter as AddCredentialsFilter_V_2_6_5,
    GitCredential as GitCredential_V_2_6_5,
    GitCredentials as GitCredentials_V_2_6_5
)


def store_git_credentials_action(
    *, 
    context: Context, 
    credentials: GitCredentials,
    audit_log: Optional[AuditLog]
) -> bool:
    
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        request_data = _build_v_2_6_5_request(
            credentials=credentials,
            audit_log=audit_log
        )

        result = add(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login(),
            payload=request_data,
        ))
        
        return bool(result.ok)
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")

def _build_v_2_6_5_request(
    *, 
    credentials: GitCredentials,
    audit_log: Optional[AuditLog]
) -> AddCredentialsFilter_V_2_6_5:
    
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
    res_audit_log = AuditParams_V_2_6_5(
        ticket_link=audit_log.ticket_link,
        comment=audit_log.comment,
        time_spent=audit_log.time_spent
    ) if audit_log else None

    # Result
    return AddCredentialsFilter_V_2_6_5(
        audit_log=res_audit_log,
        credentials=[
            GitCredentials_V_2_6_5(
                credentials=[
                    GitCredential_V_2_6_5(
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
        ]
    )