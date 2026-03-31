from typing import List

from ...context import Context
from ....model.public.client.common.git_credentials import GitCredentials
from ....model.private.api.endpoint import EndpointCall
from ....model.private.http.joc.joc_v_2_8_2 import (
    GitCredentials as GitCredentials_V_2_8_2
)


def get_git_credentials_action(*, context: Context) -> List[GitCredentials]:
    # Calls the dispatcher for the matching JOC version
    result = context.joc_api.dispatch(endpoint_id="inventory/repository/git/credentials", call=EndpointCall(
        http_service=context.http_service,
        access_token=context.auth_provider.login(),
        payload=None,
        options=None,
    ))
    
    if isinstance(result, GitCredentials_V_2_8_2):
        return [
            GitCredentials(
                email=c.email,
                git_account=c.git_account,
                git_server=c.git_server,
                keyfile_path=c.keyfile_path,
                password=c.password,
                personal_access_token=c.personal_access_token,
                username=c.username
            )
            for c in result.credentials
        ] if result.credentials else []

    raise RuntimeError(f"Unexpected response type: {type(result).__name__}")