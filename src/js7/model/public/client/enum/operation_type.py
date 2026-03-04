from enum import Enum


class OperationType(str, Enum):
    DEPLOY  = "DEPLOY"
    EXPORT  = "EXPORT"
    GIT     = "GIT"
    RECALL  = "RECALL"
    RELEASE = "RELEASE"
    REMOVE  = "REMOVE"
    REVOKE  = "REVOKE"
