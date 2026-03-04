from typing import Literal, Optional

from pydantic import BaseModel


class IdentityService(BaseModel):
    identity_service_name: str
    identity_service_type: Literal["UNKNOWN", "KEYCLOAK", "KEYCLOAK-JOC", "LDAP", "LDAP-JOC", "OIDC", "OIDC-JOC", "FIDO", "JOC", "CERTIFICATE"]
    service_authentication_scheme: Literal["SINGLE-FACTOR", "TWO-FACTOR"]
    second_factor: bool = False
    second_factor_identity_service_name: Optional[str] = None
    disabled: bool = False
    required: bool = False
    ordering: int = 1