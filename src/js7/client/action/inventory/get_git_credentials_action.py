from typing import List

from ...context import Context
from ....model.public.client.common.git_credentials import GitCredentials
from ....api.joc.http.v_2_6_5.inventory.repository.git.credentials.credentials import credentials, EndpointCall
from ....util.version_to_tuple import version_to_tuple


def get_git_credentials_action(*, context: Context) -> List[GitCredentials]:
    if version_to_tuple(context.version) >= version_to_tuple("2.6.5"):
        result = credentials(EndpointCall(
            http_service=context.http_service,
            access_token=context.auth_provider.login()
        ))
        
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
    
    raise RuntimeError(f"JOC Cockpit version {context.version} is not supported. Minimum required version is 2.6.5.")
