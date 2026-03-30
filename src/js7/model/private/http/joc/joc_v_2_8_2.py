from typing import Any, Dict, Optional, List, Union
from typing_extensions import Self
from pydantic import (Field, field_serializer, model_validator, BaseModel as PydanticBaseModel)
from datetime import date, datetime
from enum import Enum
 

#---------------#
# Configuration #
#---------------#
def snake_to_camel_case(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


class BaseModel(PydanticBaseModel):
    model_config = {
        "alias_generator": snake_to_camel_case,
        "populate_by_name": True,
        "extra": "ignore",
    }


#-------#
# ENUMS #
#-------#
class ConfigurationType(str, Enum):
    """com.sos.joc.model.configuration.ConfigurationType"""
    
    CUSTOMIZATION = "CUSTOMIZATION"
    GLOBALS = "GLOBALS"
    IGNORELIST = "IGNORELIST"
    PROFILE = "PROFILE"
    SETTING = "SETTING"
    IAM = "IAM"
    

class InstructionType(str, Enum):
    """com.sos.inventory.model.instruction.InstructionType"""
    
    ADD_ORDER = "AddOrder"
    CONSUME_NOTICES = "ConsumeNotices"
    CYCLE = "Cycle"
    EXECUTE_NAMED = "Execute.Named"
    EXPECT_NOTICE = "ExpectNotice"
    EXPECT_NOTICES = "ExpectNotices"
    FAIL = "Fail"
    FINISH = "Finish"
    FORK = "Fork"
    FORK_LIST = "ForkList"
    IF = "If"
    IMPLICIT_END = "ImplicitEnd"
    LOCK = "Lock"
    POST_NOTICE = "PostNotice"
    POST_NOTICES = "PostNotices"
    PROMPT = "Prompt"
    RETRY = "Retry"
    TRY = "Try"


class InstructionStateText(str, Enum):
    """com.sos.inventory.model.instruction.InstructionStateText"""
    
    SKIPPED = "SKIPPED"
    STOPPED = "STOPPED"
    STOPPED_AND_SKIPPED = "STOPPED_AND_SKIPPED"


class JobNotificationType(str, Enum):
    """com.sos.inventory.model.job.notification.JobNotificationType"""
    
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    

class DeployType(str, Enum):
    """com.sos.inventory.model.deploy.DeployType"""
    
    BOARD = "Board"
    FILE_WATCH = "FileWatch"
    JOB_CLASS = "JobClass"
    JOB_RESOURCE = "JobResource"
    LOCK = "Lock"
    WORKFLOW = "Workflow"
    

class SearchInstructionStateText(str, Enum):
    """com.sos.joc.model.workflow.search.InstructionStateText"""
    
    SKIPPED = "SKIPPED"
    STOPPED = "STOPPED"
    

class Severity(str, Enum):
    """com.sos.joc.model.note.common.Severity"""
    
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    INFO = "INFO"
    LOW = "LOW"
    NORMAL = "NORMAL"
    

class JobCriticality(str, Enum):
    """com.sos.inventory.model.job.JobCriticality"""
    
    CRITICAL = "CRITICAL"
    NORMAL = "NORMAL"
    

class HistoryStateText(str, Enum):
    """com.sos.joc.model.common.HistoryStateText"""
    
    FAILED = "FAILED"
    INCOMPLETE = "INCOMPLETE"
    SUCCESSFUL = "SUCCESSFUL"
    

class DailyPlanOrderStateText(str, Enum):
    """com.sos.joc.model.dailyplan.DailyPlanOrderStateText"""
    
    FINISHED = "FINISHED"
    PLANNED = "PLANNED"
    SUBMITTED = "SUBMITTED"
    

class CompatibilityLevel(str, Enum):
    """com.sos.joc.model.joc.CompatibilityLevel"""
    
    COMPATIBLE = "COMPATIBLE"
    NOT_COMPATIBLE = "NOT_COMPATIBLE"
    PARTIALLY_COMPATIBLE = "PARTIALLY_COMPATIBLE"
    
    
class JocClusterState(str, Enum):
    """com.sos.joc.model.cluster.common.state.JocClusterState"""
    
    ALREADY_RUNNING = "ALREADY_RUNNING"
    ALREADY_STARTED = "ALREADY_STARTED"
    ALREADY_STOPPED = "ALREADY_STOPPED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    MISSING_CONFIGURATION = "MISSING_CONFIGURATION"
    MISSING_HANDLERS = "MISSING_HANDLERS"
    MISSING_LICENSE = "MISSING_LICENSE"
    RESTARTED = "RESTARTED"
    RUNNING = "RUNNING"
    STARTED = "STARTED"
    STOPPED = "STOPPED"
    SWITCH_MEMBER = "SWITCH_MEMBER"
    UNCOMPLETED = "UNCOMPLETED"
    
    
class ClusterServices(str, Enum):
    """com.sos.joc.model.cluster.common.ClusterServices"""
    CLEANUP = "cleanup"
    CLUSTER = "cluster"
    DAILYPLAN = "dailyplan"
    HISTORY = "history"
    LOGNOTIFICATION = "lognotification"
    MONITOR = "monitor"
    
    
class AgentStateText(str, Enum):
    """com.sos.joc.model.agent.AgentStateText"""
    
    COUPLED = "COUPLED"
    COUPLINGFAILED = "COUPLINGFAILED"
    INITIALISED = "INITIALISED"
    RESET = "RESET"
    RESETTING = "RESETTING"
    SHUTDOWN = "SHUTDOWN"
    UNKNOWN = "UNKNOWN"
    
    
class LicenseType(str, Enum):
    """com.sos.joc.model.joc.LicenseType"""
    
    COMMERCIAL_INVALID = "COMMERCIAL_INVALID"
    COMMERCIAL_VALID = "COMMERCIAL_VALID"
    OPENSOURCE = "OPENSOURCE"
    
    
class AgentStateReason(str, Enum):
    """com.sos.joc.model.agent.AgentStateReason"""
    
    FRESH = "FRESH"
    RESET = "RESET"
    RESTARTED = "RESTARTED"
    
    
class AgentClusterStateText(str, Enum):
    """com.sos.joc.model.agent.AgentClusterStateText"""
    
    ALL_SUBAGENTS_ARE_COUPLED_AND_ENABLED = "ALL_SUBAGENTS_ARE_COUPLED_AND_ENABLED"
    NO_SUBAGENTS_ARE_COUPLED_AND_ENABLED = "NO_SUBAGENTS_ARE_COUPLED_AND_ENABLED"
    ONLY_SOME_SUBAGENTS_ARE_COUPLED_AND_ENABLED = "ONLY_SOME_SUBAGENTS_ARE_COUPLED_AND_ENABLED"
    UNKNOWN = "UNKNOWN"
    
    
class SubagentDirectorType(str, Enum):
    """com.sos.joc.model.agent.SubagentDirectorType"""
    
    NO_DIRECTOR = "NO_DIRECTOR"
    PRIMARY_DIRECTOR = "PRIMARY_DIRECTOR"
    SECONDARY_DIRECTOR = "SECONDARY_DIRECTOR"
    

class Category(str, Enum):
    """com.sos.joc.model.publish.repository.Category"""
    
    LOCAL = "LOCAL"
    ROLLOUT = "ROLLOUT"


class CommonConfigurationType(str, Enum):
    """com.sos.joc.model.inventory.common.ConfigurationType"""
    
    FOLDER = 'FOLDER'
    WORKFLOW = 'WORKFLOW'
    JOBCLASS = 'JOBCLASS'
    JOBRESOURCE = 'JOBRESOURCE'
    LOCK = 'LOCK'
    NOTICEBOARD = 'NOTICEBOARD'
    FILEORDERSOURCE = 'FILEORDERSOURCE'
    WORKINGDAYSCALENDAR = 'WORKINGDAYSCALENDAR'
    NONWORKINGDAYSCALENDAR = 'NONWORKINGDAYSCALENDAR'
    SCHEDULE = 'SCHEDULE'
    INCLUDESCRIPT = 'INCLUDESCRIPT'
    JOBTEMPLATE = 'JOBTEMPLATE'
    DEPLOYMENTDESCRIPTOR = 'DEPLOYMENTDESCRIPTOR'
    DESCRIPTORFOLDER = 'DESCRIPTORFOLDER'
    REPORT = 'REPORT'
    JOB = 'JOB'
    

class IdentityServiceType(str, Enum):
    """com.sos.joc.model.security.identityservice.IdentityServiceTypes"""
    
    CERTIFICATE = "CERTIFICATE"
    FIDO = "FIDO"
    JOC = "JOC"
    KEYCLOAK = "KEYCLOAK"
    KEYCLOAK_JOC = "KEYCLOAK-JOC"
    LDAP = "LDAP"
    LDAP_JOC = "LDAP-JOC"
    OIDC = "OIDC"
    OIDC_JOC = "OIDC-JOC"
    UNKNOWN = "UNKNOWN"


class ServiceAuthenticationScheme(str, Enum):
    """com.sos.joc.model.security.identityservice.IdentityServiceAuthenticationScheme"""
    
    SINGLE_FACTOR = "SINGLE-FACTOR"
    TWO_FACTOR = "TWO-FACTOR"


class ItemStateEnum(str, Enum):
    """com.sos.joc.model.inventory.common.ItemStateEnum"""
    
    DEPLOYMENT_IS_NEWER = "DEPLOYMENT_IS_NEWER"
    DEPLOYMENT_NOT_EXIST = "DEPLOYMENT_NOT_EXIST"
    DRAFT_IS_NEWER = "DRAFT_IS_NEWER"
    DRAFT_NOT_EXIST = "DRAFT_NOT_EXIST"
    NO_CONFIGURATION_EXIST = "NO_CONFIGURATION_EXIST"
    RELEASE_IS_NEWER = "RELEASE_IS_NEWER"
    RELEASE_NOT_EXIST = "RELEASE_NOT_EXIST"


class SyncStateText(str, Enum):
    """
    com.sos.controller.model.common.SyncStateText\n
    SUSPENDED, OUTSTANDING only for Workflows
    """

    IN_SYNC = "IN_SYNC"
    NOT_DEPLOYED = "NOT_DEPLOYED"
    NOT_IN_SYNC = "NOT_IN_SYNC"
    OUTSTANDING = "OUTSTANDING"
    SUSPENDED = "SUSPENDED"
    UNKNOWN = "UNKNOWN"

class OrderStateText(str, Enum):
    """com.sos.joc.model.order.OrderStateText"""
    
    BLOCKED = "BLOCKED"
    BROKEN = "BROKEN"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    FINISHED = "FINISHED"
    INPROGRESS = "INPROGRESS"
    PENDING = "PENDING"
    PLANNED = "PLANNED"
    PROMPTING = "PROMPTING"
    RUNNING = "RUNNING"
    SCHEDULED = "SCHEDULED"
    SUSPENDED = "SUSPENDED"
    UNKNOWN = "UNKNOWN"
    WAITING = "WAITING"


class ControllerRole(str, Enum):
    """com.sos.joc.model.controller.Role"""
    
    BACKUP = "BACKUP"
    PRIMARY = "PRIMARY"
    STANDALONE = "STANDALONE"
    
    
class JocSecurityLevel(str, Enum):
    """com.sos.joc.model.common.JocSecurityLevel"""
    
    HIGH = "HIGH"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    

class ComponentStateText(str, Enum):
    """com.sos.joc.model.controller.ComponentStateText"""
    INOPERABLE = "inoperable"
    LIMITED = "limited"
    OPERATIONAL = "operational"
    UNKNOWN = "unknown"


class ClusterNodeStateText(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNKNOWN = "unknown"
    
    
class ConnectionStateText(str, Enum):
    ESTABLISHED = "established"
    UNKNOWN = "unknown"
    UNREACHABLE = "unreachable"
    UNSTABLE = "unstable"
    

class Err(BaseModel):
    """com.sos.joc.model.common.Err"""
    
    code: Optional[str] = None
    message: Optional[str] = None
    

class AuditParams(BaseModel):
    """com.sos.joc.model.audit.AuditParams"""
    
    comment: Optional[str] = None
    ticket_link: Optional[str] = None
    time_spent: Optional[int] = None
    

class IniPermission(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.IniPermission"""
    
    permission_path: str
    excluded: Optional[bool] = None
    

class Folder(BaseModel):
    """com.sos.joc.model.common.Folder"""
    
    folder: str
    """absolute path of an object."""

    recursive: Optional[bool] = None


class DailyPlanOrderFilterBase(BaseModel):
    """com.sos.joc.model.dailyplan.DailyPlanOrderFilterBase"""

    controller_ids: Optional[List[str]] = None
    daily_plan_date_from: Optional[date] = None
    """ISO date YYYY-MM-DD"""

    daily_plan_date_to: Optional[date] = None
    """ISO date YYYY-MM-DD"""

    order_ids: Optional[List[str]] = None
    schedule_folders: Optional[List[Folder]] = None
    schedule_paths: Optional[List[str]] = None
    workflow_folders: Optional[List[Folder]] = None
    workflow_paths: Optional[List[str]] = None


class IniPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.IniPermissions"""
    
    controller_defaults: Optional[List[IniPermission]] = None
    controllers: Optional[Dict[str, List[IniPermission]]] = None
    joc: Optional[List[IniPermission]] = None


class SecurityConfigurationFolders(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.SecurityConfigurationFolders"""
    
    controllers: Optional[Dict[str, List[Folder]]] = None
    joc: Optional[List[Folder]] = None


class SecurityConfigurationRole(BaseModel):
    """com.sos.joc.model.security.configuration.SecurityConfigurationRole"""
    
    folders: Optional[SecurityConfigurationFolders] = None
    permissions: Optional[IniPermissions] = None
    

class SecurityConfigurationMainEntry(BaseModel):
    """com.sos.joc.model.security.configuration.SecurityConfigurationMainEntry"""
    
    entry_name: str
    entry_value: List[str]
    entry_comment: Optional[List[str]] = None
    
    
class Profile(BaseModel):
    """com.sos.joc.model.configuration.Profile"""
    
    account: Optional[str] = None
    last_login: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""
    

class Permission(BaseModel):
    """com.sos.joc.model.security.permissions.Permission"""
    
    excluded: Optional[bool] = None
    permission_path: str
    
    
class SecurityConfigurationAccount(BaseModel):
    """com.sos.joc.model.security.configuration.SecurityConfigurationAccount"""
    
    account_name: str
    disabled: Optional[bool] = None
    """controls if the object is disabled"""

    force_password_change: Optional[bool] = None
    """controls if the account is forced to change the password"""

    identity_service_id: Optional[float] = None
    old_password: Optional[str] = None
    password: Optional[str] = None
    repeated_password: Optional[str] = None
    roles: Optional[List[str]] = None
    
    
class PublishConfiguration(BaseModel):
    """com.sos.joc.model.publish.Configuration"""
    
    commit_id: Optional[str] = None
    object_type: CommonConfigurationType
    path: str
    """absolute path of an object."""

    recursive: Optional[bool] = None


class OK(BaseModel):
    """com.sos.joc.model.common.Ok"""
    
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    ok: Optional[bool] = None
    survey_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""
    
    
class Timespan(BaseModel):
    """com.sos.joc.model.inventory.changes.common.Timespan"""

    from_: Optional[datetime] = None
    """ISO datetime yyyy-mm-dd HH:MM[:SS]"""

    to: Optional[datetime] = None
    """ISO datetime yyyy-mm-dd HH:MM[:SS]"""

    @field_serializer("from_", "to", when_used="json")
    def serialize_timespan(self, value: Optional[datetime]):
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")
    

class ChangeState(str, Enum):
    """com.sos.joc.model.inventory.changes.common.ChangeState"""
    
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    PUBLISHED = "PUBLISHED"


class ChangeItem(BaseModel):
    """com.sos.joc.model.inventory.changes.common.ChangeItem"""
    
    deployed: Optional[bool] = None
    name: Optional[str] = None
    object_type: Optional[CommonConfigurationType] = None
    path: Optional[str] = None
    """absolute path of an object."""

    released: Optional[bool] = None
    valid: Optional[bool] = None


class ChangeIdentifier(BaseModel):
    """com.sos.joc.model.inventory.changes.common.ChangeIdentifier"""
    
    name: Optional[str] = None
    state: Optional[ChangeState] = None
    title: Optional[str] = None
    

class Change(ChangeIdentifier):
    """com.sos.joc.model.inventory.changes.common.Change"""

    closed: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    configurations: Optional[List[ChangeItem]] = None
    created: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    last_published_by: Optional[str] = None
    modified: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    owner: Optional[str] = None


class CommonRequestFilter(BaseModel):
    """com.sos.joc.model.inventory.common.RequestFilter"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    id: Optional[float] = None
    object_type: Optional[CommonConfigurationType] = None
    path: Optional[str] = None
    
    
class Releasable(BaseModel):
    """com.sos.joc.model.inventory.release.Releasable"""
    
    object_type: Optional[CommonConfigurationType] = None
    path: Optional[str] = None
    

class SyncState(BaseModel):
    """com.sos.controller.model.common.SyncState"""
    
    text: Optional[SyncStateText] = None
    """SUSPENDED, OUTSTANDING only for Workflows"""

    severity: Optional[int] = None


class ResponseItemDeployment(BaseModel):
    """com.sos.joc.model.inventory.common.ResponseItemDeployment"""
    
    controller_id: Optional[str] = None
    deployment_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    deployment_id: Optional[float] = None
    path: Optional[str] = None
    """absolute path of an object."""

    version: Optional[str] = None
    

class ResponseDeployableVersion(BaseModel):
    """com.sos.joc.model.inventory.deploy.ResponseDeployableVersion"""
    
    commit_id: Optional[str] = None
    deployment_id: Optional[float] = None
    deployment_operation: Optional[str] = None
    deployment_path: Optional[str] = None
    """absolute path of an object."""

    id: Optional[float] = None
    version_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    versions: Optional[List[ResponseItemDeployment]] = None


class ReportItem(BaseModel):
    """com.sos.joc.model.inventory.validate.ReportItem"""
    
    error: Optional[Err] = None
    invalid_msg: Optional[str] = None
    name: Optional[str] = None
    object_type: Optional[CommonConfigurationType] = None
    path: Optional[str] = None
    """absolute path of an object."""

    title: Optional[str] = None
    valid: Optional[bool] = None


class RequestItem(BaseModel):
    """com.sos.joc.model.inventory.dependencies.RequestItem"""
    
    name: Optional[str] = None
    type: Optional[str] = None


class OperationType(str, Enum):
    """com.sos.joc.model.inventory.dependencies.get.OperationType"""
    
    DEPLOY = "DEPLOY"
    EXPORT = "EXPORT"
    GIT = "GIT"
    RECALL = "RECALL"
    RELEASE = "RELEASE"
    REMOVE = "REMOVE"
    REVOKE = "REVOKE"


class ArchiveFormat(str, Enum):
    """com.sos.joc.model.publish.ArchiveFormat"""
    
    TAR_GZ = "TAR_GZ"
    ZIP = "ZIP"


class Config(BaseModel):
    """com.sos.joc.model.publish.Config"""
    
    configuration: PublishConfiguration
    

class DeployablesValidFilter(BaseModel):
    """com.sos.joc.model.publish.DeployablesValidFilter"""
    
    deploy_configurations: Optional[List[Config]] = None
    draft_configurations: Optional[List[Config]] = None
    
    @model_validator(mode="after")
    def any_of(self) -> Self:
        if not (self.draft_configurations or self.deploy_configurations):
            raise ValueError("At least one of 'draftConfigurations' or 'deployConfigurations' must be set")
        return self
    

class ExportForSigning(BaseModel):
    """com.sos.joc.model.publish.ExportForSigning"""
    
    controller_id: str
    deployables: DeployablesValidFilter


class DeployablesFilter(BaseModel):
    """com.sos.joc.model.publish.DeployablesFilter"""
    
    draft_configurations: Optional[List[Config]] = None
    deploy_configurations: Optional[List[Config]] = None
    without_invalid: Optional[bool] = False


class ReleasablesFilter(BaseModel):
    """com.sos.joc.model.publish.ReleasablesFilter"""
    
    draft_configurations: Optional[List[Config]] = None
    released_configurations: Optional[List[Config]] = None
    without_invalid: Optional[bool] = False


class ExportShallowCopy(BaseModel):
    """com.sos.joc.model.publish.ExportShallowCopy"""
    
    deployables: Optional[DeployablesFilter] = None
    releasables: Optional[ReleasablesFilter] = None
    incl_all_tags: Optional[bool] = False


class ExportFile(BaseModel):
    """com.sos.joc.model.publish.ExportFile"""
    
    filename: Optional[str] = None
    format: Optional[ArchiveFormat] = None


class AdminAccounts(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.admin.Accounts"""
    manage: Optional[bool] = None
    view: Optional[bool] = None


class DailyPlanPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.DailyPlan"""
    
    manage: Optional[bool] = None
    """create daily plan, delete submissions"""

    view: Optional[bool] = None
    """show tab, planned orders, history"""


class AdminSettings(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.admin.Settings"""
    
    manage: Optional[bool] = None
    view: Optional[bool] = None
    

class AdminControllers(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.admin.Controllers"""
    
    manage: Optional[bool] = None
    view: Optional[bool] = None
    

class AdminCertificates(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.admin.Certificates"""
    
    manage: Optional[bool] = None
    view: Optional[bool] = None
    

class AdminCustomization(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.admin.Customization"""
    
    manage: Optional[bool] = None
    share: Optional[bool] = None
    """share/makePrvate"""

    view: Optional[bool] = None
    

class AdministrationPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.Administration"""
    accounts: Optional[AdminAccounts] = None
    certificates: Optional[AdminCertificates] = None
    controllers: Optional[AdminControllers] = None
    customization: Optional[AdminCustomization] = None
    settings: Optional[AdminSettings] = None


class CalendarsPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.Calendars"""
    
    view: Optional[bool] = None
    

class ClusterPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.Cluster"""
    
    manage: Optional[bool] = None
    

class DocumentationsPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.Documentations"""
    
    manage: Optional[bool] = None
    view: Optional[bool] = None
    """show/export"""


class FileTransferPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.FileTransfer"""
    
    manage: Optional[bool] = None
    view: Optional[bool] = None
    """show history, configuration tab"""


class InventoryPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.Inventory"""
    
    deploy: Optional[bool] = None
    """publishing depoyables and releasables"""

    manage: Optional[bool] = None
    """edit/restore/assign documentation"""

    view: Optional[bool] = None
    

class NotificationPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.Notification"""
    
    manage: Optional[bool] = None
    view: Optional[bool] = None
    """configuration tab"""
    

class OthersPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.Others"""
    
    manage: Optional[bool] = None
    view: Optional[bool] = None
    """configuration tab"""


class AuditLogPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.joc.AuditLog"""
    
    view: Optional[bool] = None
    

class JocPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.JocPermissions"""
    
    administration: Optional[AdministrationPermissions] = None
    audit_log: Optional[AuditLogPermissions] = None
    calendars: Optional[CalendarsPermissions] = None
    cluster: Optional[ClusterPermissions] = None
    daily_plan: Optional[DailyPlanPermissions] = None
    documentations: Optional[DocumentationsPermissions] = None
    file_transfer: Optional[FileTransferPermissions] = None
    get_log: Optional[bool] = None
    inventory: Optional[InventoryPermissions] = None
    notification: Optional[NotificationPermissions] = None
    others: Optional[OthersPermissions] = None
    

class Agents(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.controller.Agents"""
    
    view: Optional[bool] = None
    """show resource tab 'agents'"""
    

class Deployments(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.controller.Deployments"""
    
    deploy: Optional[bool] = None
    """add/update/remove releasable and deployable objects"""

    view: Optional[bool] = None
    """show deployment history"""
    

class Locks(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.controller.Locks"""
    
    view: Optional[bool] = None
    """show resource tab 'locks'"""
    

class NoticeBoards(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.controller.NoticeBoards"""
    delete: Optional[bool] = None
    """delete notice"""

    post: Optional[bool] = None
    """post notice"""

    view: Optional[bool] = None
    """show resource tab 'notice boards'"""
    

class Orders(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.controller.Orders"""
    
    cancel: Optional[bool] = None
    create: Optional[bool] = None
    """add, generate, submit"""

    manage_positions: Optional[bool] = None
    """skip, unskip, stop, unstop workflow jobs and add/modify order with special
    start-/endposition
    """
    modify: Optional[bool] = None
    suspend_resume: Optional[bool] = None
    """suspend, resume"""

    view: Optional[bool] = None
    """show order/task widget, overview, order/task history"""
    

class PermissionWorkflows(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.controller.Workflows"""
    
    view: Optional[bool] = None
    """show tab"""
    

class ControllerPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.ControllerPermissions"""
    
    agents: Optional[Agents] = None
    deployments: Optional[Deployments] = None
    get_log: Optional[bool] = None
    locks: Optional[Locks] = None
    notice_boards: Optional[NoticeBoards] = None
    orders: Optional[Orders] = None
    restart: Optional[bool] = None
    switch_over: Optional[bool] = None
    terminate: Optional[bool] = None
    view: Optional[bool] = None
    workflows: Optional[PermissionWorkflows] = None
    

class ControllerAgents(BaseModel):
    view: Optional[bool] = None
    """show resource tab 'agents'"""


class ControllerDeployments(BaseModel):
    deploy: Optional[bool] = None
    """add/update/remove releasable and deployable objects"""

    view: Optional[bool] = None
    """show deployment history"""


class ControllerLocks(BaseModel):
    view: Optional[bool] = None
    """show resource tab 'locks'"""


class ControllerNoticeBoards(BaseModel):
    delete: Optional[bool] = None
    """delete notice"""

    post: Optional[bool] = None
    """post notice"""

    view: Optional[bool] = None
    """show resource tab 'notice boards'"""


class ControllerOrders(BaseModel):
    cancel: Optional[bool] = None
    create: Optional[bool] = None
    """add, generate, submit"""

    manage_positions: Optional[bool] = None
    """skip, unskip, stop, unstop workflow jobs and add/modify order with special
    start-/endposition
    """
    modify: Optional[bool] = None
    suspend_resume: Optional[bool] = None
    """suspend, resume"""

    view: Optional[bool] = None
    """show order/task widget, overview, order/task history"""


class ControllerWorkflows(BaseModel):
    view: Optional[bool] = None
    """show tab"""
    

class Controller(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.Controllers"""
    
    agents: Optional[ControllerAgents] = None
    deployments: Optional[ControllerDeployments] = None
    get_log: Optional[bool] = None
    locks: Optional[ControllerLocks] = None
    notice_boards: Optional[ControllerNoticeBoards] = None
    orders: Optional[ControllerOrders] = None
    restart: Optional[bool] = None
    switch_over: Optional[bool] = None
    terminate: Optional[bool] = None
    view: Optional[bool] = None
    workflows: Optional[ControllerWorkflows] = None
    

#############
#   JOC     #
#############
class Authentication(BaseModel):
    access_token: Optional[str] = None
    account: Optional[str] = None
    caller_host_name: Optional[str] = None
    caller_ip_address: Optional[str] = None
    enable_touch: Optional[bool] = None
    force_password_change: Optional[bool] = None
    has_role: Optional[bool] = None
    identity_service: Optional[str] = None
    is_approval_requestor: Optional[bool] = None
    is_approver: Optional[bool] = None
    is_authenticated: Optional[bool] = None
    is_permitted: Optional[bool] = None
    message: Optional[str] = None
    role: Optional[str] = None
    session_timeout: Optional[int] = None


class SecurityConfiguration(BaseModel):
    """com.sos.joc.model.security.configuration.SecurityConfiguration"""
    
    identity_service_name: Optional[str] = None
    accounts: Optional[List[SecurityConfigurationAccount]] = None
    audit_log: Optional[AuditParams] = None
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    main: Optional[List[SecurityConfigurationMainEntry]] = None
    profiles: Optional[List[Profile]] = None
    roles: Optional[Dict[str, SecurityConfigurationRole]] = None


class Validate(BaseModel):
    """com.sos.joc.model.inventory.Validate"""
    
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    invalid_msg: Optional[str] = None
    valid: Optional[bool] = None


class DeployFilter(BaseModel):
    """com.sos.joc.model.publish.DeployFilter"""
    
    add_orders_date_from: Optional[datetime] = None
    audit_log: Optional[AuditParams] = None
    controller_ids: List[str]
    delete: Optional[DeployablesValidFilter] = None
    include_late: Optional[bool] = None
    store: Optional[DeployablesValidFilter] = None
    
    @model_validator(mode="after")
    def validate_any_of(self):
        if not (self.store or self.delete):
            raise ValueError("At least one of 'store' or 'delete' must be provided.")
        return self


class ShowChangesResponse(BaseModel):
    """com.sos.joc.model.inventory.changes.ShowChangesResponse"""
    
    changes: Optional[List[Change]] = None
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""


class ShowChangesFilter(BaseModel):
    """com.sos.joc.model.inventory.changes.ShowChangesFilter"""
    
    closed: Optional[Timespan] = None
    created: Optional[Timespan] = None
    details: Optional[bool] = True
    last_published_by: Optional[str] = None
    modified: Optional[Timespan] = None
    names: Optional[List[str]] = None
    owner: Optional[str] = None
    states: Optional[List[ChangeState]] = None


class RevokeFilter(BaseModel):
    """com.sos.joc.model.publish.RevokeFilter"""
    
    audit_log: Optional[AuditParams] = None
    cancel_orders_date_from: Optional[datetime] = None
    controller_ids: List[str]
    deploy_configurations: List[Config]


class ReleaseFilter(BaseModel):
    """com.sos.joc.model.inventory.release.ReleaseFilter"""
    
    add_orders_date_from: Optional[date] = None
    audit_log: Optional[AuditParams] = None
    delete: Optional[List[CommonRequestFilter]] = None
    include_late: Optional[bool] = None
    update: Optional[List[CommonRequestFilter]] = None

    @model_validator(mode="after")
    def validate_any_of(self):
        if not (self.update or self.delete):
            raise ValueError("At least one of 'update' or 'delete' must be provided.")
        return self


class ReleasableRecallFilter(BaseModel):
    """com.sos.joc.model.inventory.release.ReleasableRecallFilter"""
    
    audit_log: Optional[AuditParams] = None
    releasables: Optional[List[Releasable]] = None


class CommonRequestFolder(BaseModel):
    """com.sos.joc.model.inventory.common.RequestFolder"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    object_types: Optional[List[CommonConfigurationType]] = None
    only_valid_objects: Optional[bool] = None
    path: Optional[str] = None
    """absolute path of an object."""

    recursive: Optional[bool] = None
    

class ValidateRequestFolder(BaseModel):
    """com.sos.joc.model.inventory.validate.RequestFolder"""
    
    audit_log: Optional[AuditParams] = None
    path: Optional[str] = None
    """absolute path of an object."""

    recursive: Optional[bool] = None


class ConfigurationObject(BaseModel):
    """com.sos.joc.model.inventory.ConfigurationObject"""
    
    audit_log: Optional[AuditParams] = None
    configuration: Optional[Dict[str, Any]] = None
    """interface for different json representations of a configuration item"""

    configuration_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    deleted: Optional[bool] = None
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    deployed: Optional[bool] = None
    deployments: Optional[List[ResponseDeployableVersion]] = None
    has_deployments: Optional[bool] = None
    has_note: Optional[Severity] = None
    has_releases: Optional[bool] = None
    id: Optional[float] = None
    invalid_msg: Optional[str] = None
    is_referenced_by: Optional[Dict[str, int]] = None
    name: Optional[str] = None
    object_type: Optional[CommonConfigurationType] = None
    path: Optional[str] = None
    """absolute path of an object."""

    released: Optional[bool] = None
    state: Optional[ItemStateEnum] = None
    sync_state: Optional[SyncState] = None
    valid: Optional[bool] = None


class Report(BaseModel):
    """com.sos.joc.model.inventory.validate.Report"""
    
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    erroneous_objs: Optional[List[ReportItem]] = None
    invalid_objs: Optional[List[ReportItem]] = None
    valid_objs: Optional[List[ReportItem]] = None


class RequestFilters(BaseModel):
    """com.sos.joc.model.inventory.delete.RequestFilters"""
    cancel_orders_date_from: Optional[datetime] = None
    objects: List[CommonRequestFilter]
    audit_log: Optional[AuditParams] = None


class RequestFolder(BaseModel):
    """com.sos.joc.model.inventory.delete.RequestFolder"""
    cancel_orders_date_from: Optional[datetime] = None
    controller_id: Optional[str] = None
    path: str
    recursive: bool = False
    object_types: Optional[List[CommonConfigurationType]] = None
    only_valid_objects: bool = False
    audit_log: Optional[AuditParams] = None


class CommonRequestFilters(BaseModel):
    """com.sos.joc.model.inventory.common.RequestFilters"""
    
    audit_log: Optional[AuditParams] = None
    objects: Optional[List[CommonRequestFilter]] = None
    

class RestoreRequestFilter(CommonRequestFilters):
    """com.sos.joc.model.inventory.restore.RequestFilter"""
    
    # Target path / Renaming
    new_path: Optional[str] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None

    # Identifikation
    id: Optional[int] = None
    path: Optional[str] = None
    object_type: Optional[CommonConfigurationType] = None

    @model_validator(mode="after")
    def validate_selector(self):
        has_id = self.id is not None
        has_path = self.path is not None
        has_type = self.object_type is not None

        if has_id:
            # id must not be combined with path/objectType
            if has_path or has_type:
                raise ValueError("Use either 'id' OR ('path' + 'object_type'), not both")
            return self

        # no id → path + object_type required
        if not (has_path and has_type):
            raise ValueError("Either 'id' or both 'path' and 'object_type' are required")

        return self


class ResponseNewPath(BaseModel):
    """
    com.sos.joc.model.inventory.common.ResponseNewPath\n
    response of copy, rename, restore
    """

    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    id: Optional[float] = None
    object_type: Optional[CommonConfigurationType] = None
    path: Optional[str] = None


class Version(BaseModel):
    """com.sos.joc.model.Version"""
    
    date: Optional[str] = None
    git_hash: Optional[str] = None
    version: Optional[str] = None


class GetDependenciesRequest(BaseModel):
    """com.sos.joc.model.inventory.dependencies.GetDependenciesRequest"""
    
    configurations: Optional[List[RequestItem]] = None
    operation_type: Optional[OperationType] = None


class ResponseObject(ConfigurationObject):
    """com.sos.joc.model.inventory.dependencies.get.ResponseObject"""
    
    enforced_referenced_by: Optional[List[float]] = None
    enforced_references: Optional[List[float]] = None
    referenced_by: Optional[List[float]] = None
    references: Optional[List[float]] = None


class GetDependenciesResponse(BaseModel):
    """com.sos.joc.model.inventory.dependencies.get.Response"""
    
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    objects: Optional[Dict[str, ResponseObject]] = None
    requested_items: Optional[List[float]] = None


class ExportFilter(BaseModel):
    """com.sos.joc.model.publish.ExportFilter"""
    
    audit_log: Optional[AuditParams] = None
    export_file: Optional[ExportFile] = None
    for_signing: Optional[ExportForSigning] = None
    shallow_copy: Optional[ExportShallowCopy] = None
    start_folder: Optional[str] = None
    use_short_path: Optional[bool] = False

    @model_validator(mode="after")
    def validate_one_of(self):
        has_for_signing = self.for_signing is not None
        has_shallow_copy = self.shallow_copy is not None

        if self.export_file is None:
            raise ValueError("export_file is required")

        if has_for_signing == has_shallow_copy:
            raise ValueError("Exactly one of 'for_signing' or 'shallow_copy' must be set")

        return self


class ShallowCopy(BaseModel):
    """com.sos.joc.model.publish.folder.ExportFolderShallowCopy"""
    
    folders: List[str]
    object_types: List[CommonConfigurationType]
    incl_all_tags: Optional[bool] = False
    only_valid_objects: Optional[bool] = False
    recursive: Optional[bool] = False
    without_deployed: Optional[bool] = False
    without_drafts: Optional[bool] = False
    without_released: Optional[bool] = False
    


class ExportFolderForSigning(BaseModel):
    """com.sos.joc.model.publish.folder.ExportFolderForSigning"""
    
    controller_id: str
    folders: List[str]
    object_types: List[CommonConfigurationType]
    recursive: Optional[bool] = False
    without_deployed: Optional[bool] = False
    without_drafts: Optional[bool] = False



class ExportFolderFilter(BaseModel):
    """com.sos.joc.model.publish.folder.ExportFolderFilter"""
    
    audit_log: Optional[AuditParams] = None
    export_file: ExportFile
    for_signing: Optional[ExportFolderForSigning] = None
    shallow_copy: Optional[ShallowCopy] = None
    use_short_path: Optional[bool] = None

    @model_validator(mode="after")
    def validate_one_of(self) -> Self:
        has_for_signing = self.for_signing is not None
        has_shallow_copy = self.shallow_copy is not None

        if has_for_signing == has_shallow_copy:
            raise ValueError("Exactly one of 'forSigning' or 'shallowCopy' must be set")

        return self


class Permissions(BaseModel):
    """com.sos.joc.model.security.permissions.Permissions"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: str
    identity_service_name: str
    permissions: List[Permission]
    role_name: str
    

class AccountListFilter(BaseModel):
    """com.sos.joc.model.security.accounts.AccountListFilter"""
    
    account_name: Optional[str] = None
    disabled: Optional[bool] = None
    enabled: Optional[bool] = None
    identity_service_name: str


class Account(BaseModel):
    """com.sos.joc.model.security.accounts.Account"""
    
    account_name: str
    audit_log: Optional[AuditParams] = None
    disabled: Optional[bool] = None
    """controls if the object is disabled"""

    force_password_change: Optional[bool] = None
    """controls if the account is forced to change the password"""

    identity_service_name: str
    password: Optional[str] = None
    roles: Optional[List[str]] = None


class Accounts(BaseModel):
    """com.sos.joc.model.security.accounts.Accounts"""
    
    account_items: Optional[List[Account]] = None
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    identity_service_name: Optional[str] = None
    
    
class BlockedAccountsFilter(BaseModel):
    """com.sos.joc.model.security.blocklist.BlockedAccountsFilter"""
    
    account_name: Optional[str] = None
    date_from: Optional[datetime] = None
    """ISO 8601 datetime"""

    date_to: Optional[datetime] = None
    """ISO 8601 datetime"""

    limit: Optional[int] = None
    """restricts the number of responsed records; -1=unlimited"""

    time_zone: Optional[str] = None
    

class BlockedAccount(BaseModel):
    """com.sos.joc.model.security.blocklist.BlockedAccount"""
    
    account_name: str
    audit_log: Optional[AuditParams] = None
    comment: Optional[str] = None
    since: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""


class BlockedAccounts(BaseModel):
    """com.sos.joc.model.security.blocklist.BlockedAccounts"""
    
    blocked_accounts: Optional[List[BlockedAccount]] = None
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""
    

class AccountRename(BaseModel):
    """com.sos.joc.model.security.accounts.AccountRename"""
    
    account_new_name: str
    account_old_name: str
    audit_log: Optional[AuditParams] = None
    identity_service_name: str
    
    
class AccountsFilter(BaseModel):
    """com.sos.joc.model.security.accounts.AccountsFilter"""
    
    account_names: List[str]
    audit_log: Optional[AuditParams] = None
    disabled: Optional[bool] = None
    enabled: Optional[bool] = None
    identity_service_name: str
    
    
class AccountFilter(BaseModel):
    """com.sos.joc.model.security.accounts.AccountFilter"""
    
    account_name: str
    audit_log: Optional[AuditParams] = None
    identity_service_name: str
    

class ConfigurationPermissions(BaseModel):
    """com.sos.joc.model.security.configuration.permissions.Permissions"""
    
    controller_defaults: Optional[ControllerPermissions] = None
    controllers: Optional[Dict[str, Controller]] = None
    joc: Optional[JocPermissions] = None
    roles: Optional[List[str]] = None
    
    
class AccountChangePassword(BaseModel):
    """com.sos.joc.model.security.accounts.AccountChangePassword"""
    
    account_name: str
    audit_log: Optional[AuditParams] = None
    force_password_change: Optional[bool] = None
    """controls if the account is forced to change the password"""

    identity_service_name: str
    old_password: Optional[str] = None
    password: Optional[str] = None
    repeated_password: Optional[str] = None
    
    
class AccountNamesFilter(BaseModel):
    """com.sos.joc.model.security.accounts.AccountNamesFilter"""
    
    account_names: List[str]
    audit_log: Optional[AuditParams] = None
    identity_service_name: str
    
    
class BlockedAccountsDeleteFilter(BaseModel):
    """com.sos.joc.model.security.blocklist.BlockedAccountsDeleteFilter"""
    
    account_names: List[str]
    audit_log: Optional[AuditParams] = None
    
    
class RoleFilter(BaseModel):
    """com.sos.joc.model.security.roles.RoleFilter"""
    
    audit_log: Optional[AuditParams] = None
    identity_service_name: str
    role_name: str
    
    
class Role(BaseModel):
    """com.sos.joc.model.security.roles.Role"""
    
    audit_log: Optional[AuditParams] = None
    controllers: Optional[List[str]] = None
    identity_service_name: Optional[str] = None
    ordering: Optional[int] = None
    role_name: Optional[str] = None
    
    
class RoleListFilter(BaseModel):
    """com.sos.joc.model.security.roles.RoleListFilter"""
    
    identity_service_name: str
    
    
class Roles(BaseModel):
    """com.sos.joc.model.security.roles.Roles"""
    
    identity_service_name: Optional[str] = None
    roles: Optional[List[Role]] = None
    
    
class RoleStore(BaseModel):
    """com.sos.joc.model.security.roles.RoleStore"""
    
    audit_log: Optional[AuditParams] = None
    identity_service_name: str
    ordering: Optional[int] = None
    role_name: str
    
    
class RoleRename(BaseModel):
    """com.sos.joc.model.security.roles.RoleRename"""
    
    audit_log: Optional[AuditParams] = None
    identity_service_name: str
    role_new_name: str
    role_old_name: str
    
    
class RolesFilter(BaseModel):
    """com.sos.joc.model.security.roles.RolesFilter"""
    
    audit_log: Optional[AuditParams] = None
    identity_service_name: str
    role_names: List[str]
    
    
class PermissionFilter(BaseModel):
    """com.sos.joc.model.security.permissions.PermissionFilter"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    identity_service_name: str
    permission_path: str
    role_name: str


class PermissionItem(BaseModel):
    """com.sos.joc.model.security.permissions.PermissionItem"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    identity_service_name: Optional[str] = None
    permission: Optional[Permission] = None
    role_name: Optional[str] = None
    
    
class PermissionListFilter(BaseModel):
    """com.sos.joc.model.security.permissions.PermissionListFilter"""
    
    controller_id: Optional[str] = None
    identity_service_name: str
    role_name: str


class PermissionRename(BaseModel):
    """com.sos.joc.model.security.permissions.PermissionRename"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: str
    identity_service_name: str
    new_permission: Permission
    old_permission_path: str
    role_name: str
    
    
class PermissionsFilter(BaseModel):
    """com.sos.joc.model.security.permissions.PermissionsFilter"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    identity_service_name: str
    permission_paths: List[str]
    role_name: str
    
    
class FolderFilter(BaseModel):
    """com.sos.joc.model.security.folders.FolderFilter"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: str
    folder_name: str
    identity_service_name: str
    role_name: str


class FolderItem(BaseModel):
    """com.sos.joc.model.security.folders.FolderItem"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    folder: Optional[Folder] = None
    identity_service_name: Optional[str] = None
    role_name: Optional[str] = None
    
    
class FolderListFilter(BaseModel):
    """com.sos.joc.model.security.folders.FolderListFilter"""
    
    controller_id: Optional[str] = None
    identity_service_name: str
    role_name: str
    
    
class Folders(BaseModel):
    """com.sos.joc.model.security.folders.Folders"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: str
    folders: List[Folder]
    identity_service_name: str
    role_name: str
    
    
class FolderRename(BaseModel):
    """com.sos.joc.model.security.folders.FolderRename"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: str
    identity_service_name: str
    new_folder: Folder
    old_folder_name: str
    role_name: str
    
    
class FoldersFilter(BaseModel):
    """com.sos.joc.model.security.permissions.FoldersFilter"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    folder_names: List[str]
    identity_service_name: str
    role_name: str
    

class IdentityServiceFilter(BaseModel):
    """com.sos.joc.model.security.identityservice.IdentityServiceFilter"""
    
    audit_log: Optional[AuditParams] = None
    identity_service_name: Optional[str] = None
    

class IdentityService(BaseModel):
    """com.sos.joc.model.security.identityservice.IdentityService"""
    
    audit_log: Optional[AuditParams] = None
    disabled: Optional[bool] = None
    """controls if the object is disabled"""

    identity_service_name: str
    identity_service_type: Optional[IdentityServiceType] = None
    ordering: Optional[int] = None
    required: Optional[bool] = None
    """controls if the identity service is required"""

    second_factor: Optional[bool] = None
    """Identity Service is used as a second factor"""

    second_factor_identity_service_name: Optional[str] = None
    service_authentication_scheme: ServiceAuthenticationScheme
    
    
class IdentityServices(BaseModel):
    """com.sos.joc.model.security.identityservice.IdentityServices"""
    
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    identity_service_items: Optional[List[IdentityService]] = None
    identity_service_types: Optional[List[IdentityServiceType]] = None
    
    
class IdentityServiceRename(BaseModel):
    """com.sos.joc.model.security.identityservice.IdentityServiceRename"""
    
    audit_log: Optional[AuditParams] = None
    identity_service_new_name: str
    identity_service_old_name: str


class ReadFromFilter(BaseModel):
    """com.sos.joc.model.publish.repository.ReadFromFilter"""
    
    category: Category
    folder: str
    """absolute path of an object."""

    recursive: Optional[bool] = None
    
    
class ResponseFolderItem(BaseModel):
    """com.sos.joc.model.publish.repository.ResponseFolderItem"""
    
    folder: Optional[str] = None
    """absolute path of an object."""

    last_modified: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    object_name: Optional[str] = None
    object_type: Optional[CommonConfigurationType] = None


class ResponseFolder(BaseModel):
    """com.sos.joc.model.publish.repository.ResponseFolder"""
    
    folders: Optional[List[Any]] = None
    items: Optional[List[ResponseFolderItem]] = None
    last_modified: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    name: Optional[str] = None
    path: Optional[str] = None
    """absolute path of an object."""
    
    
class UpdateFromFilter(BaseModel):
    """com.sos.joc.model.publish.repository.UpdateFromFilter"""
    
    audit_log: Optional[AuditParams] = None
    category: Category
    configurations: List[Config]


class Configurations(BaseModel):
    """com.sos.joc.model.publish.repository.Configurations"""
    
    deploy_configurations: Optional[List[Config]] = None
    draft_configurations: Optional[List[Config]] = None
    released_configurations: Optional[List[Config]] = None
    
    @model_validator(mode="after")
    def validate_any_of(self):
        if (
            not self.deploy_configurations 
            and not self.draft_configurations 
            and not self.released_configurations
        ):
            raise ValueError(
                "At least one of the following parameters must not be None: "
                "deploy_configurations, draft_configurations, released_configurations."
            )
        return self

    
class CopyToFilter(BaseModel):
    """com.sos.joc.model.publish.repository.CopyToFilter"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    local: Optional[Configurations] = None
    rollout: Optional[Configurations] = None
    
    @model_validator(mode="after")
    def validate_one_of(self):
        if (self.local and self.rollout) or (not self.local and not self.rollout):
            raise ValueError("Exactly one of 'local' or 'rollout' must be set.")
        return self


class PublishConfig(BaseModel):
    """com.sos.joc.model.publish.Config"""
    
    configuration: Optional[PublishConfiguration] = None


class DeleteFromFilter(BaseModel):
    """com.sos.joc.model.publish.repository.DeleteFromFilter"""
    
    audit_log: Optional[AuditParams] = None
    category: Category
    configurations: List[PublishConfig]
    

class CheckoutFilter(BaseModel):
    """com.sos.joc.model.publish.git.commands.CheckoutFilter"""
    
    audit_log: Optional[AuditParams] = None
    branch: Optional[str] = None
    category: Optional[Category] = None
    folder: Optional[str] = None
    tag: Optional[str] = None
    
    @model_validator(mode="after")
    def validate_one_of(self):
        branch_set = all([self.branch, self.folder, self.category])
        tag_set = all([self.tag, self.folder, self.category])
        
        if (branch_set and tag_set) or (not branch_set and not tag_set):
            raise ValueError(
                "One of the following parameter sets must be provided: "
                "(branch, folder, category) or (tag, folder, category)."
            )
            
        return self
    
    
class GitCommandResponse(BaseModel):
    """com.sos.joc.model.publish.git.commands.GitCommandResponse"""
    
    command: Optional[str] = None
    exit_code: Optional[int] = None
    std_err: Optional[str] = None
    std_out: Optional[str] = None
    
    
class CloneFilter(BaseModel):
    """com.sos.joc.model.publish.git.commands.CloneFilter"""
    
    audit_log: Optional[AuditParams] = None
    category: Category
    folder: str
    remote_url: str
    """Git Remote URL"""
    
    
class CommonFilter(BaseModel):
    """com.sos.joc.model.publish.git.commands.CommonFilter"""
    
    audit_log: Optional[AuditParams] = None
    category: Category
    folder: str
    
    
class CommitFilter(BaseModel):
    """com.sos.joc.model.publish.git.commands.CommitFilter"""
    
    audit_log: Optional[AuditParams] = None
    category: Category
    folder: str
    message: Optional[str] = None
    
    
class GitCredentials(BaseModel):
    """com.sos.joc.model.publish.git.GitCredentials"""
    
    email: Optional[str] = None
    git_account: Optional[str] = None
    git_server: Optional[str] = None
    keyfile_path: Optional[str] = None
    """path or filename of a private Key. Empty filename possible."""

    password: Optional[str] = None
    personal_access_token: Optional[str] = None
    username: Optional[str] = None
    

class RemoveCredentialsFilter(BaseModel):
    """com.sos.joc.model.publish.git.RemoveCredentialsFilter"""
    
    audit_log: Optional[AuditParams] = None
    git_servers: List[str]
    
    
class AddCredentialsFilter(BaseModel):
    """com.sos.joc.model.publish.git.AddCredentialsFilter"""
    
    audit_log: Optional[AuditParams] = None
    credentials: List[GitCredentials]
    

class WorkflowID(BaseModel):
    """com.sos.controller.model.workflow.WorkflowId"""
    
    path: Optional[str] = None
    version_id: Optional[str] = None
    
    
class ModifyOrdersBase(BaseModel):
    """com.sos.joc.model.order.ModifyOrdersBase"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: str
    folders: Optional[List[Folder]] = None
    order_ids: Optional[List[str]] = None
    states: Optional[List[OrderStateText]] = None
    workflow_ids: Optional[List[WorkflowID]] = None
    
    @model_validator(mode="after")
    def validate_order_ids(self):
        if not self.order_ids:
            return self
        
        ignored_params: List[Any] = [self.workflow_ids, self.folders, self.states]
        
        if sum(value is not None for value in ignored_params) != 0:
            raise ValueError("The parameters 'workflow_ids', 'folders' and 'states' are ignored.")

        return self
    
    @model_validator(mode="after")
    def validate_workflow_ids(self):
        if not self.workflow_ids:
            return self
        
        if self.folders:
            raise ValueError("The parameter 'folders' are ignored.")
        
        return self
    

class CancelOrders(ModifyOrdersBase):
    """com.sos.joc.model.order.CancelOrders"""
    
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    time_zone: Optional[str] = None
    kill: Optional[bool] = None
    deep: Optional[bool] = None


class PlanID(BaseModel):
    """com.sos.joc.model.plan.PlanId"""
    
    notice_space_key: str
    plan_schema_id: str


class AddOrder(BaseModel):
    """com.sos.joc.model.order.AddOrder"""
    
    arguments: Optional[Dict[str, Any]] = None
    """a map for arbitrary key-value pairs"""

    block_position: Optional[Union[List[Union[int, str]], str]] = None
    end_positions: Optional[List[Union[List[Union[int, str]], str]]] = None
    force_job_admission: Optional[bool] = None
    open_closed_plan: Optional[bool] = None
    order_name: str
    plan_id: Optional[PlanID] = None
    priority: Optional[int] = None
    scheduled_for: Optional[str] = None
    """ISO format yyyy-mm-dd HH:MM[:SS] or now or now + HH:MM[:SS] or now + SECONDS or empty"""

    start_position: Optional[Union[List[Union[int, str]], str]] = None
    tags: Optional[List[str]] = None
    time_zone: Optional[str] = None
    """see https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"""

    workflow_path: str
    

class AddOrders(BaseModel):
    """com.sos.joc.model.order.AddOrders"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: str
    orders: List[AddOrder]
    
    
class OrderIDS(BaseModel):
    """com.sos.joc.model.order.OrderIds"""
    
    delivery_date: datetime
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    order_ids: Optional[List[str]] = None
    
    
class RequestFilter(BaseModel):
    """com.sos.joc.model.inventory.restore.RequestFilter"""
    
    new_path: Optional[str] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    id: Optional[str] = None
    path: Optional[str] = None
    object_type: Optional[CommonConfigurationType] = None
    audit_log: Optional[AuditParams] = None
    
    @model_validator(mode="after")
    def validate_identifier(self):
        has_id = self.id is not None
        has_path_and_type = self.path is not None and self.object_type is not None

        if not (has_id or has_path_and_type):
            raise ValueError(
                "Either 'id' must be provided, or both 'path' and 'object_type' must be set."
            )

        return self


class URLParameter(BaseModel):
    """com.sos.joc.model.controller.UrlParameter"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: str
    url: Optional[str] = None
    with_switchover: Optional[bool] = None


class ClusterNodeState(BaseModel):
    """com.sos.joc.model.controller.ClusterNodeState"""
    
    text: Optional[ClusterNodeStateText] = None
    severity: Optional[int] = None
    """0=active, 1=inactive, 3=unknown"""

class ComponentState(BaseModel):
    """com.sos.joc.model.controller.ComponentState"""
    
    text: Optional[ComponentStateText] = None
    severity: Optional[int] = None
    """0=operational, 1=limited, 2=inoperable, 3=unknown"""


class ConnectionState(BaseModel):
    """com.sos.joc.model.controller.ConnectionState"""
    
    text: Optional[ConnectionStateText] = Field(None, alias="_text")
    severity: Optional[int] = None
    """0=established, 1=unstable, 2=unreachable, 3=unknown"""


class OS(BaseModel):
    architecture: Optional[str] = None
    distribution: Optional[str] = None
    """e.g. Windows 2012, CentOS Linux release 7.2.1511 (Core)"""


class ControllerInfo(BaseModel):
    """com.sos.joc.model.controller.Controller"""
    
    cluster_node_state: Optional[ClusterNodeState] = None
    cluster_url: Optional[str] = None
    component_state: Optional[ComponentState] = None
    connection_state: Optional[ConnectionState] = None
    controller_id: Optional[str] = None
    host: Optional[str] = None
    id: Optional[float] = None
    is_coupled: Optional[bool] = None
    os: Optional[OS] = None
    role: Optional[ControllerRole] = None
    security_level: Optional[JocSecurityLevel] = None
    started_at: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    survey_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    title: Optional[str] = None
    url: Optional[str] = None
    version: Optional[str] = None

    
class JobScheduler200(BaseModel):
    """com.sos.joc.model.controller.JobScheduler200"""
    
    controller: Optional[ControllerInfo] = None
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""
    
    
class TestConnect(BaseModel):
    """com.sos.joc.model.controller.TestConnect"""
    
    controller_id: Optional[str] = None
    url: str


class RegisterParameter(BaseModel):
    """com.sos.joc.model.controller.RegisterParameter"""
    
    cluster_url: Optional[str] = None
    id: Optional[float] = None
    role: Optional[ControllerRole] = None
    title: Optional[str] = None
    url: Optional[str] = None


class RegisterParameters(BaseModel):
    """com.sos.joc.model.controller.RegisterParameters"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    controllers: Optional[List[RegisterParameter]] = None


class Agent(BaseModel):
    """com.sos.joc.model.agent.Agent"""
    
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    agent_name_aliases: Optional[List[str]] = None
    controller_id: Optional[str] = None
    deployed: Optional[bool] = None
    disabled: Optional[bool] = None
    hidden: Optional[bool] = None
    ordering: Optional[int] = None
    process_limit: Optional[int] = None
    sync_state: Optional[SyncState] = None
    title: Optional[str] = None
    url: Optional[str] = None
    version: Optional[str] = None

    
class StoreAgents(BaseModel):
    """com.sos.joc.model.agent.StoreAgents"""
    
    agents: Optional[List[Agent]] = None
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    update: Optional[bool] = None
    """if true than agents can only be updated"""


class Subagent(BaseModel):
    """com.sos.joc.model.agent.SubAgent"""
    
    agent_id: Optional[str] = None
    deployed: Optional[bool] = None
    disabled: Optional[bool] = None
    is_director: Optional[SubagentDirectorType] = None
    ordering: Optional[int] = None
    subagent_id: Optional[str] = None
    sync_state: Optional[SyncState] = None
    title: Optional[str] = None
    url: Optional[str] = None
    version: Optional[str] = None
    with_generate_subagent_cluster: Optional[bool] = None


class ClusterAgent(Agent):
    subagents: Optional[List[Subagent]] = None
    

class StoreClusterAgents(BaseModel):
    """com.sos.joc.model.agent.StoreClusterAgents"""
    
    audit_log: Optional[AuditParams] = None
    cluster_agents: Optional[List[ClusterAgent]] = None
    controller_id: Optional[str] = None
    update: Optional[bool] = None
    """if true than agents can only be updated"""
    
    
class StoreSubAgents(BaseModel):
    """com.sos.joc.model.agent.StoreSubAgents"""
    
    agent_id: Optional[str] = None
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    subagents: Optional[List[Subagent]] = None
    update: Optional[bool] = None
    """if true than agents can only be updated"""
    
    
class AgentCommand(BaseModel):
    """com.sos.joc.model.agent.AgentCommand"""
    
    agent_id: Optional[str] = None
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    force: Optional[bool] = None
    """only relevant for reset agent"""
    
    
class DeployAgents(BaseModel):
    """com.sos.joc.model.agent.DeployAgents"""
    
    agent_ids: Optional[List[str]] = None
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    
    
class DeployClusterAgents(BaseModel):
    """com.sos.joc.model.agent.DeployClusterAgents"""
    
    audit_log: Optional[AuditParams] = None
    cluster_agent_ids: Optional[List[str]] = None
    controller_id: Optional[str] = None
    
    
class SubAgentsCommand(BaseModel):
    """com.sos.joc.model.agent.SubAgentsCommand"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    subagent_ids: Optional[List[str]] = None


class SubagentID(BaseModel):
    """com.sos.joc.model.agent.SubAgentId"""
    
    priority: Optional[Union[int, str]] = None
    subagent_id: Optional[str] = None


class SubagentCluster(BaseModel):
    """com.sos.joc.model.agent.SubagentCluster"""
    
    agent_id: Optional[str] = None
    controller_id: Optional[str] = None
    deployed: Optional[bool] = None
    ordering: Optional[int] = None
    subagent_cluster_id: Optional[str] = None
    subagent_ids: Optional[List[SubagentID]] = None
    sync_state: Optional[SyncState] = None
    title: Optional[str] = None
    

class StoreSubagentClusters(BaseModel):
    """com.sos.joc.model.agent.StoreSubagentClusters"""
    
    audit_log: Optional[AuditParams] = None
    subagent_clusters: Optional[List[SubagentCluster]] = None
    update: Optional[bool] = None
    """if true than agents can only be updated"""
    
    
class DeploySubagentClusters(BaseModel):
    """com.sos.joc.model.agent.DeploySubagentClusters"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    subagent_cluster_ids: Optional[List[str]] = None
    
    
class OrdersFilterV(BaseModel):
    compact: Optional[bool] = None
    """controls if the object's data is compact or detailed"""

    limit: Optional[int] = None
    """-1=unlimited"""

    order_ids: Optional[List[str]] = None
    order_tags: Optional[List[str]] = None
    regex: Optional[str] = None
    """regular expression to filter Controller objects by matching the path"""

    state_date_from: Optional[Union[str, datetime]] = None
    """0 or [number][smhdwMy] (where smhdwMy unit for second, minute, etc) or ISO 8601 timestamp"""

    state_date_to: Optional[Union[str, datetime]] = None
    """0 or [number][smhdwMy] (where smhdwMy unit for second, minute, etc) or ISO 8601 timestamp"""

    states: Optional[List[OrderStateText]] = None
    without_workflow_tags: Optional[bool] = None
    """if true then response doesn't contain 'workflowsTagPerWorkflow'"""

    workflow_tags: Optional[List[str]] = None
    controller_id: str


class OrderAttachedState(BaseModel):
    """com.sos.controller.model.order.OrderAttachedState"""

    agentName: Optional[str] = None
    TYPE: Optional[str] = None
    """Attaching, Attached, ..."""
    

class OrderCycleState(BaseModel):
    """com.sos.controller.model.order.OrderCycleState"""

    index: Optional[int] = None
    next: Optional[datetime] = None
    since: Optional[datetime] = None
    
    
class CyclicOrderInfos(BaseModel):
    """com.sos.joc.model.dailyplan.CyclicOrderInfos"""

    count: Optional[int] = None
    first_order_id: Optional[str] = None
    first_start: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    last_order_id: Optional[str] = None
    last_start: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""
    
    
class ExpectedNotice(BaseModel):
    """com.sos.controller.model.order.ExpectedNotice"""

    board_name: Optional[str] = None
    notice_id: Optional[str] = None
    

class Outcome(BaseModel):
    """com.sos.controller.model.common.Outcome"""

    TYPE: Optional[str] = None
    namedValues: Optional[Dict[str, Any]] = None
    outcome: Any
    
    
class HistoricOutcome(BaseModel):
    """com.sos.controller.model.workflow.HistoricOutcome"""

    position: Optional[List[Union[int, str]]] = None
    outcome: Optional[Outcome] = None
    
    
class OrderMarkText(str, Enum):
    CANCELLING = "CANCELLING"
    OUTDATED = "OUTDATED"
    RESUMING = "RESUMING"
    SUSPENDING = "SUSPENDING"


class OrderMark(BaseModel):
    """Java: com.sos.joc.model.order.OrderMark"""

    severity: Optional[int] = None
    _text: Optional[OrderMarkText] = None
    
    
class PlanId(BaseModel):
    """com.sos.joc.model.plan.PlanId"""

    notice_space_key: Optional[str] = None
    plan_schema_id: Optional[str] = None
    
    
class ListParameterType(str, Enum):
    String = "String"
    Number = "Number"
    Boolean = "Boolean"


class ListParameter(BaseModel):
    """com.sos.inventory.model.workflow.ListParameter"""

    type: Optional[ListParameterType] = None
    
    
class ParameterType(str, Enum):
    String = "String"
    Number = "Number"
    Boolean = "Boolean"
    List = "List"
    
    
class Parameter(BaseModel):
    """com.sos.inventory.model.workflow.Parameter"""

    type: Optional[ParameterType] = None
    default: Optional[Union[str, float, bool, List[Any]]] = None
    facet: Optional[str] = None
    final: Optional[str] = None
    list: Optional[List[str]] = None
    message: Optional[str] = None
    listParameters: Optional[Dict[str, ListParameter]] = None
    
    
class Requirements(BaseModel):
    """com.sos.inventory.model.workflow.Requirements"""

    parameters: Optional[Dict[str, Parameter]] = None
    allowUndeclared: Optional[bool] = None
    
    
class OrderRetryState(BaseModel):
    """com.sos.controller.model.order.OrderRetryState"""

    attempt: Optional[int] = None
    next: Optional[datetime] = None
    
    
class OrderSleepState(BaseModel):
    """com.sos.controller.model.order.OrderSleepState"""

    until: Optional[datetime] = None
    
    
class OrderWaitingReason(str, Enum):
    BETWEEN_CYCLES = "BETWEEN_CYCLES"
    DELAYED_AFTER_ERROR = "DELAYED_AFTER_ERROR"
    EXPECTING_NOTICES = "EXPECTING_NOTICES"
    FORKED = "FORKED"
    WAITING_FOR_LOCK = "WAITING_FOR_LOCK"
    
    
class OrderState(BaseModel):
    """com.sos.joc.model.order.OrderState"""

    severity: Optional[int] = None
    _text: Optional[OrderStateText] = None
    _reason: Optional[OrderWaitingReason] = None
    
    
class WorkflowId(BaseModel):
    """com.sos.controller.model.workflow.WorkflowId"""

    path: Optional[str] = None
    version_id: Optional[str] = None
    

class OrderV(BaseModel):
    """com.sos.joc.model.order.OrderV"""
    
    agent_id: Optional[str] = None
    arguments: Optional[Dict[str, Any]] = None
    """a map for arbitrary key-value pairs"""

    attached_state: Optional[OrderAttachedState] = None
    can_leave: Optional[bool] = None
    """only relevant for state COMPLETED"""

    cycle_state: Optional[OrderCycleState] = None
    """set if state == BetweenCycles or processing inside a cycle"""

    cyclic_order: Optional[CyclicOrderInfos] = None
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    end_positions: Optional[List[Union[List[Union[int, str]], str]]] = None
    expected_notices: Optional[List[ExpectedNotice]] = None
    """if state._reason == EXPECTING_NOTICES"""

    has_child_orders: Optional[bool] = None
    historic_outcome: Optional[List[HistoricOutcome]] = None
    """only for compact parameter is false"""

    is_continuable: Optional[bool] = None
    is_resumable: Optional[bool] = None
    is_suspendible: Optional[bool] = None
    label: Optional[str] = None
    """a label is only in the response if the request restricts the orders to one workflow"""

    last_outcome: Optional[Outcome] = None
    marked: Optional[OrderMark] = None
    order_id: Optional[str] = None
    plan_id: Optional[PlanID] = None
    position: Optional[List[Union[int, str]]] = None
    """Actually, each even item is a string, each odd item is an integer"""

    position_is_implicit_end: Optional[bool] = None
    position_string: Optional[str] = None
    priority: Optional[int] = None
    question: Optional[str] = None
    """only relevant for state PROMPTING"""

    requirements: Optional[Requirements] = None
    retry_state: Optional[OrderRetryState] = None
    """set if state == DelayedAfterError"""

    scheduled_for: Optional[float] = None
    scheduled_never: Optional[bool] = None
    """deprecated -> is State.PENDING"""

    sleep_state: Optional[OrderSleepState] = None
    """set if state == OrderSleeping"""

    state: Optional[OrderState] = None
    subagent_id: Optional[str] = None
    survey_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    tags: Optional[List[str]] = None
    workflow_id: Optional[WorkflowID] = None
    

class OrdersV(BaseModel):
    """com.sos.joc.model.order.OrdersV"""
    
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    orders: Optional[List[OrderV]] = None
    survey_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    workflow_tags_per_workflow: Optional[Dict[str, List[str]]] = None
    """a map of workflowName -> tags-array"""
    
    
class SuspendOrders(ModifyOrdersBase):
    """com.sos.joc.model.order.SuspendOrders"""

    date_from: Optional[Union[str, datetime]] = None
    date_to: Optional[Union[str, datetime]] = None
    time_zone: Optional[str] = None

    kill: Optional[bool] = None
    deep: Optional[bool] = None
    reset: Optional[bool] = None
    
    
class ResumeOrders(ModifyOrdersBase):
    """com.sos.joc.model.order.ResumeOrders"""
    
    cycle_end_time: Optional[float] = None
    force: Optional[bool] = None
    """force execution of non-startable jobs after kill"""

    from_current_block: Optional[bool] = None
    position: Optional[Union[List[Union[int, str]], str]] = None
    variables: Optional[Dict[str, Any]] = None
    """a map for arbitrary key-value pairs"""
    
    
class ModifyWorkflows(BaseModel):
    """com.sos.joc.model.workflow.ModifyWorkflows"""
    
    all: Optional[bool] = None
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    folders: Optional[List[Folder]] = None
    workflow_paths: Optional[List[str]] = None
    workflow_tags: Optional[List[str]] = None
    workflow_id: Optional[WorkflowID] = None
    
    
class ModifyWorkflowPositions(ModifyWorkflows):
    """com.sos.joc.model.workflow.ModifyWorkflowPositions"""
    
    positions: Optional[List[Union[List[Union[int, str]], str]]] = None
    
    
class ModifyWorkflowLabels(BaseModel):
    """com.sos.joc.model.workflow.ModifyWorkflowLabels"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    labels: Optional[List[str]] = None
    workflow_path: Optional[str] = None
    

class ModifyNotice(BaseModel):
    """com.sos.joc.model.board.ModifyNotice"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    end_of_life: Optional[str] = None
    """0 or [number][smhdwMy] (where smhdwMy unit for second, minute, etc) or ISO 8601 timestamp"""

    notice_board_path: Optional[str] = None
    notice_id: Optional[str] = None
    time_zone: Optional[str] = None
    """see https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"""


class JOCConfigurationType(str, Enum):
    CUSTOMIZATION = "CUSTOMIZATION"
    GLOBALS = "GLOBALS"
    IGNORELIST = "IGNORELIST"
    PROFILE = "PROFILE"
    SETTING = "SETTING"
    IAM = "IAM"
    
    
class JOCConfiguration(BaseModel):
    """com.sos.joc.model.configuration.Configuration"""
    
    account: Optional[str] = None
    configuration_item: Optional[str] = None
    """JSON object as string,  depends on configuration type"""

    configuration_type: Optional[JOCConfigurationType] = None
    controller_id: Optional[str] = None
    id: Optional[float] = None
    name: Optional[str] = None
    object_type: Optional[str] = None
    shared: Optional[bool] = None
    

class Configuration200(BaseModel):
    """com.sos.joc.model.configuration.Configuration200"""
    
    configuration: Optional[JOCConfiguration] = None
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""
    
    
class StoreSettingsFilter(BaseModel):
    """com.sos.joc.model.settings.StoreSettingsFilter"""
    
    audit_log: Optional[AuditParams] = None
    configuration_item: Optional[str] = None
    """JSON object as string, depends on configuration type"""
    

class ClusterRestart(BaseModel):
    """com.sos.joc.model.cluster.ClusterRestart"""
    
    audit_log: Optional[AuditParams] = None
    type: Optional[ClusterServices] = None

    
class ClusterResponse(BaseModel):
    """com.sos.joc.model.cluster.ClusterResponse"""
    
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    state: Optional[JocClusterState] = None
    type: Optional[ClusterServices] = None


class ClusterServiceRun(BaseModel):
    """com.sos.joc.model.cluster.ClusterServiceRun"""
    
    audit_log: Optional[AuditParams] = None
    type: Optional[ClusterServices] = None
    

class Js7LicenseInfo(BaseModel):
    """com.sos.joc.model.joc.Js7LicenseInfo"""
    
    type: Optional[LicenseType] = None
    valid: Optional[bool] = None
    valid_from: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    valid_until: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""


class ReadAgentsV(BaseModel):
    """com.sos.joc.model.agent.ReadAgentsV"""
    
    agent_ids: Optional[List[str]] = None
    compact: Optional[bool] = None
    """controls if the object's data is compact or detailed"""

    controller_id: Optional[str] = None
    flat: Optional[bool] = None
    only_visible_agents: Optional[bool] = None
    states: Optional[List[AgentStateText]] = None
    

class AgentExportFilter(BaseModel):
    """com.sos.joc.model.agent.transfer.AgentExportFilter"""
    
    agent_ids: Optional[List[str]] = None
    audit_log: Optional[AuditParams] = None
    export_file: Optional[ExportFile] = None


class ClusterState(BaseModel):
    """com.sos.joc.model.controller.ClusterState"""
    
    text: Optional[str] = None
    loss_node: Optional[str] = None
    severity: Optional[int] = None
    """0=ClusterCoupled,
    1=ClusterNodesAppointed,ClusterPassiveLost,ClusterSwitchedOver,ClusterFailOver
    2=ClusterPreparedToBeCoupled,ClusterEmpty 3=ClusterUnknown
    """


class AgentClusterState(BaseModel):
    """com.sos.joc.model.agent.AgentClusterState"""
    
    text: Optional[AgentClusterStateText] = None
    severity: Optional[int] = None
    """0=ALL_SUBAGENTS_ARE_COUPLED_AND_ENABLED, 1=ONLY_SOME_SUBAGENTS_ARE_COUPLED_AND_ENABLED,
    2=NO_SUBAGENTS_ARE_COUPLED_AND_ENABLED, 2=UNKNOWN
    """


class AgentState(BaseModel):
    """com.sos.joc.model.agent.AgentState"""
    
    reason: Optional[AgentStateReason] = None
    text: Optional[AgentStateText] = None
    severity: Optional[int] = None
    """0=COUPLED, 1=RESETTING, 1=RESET, 2=COUPLINGFAILED, 3=UNKNOWN"""


class AgentStateV(BaseModel):
    """com.sos.joc.model.agent.AgentStateV"""
    
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    cluster_state: Optional[ClusterState] = None
    controller_id: Optional[str] = None
    disabled: Optional[bool] = None
    error_message: Optional[str] = None
    """if state == couplngFailed or unknown"""

    health_state: Optional[AgentClusterState] = None
    orders: Optional[List[OrderV]] = None
    process_limit: Optional[int] = None
    running_tasks: Optional[int] = None
    state: Optional[AgentState] = None
    subagent_id: Optional[str] = None
    url: Optional[str] = None
    version: Optional[str] = None


class AgentV(AgentStateV):
    """com.sos.joc.model.agent.AgentV"""
    
    subagents: Optional[List[Subagent]] = None


class AgentsV(BaseModel):
    """com.sos.joc.model.agent.AgentsV"""
    
    agents: Optional[List[AgentV]] = None
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    survey_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""
    
    
class ResetAgents(DeployAgents):
    """com.sos.joc.model.agent.ResetAgents"""
    
    force: Optional[bool] = None
    
    
class SubAgentCommand(BaseModel):
    """com.sos.joc.model.agent.SubAgentCommand"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    force: Optional[bool] = None
    """only relevant for reset subagent"""

    subagent_id: Optional[str] = None
    
    
class VersionsFilter(BaseModel):
    """com.sos.joc.model.joc.VersionsFilter"""
    
    agent_ids: Optional[List[str]] = None
    controller_ids: Optional[List[str]] = None
    

class AgentVersion(BaseModel):
    """com.sos.joc.model.joc.AgentVersion"""
    
    agent_id: Optional[str] = None
    compatibility: Optional[CompatibilityLevel] = None
    subagent_id: Optional[str] = None
    uri: Optional[str] = None
    version: Optional[str] = None
    
    
class ControllerVersion(BaseModel):
    """com.sos.joc.model.joc.ControllerVersion"""
    
    compatibility: Optional[CompatibilityLevel] = None
    controller_id: Optional[str] = None
    uri: Optional[str] = None
    version: Optional[str] = None
    

class VersionResponse(BaseModel):
    """com.sos.joc.model.joc.VersionResponse"""
    
    agent_versions: Optional[List[AgentVersion]] = None
    controller_versions: Optional[List[ControllerVersion]] = None
    joc_version: Optional[str] = None
    version: Optional[str] = None
    
    
class ControllerIdReq(BaseModel):
    """com.sos.joc.model.controller.ControllerIdReq"""
    
    controller_id: Optional[str] = None
    

class DB(BaseModel):
    """com.sos.joc.model.joc.DB"""
    
    component_state: Optional[ComponentState] = None
    connection_state: Optional[ConnectionState] = None
    dbms: Optional[str] = None
    """possible values 'SQL Server', 'MySQL', 'Oracle', 'PostgreSQL'"""

    version: Optional[str] = None    
    
    
class OperatingSystem(BaseModel):
    """com.sos.joc.model.controller.OperatingSystem"""
    
    architecture: Optional[str] = None
    distribution: Optional[str] = None
    """e.g. Windows 2012, CentOS Linux release 7.2.1511 (Core)"""

    name: Optional[str] = None
    """Windows, Linux, AIX, Solaris, other""" 
    

class ControllerConnectionState(BaseModel):
    """com.sos.joc.model.joc.ControllerConnectionState"""
    
    text: Optional[ConnectionStateText] = None
    severity: Optional[int] = None
    """0=established, 1=unstable, 2=unreachable, 3=unknown"""
    
    
class Cockpit(BaseModel):
    """com.sos.joc.model.joc.Cockpit"""
    
    cluster_node_state: Optional[ClusterNodeState] = None
    """not relevant for JOC as API server only"""

    component_state: Optional[ComponentState] = None
    connection_state: Optional[ConnectionState] = None
    controller_connection_states: Optional[List[ControllerConnectionState]] = None
    """not relevant for JOC as API server only"""

    current: Optional[bool] = None
    """true if joc is that joc which sends this response"""

    host: Optional[str] = None
    id: Optional[float] = None
    instance_id: Optional[str] = None
    is_api_server: Optional[bool] = None
    last_heartbeat: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    member_id: Optional[str] = None
    os: Optional[OperatingSystem] = None
    security_level: Optional[JocSecurityLevel] = None
    started_at: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    title: Optional[str] = None
    url: Optional[str] = None
    version: Optional[str] = None
    
    
class Components(BaseModel):
    """com.sos.joc.model.controller.Components"""
    
    cluster_state: Optional[ClusterState] = None
    controllers: Optional[List[Controller]] = None
    database: Optional[DB] = None
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    jocs: Optional[List[Cockpit]] = None
    
    
class ClusterSwitchMember(BaseModel):
    """com.sos.joc.model.cluster.ClusterSwitchMember"""
    
    audit_log: Optional[AuditParams] = None
    member_id: Optional[str] = None
    

class DailyPlanOrdersFilter(DailyPlanOrderFilterBase):
    """com.sos.joc.model.dailyplan.DailyPlanOrdersFilter"""

    expand_cycle_orders: Optional[bool] = None
    """for internal use only: controls if the cycle order should be expanded in the answer"""

    late: Optional[bool] = None
    order_tags: Optional[List[str]] = None
    states: Optional[List[DailyPlanOrderStateText]] = None
    submission_history_ids: Optional[List[float]] = None
    workflow_tags: Optional[List[str]] = None
    

class DailyPlanOrderState(BaseModel):
    """com.sos.joc.model.dailyplan.DailyPlanOrderState"""
    
    text: Optional[DailyPlanOrderStateText] = None
    severity: Optional[int] = None


class Period(BaseModel):
    """undefined for startMode=0"""

    begin: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    end: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    repeat: Optional[float] = None
    

class PlannedOrderItem(BaseModel):
    """com.sos.joc.model.dailyplan.PlannedOrderItem"""
    
    controller_id: Optional[str] = None
    cyclic_order: Optional[CyclicOrderInfos] = None
    end_time: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    error: Optional[Err] = None
    exit_code: Optional[int] = None
    expected_end_time: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    history_id: Optional[str] = None
    late: Optional[bool] = None
    node: Optional[str] = None
    """only for orders"""

    order_id: Optional[str] = None
    order_name: Optional[str] = None
    period: Optional[Period] = None
    """undefined for startMode=0"""

    planned_start_time: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    schedule_path: Optional[str] = None
    start_mode: Optional[int] = None
    """0=single_start, 1=start_start_repeat"""

    start_time: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    state: Optional[DailyPlanOrderState] = None
    submitted: Optional[bool] = None
    survey_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    tags: Optional[List[str]] = None
    workflow_path: Optional[str] = None
    

class PlannedOrders(BaseModel):
    """com.sos.joc.model.dailyplan.PlannedOrders"""
    
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    planned_order_items: Optional[List[PlannedOrderItem]] = None
    workflow_tags_per_workflow: Optional[Dict[str, List[str]]] = None
    """a map of workflowName -> tags-array"""


class OrderPath(BaseModel):
    """com.sos.joc.model.order.OrderPath"""
    
    order_id: Optional[str] = None
    workflow_path: Optional[str] = None

    
class OrdersFilter(BaseModel):
    """com.sos.joc.model.order.OrdersFilter"""
    
    compact: Optional[bool] = None
    """controls if the object's data is compact or detailed"""

    completed_date_from: Optional[str] = None
    """0 or [number][smhdwMy] (where smhdwMy unit for second, minute, etc) or ISO 8601 timestamp"""

    completed_date_to: Optional[str] = None
    """0 or [number][smhdwMy] (where smhdwMy unit for second, minute, etc) or ISO 8601 timestamp"""

    controller_id: Optional[str] = None
    date_from: Optional[str] = None
    """0 or [number][smhdwMy] (where smhdwMy unit for second, minute, etc) or ISO 8601 timestamp"""

    date_to: Optional[str] = None
    """0 or [number][smhdwMy] (where smhdwMy unit for second, minute, etc) or ISO 8601 timestamp"""

    exclude_workflows: Optional[List[str]] = None
    folders: Optional[List[Folder]] = None
    history_ids: Optional[List[float]] = None
    history_states: Optional[List[HistoryStateText]] = None
    limit: Optional[int] = None
    """only for db history urls to restrict the number of responsed records; -1=unlimited"""

    order_id: Optional[str] = None
    """pattern with wildcards '*' and '?' where '*' match zero or more characters and '?' match
    any single character
    """
    orders: Optional[List[OrderPath]] = None
    time_zone: Optional[str] = None
    """see https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"""

    workflow_name: Optional[str] = None
    """pattern with wildcards '*' and '?' where '*' match zero or more characters and '?' match
    any single character
    """
    workflow_path: Optional[str] = None
    """pattern with wildcards '*' and '?' where '*' match zero or more characters and '?' match
    any single character
    """


class HistoryState(BaseModel):
    """com.sos.joc.model.common.HistoryState"""
    text: Optional[HistoryStateText] = None
    severity: Optional[int] = None
    """0=successful, 1=incomplete, 2=failed with a green/yellow/red representation"""
    

class OrderHistoryItem(BaseModel):
    """com.sos.joc.model.order.OrderHistoryItem"""
    
    arguments: Optional[Dict[str, Any]] = None
    """a map for arbitrary key-value pairs"""

    children: Optional[List[Any]] = None
    controller_id: Optional[str] = None
    end_time: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    history_id: Optional[float] = None
    order_id: Optional[str] = None
    order_state: Optional[OrderState] = None
    planned_time: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    position: Optional[str] = None
    sequence: Optional[int] = None
    start_time: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    state: Optional[HistoryState] = None
    survey_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    tags: Optional[List[str]] = None
    workflow: Optional[str] = None
    """absolute path of an object."""


class OrderHistory(BaseModel):
    """com.sos.joc.model.order.OrderHistory"""

    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    history: Optional[List[OrderHistoryItem]] = None
    workflow_tags_per_workflow: Optional[Dict[str, List[str]]] = None
    """a map of workflowName -> tags-array"""

    
class TaskIdOfOrder(BaseModel):
    """com.sos.joc.model.job.TaskIdOfOrder"""

    history_id: Optional[float] = None
    position: Optional[str] = None
    
    
class JobPath(BaseModel):
    """com.sos.joc.model.job.JobPath"""
    
    job: Optional[str] = None
    """if job undefined or empty then all jobs of specified workflow are requested"""

    workflow_path: Optional[str] = None
    
    
class JobsFilter(BaseModel):
    """com.sos.joc.model.job.JobsFilter"""
    
    completed_date_from: Optional[str] = None
    """0 or [number][smhdwMy] (where smhdwMy unit for second, minute, etc) or ISO 8601 timestamp"""

    completed_date_to: Optional[str] = None
    """0 or [number][smhdwMy] (where smhdwMy unit for second, minute, etc) or ISO 8601 timestamp"""

    controller_id: Optional[str] = None
    criticalities: Optional[List[JobCriticality]] = None
    date_from: Optional[str] = None
    """0 or [number][smhdwMy] (where smhdwMy unit for second, minute, etc) or ISO 8601 timestamp"""

    date_to: Optional[str] = None
    """0 or [number][smhdwMy] (where smhdwMy unit for second, minute, etc) or ISO 8601 timestamp"""

    exclude_jobs: Optional[List[JobPath]] = None
    folders: Optional[List[Folder]] = None
    history_ids: Optional[List[TaskIdOfOrder]] = None
    history_states: Optional[List[HistoryState]] = None
    job_name: Optional[str] = None
    jobs: Optional[List[JobPath]] = None
    limit: Optional[int] = None
    """only for db history urls to restrict the number of responsed records; -1=unlimited"""

    task_ids: Optional[List[float]] = None
    time_zone: Optional[str] = None
    """see https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"""

    workflow_name: Optional[str] = None
    """pattern with wildcards '*' and '?' where '*' match zero or more characters and '?' match
    any single character
    """
    workflow_path: Optional[str] = None
    """pattern with wildcards '*' and '?' where '*' match zero or more characters and '?' match
    any single character
    """


class TaskHistoryItem(BaseModel):
    """com.sos.joc.model.job.TaskHistoryItem"""
    
    agent_url: Optional[str] = None
    arguments: Optional[Dict[str, Any]] = None
    """a map for arbitrary key-value pairs"""

    controller_id: Optional[str] = None
    criticality: Optional[str] = None
    end_time: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    error: Optional[Err] = None
    exit_code: Optional[int] = None
    job: Optional[str] = None
    label: Optional[str] = None
    order_id: Optional[str] = None
    position: Optional[str] = None
    retry_counter: Optional[int] = None
    sequence: Optional[int] = None
    start_time: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    state: Optional[HistoryState] = None
    survey_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    task_id: Optional[float] = None
    workflow: Optional[str] = None


class TaskHistory(BaseModel):
    """com.sos.joc.model.job.TaskHistory"""

    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    history: Optional[List[TaskHistoryItem]] = None
    workflow_tags_per_workflow: Optional[Dict[str, List[str]]] = None
    """a map of workflowName -> tags-array"""


class WorkflowFilter(BaseModel):
    """com.sos.joc.model.workflow.WorkflowFilter"""

    compact: Optional[bool] = None
    """controls if the object's data is compact or detailed"""

    controller_id: Optional[str] = None
    workflow_id: Optional[WorkflowID] = None


class WorkflowsFilter(BaseModel):
    """com.sos.joc.model.workflow.WorkflowsFilter"""
    
    agent_names: Optional[List[str]] = None
    compact: Optional[bool] = None
    """controls if the object's data is compact or detailed"""

    controller_id: Optional[str] = None
    folders: Optional[List[Folder]] = None
    instruction_states: Optional[List[SearchInstructionStateText]] = None
    regex: Optional[str] = None
    """regular expression to filter Controller objects by matching the path"""

    states: Optional[List[SyncStateText]] = None
    tags: Optional[List[str]] = None
    workflow_ids: Optional[List[WorkflowID]] = None


class InstructionState(BaseModel):
    text: Optional[InstructionStateText] = None
    severity: Optional[int] = None


class Instruction(BaseModel):
    """com.sos.inventory.model.instruction.Instruction"""
    
    position: Optional[List[Union[int, str]]] = None
    """Actually, each even item is a string, each odd item is an integer"""

    position_string: Optional[str] = None
    state: Optional[InstructionState] = None
    type: Optional[InstructionType] = None


class AdmissionTimeScheme(BaseModel):
    """com.sos.inventory.model.job.AdmissionTimeScheme"""
    
    periods: Optional[List[Period]] = None


class ExecutableScriptLogin(BaseModel):
    """com.sos.inventory.model.job.ExecutableScriptLogin"""
    
    credential_key: Optional[str] = None
    with_user_profile: Optional[bool] = None
    

class JobReturnCodeWarning(BaseModel):
    """com.sos.inventory.model.job.JobReturnCodeWarning"""
    
    failure: Optional[Union[List[int], str]] = None
    success: Optional[Union[List[int], str]] = None
    warning: Optional[Union[List[int], str]] = None
    

class Executable(BaseModel):
    """com.sos.inventory.model.job.Executable"""
    
    env: Optional[Dict[str, str]] = None
    """a map for arbitrary key-value pairs"""

    login: Optional[ExecutableScriptLogin] = None
    return_code_meaning: Optional[JobReturnCodeWarning] = None
    script: Optional[str] = None
    v1_compatible: Optional[bool] = None
    arguments: Optional[Dict[str, str]] = None
    """a map for arbitrary key-value pairs"""

    class_name: Optional[str] = None
    job_arguments: Optional[Dict[str, Any]] = None
    """a map for arbitrary key-value pairs"""


class JobTemplateRef(BaseModel):
    """com.sos.inventory.model.job.JobTemplateRef"""
    
    hash: Optional[str] = None
    name: Optional[str] = None
    

class JobNotificationMail(BaseModel):
    """com.sos.inventory.model.job.notification.JobNotificationMail"""
    
    bcc: Optional[str] = None
    cc: Optional[str] = None
    to: Optional[str] = None
    

class JobNotification(BaseModel):
    """com.sos.inventory.model.job.notification.JobNotification"""
    
    mail: Optional[JobNotificationMail] = None
    types: Optional[List[JobNotificationType]] = None
    

class JobReturnCode(JobReturnCodeWarning):
    """com.sos.inventory.model.job.JobReturnCode"""
    
    failure: Optional[Union[List[int], str]] = None
    success: Optional[Union[List[int], str]] = None
    

class Job(BaseModel):
    """com.sos.inventory.model.job.Job"""

    admission_time_scheme: Optional[AdmissionTimeScheme] = None
    agent_name: Optional[str] = None
    criticality: Optional[JobCriticality] = None
    default_arguments: Optional[Dict[str, str]] = None
    """a map for arbitrary key-value pairs"""

    documentation_name: Optional[str] = None
    executable: Optional[Executable] = None
    fail_on_err_written: Optional[bool] = None
    grace_timeout: Optional[int] = None
    """in seconds"""

    job_class_name: Optional[str] = None
    job_resource_names: Optional[List[str]] = None
    job_template: Optional[JobTemplateRef] = None
    notification: Optional[JobNotification] = None
    parallelism: Optional[int] = None
    return_code_meaning: Optional[JobReturnCode] = None
    skip_if_no_admission_for_order_day: Optional[bool] = None
    subagent_cluster_id: Optional[str] = None
    subagent_cluster_id_expr: Optional[str] = None
    timeout: Optional[int] = None
    title: Optional[str] = None
    warn_if_longer: Optional[str] = None
    warn_if_shorter: Optional[str] = None
    warn_on_err_written: Optional[bool] = None
    with_subagent_cluster_id_expr: Optional[bool] = None
    

class InventoryWorkflow(BaseModel):
    """com.sos.inventory.model.workflow.Workflow"""

    documentation_name: Optional[str] = None
    instructions: Optional[List[Instruction]] = None
    job_resource_names: Optional[List[str]] = None
    jobs: Optional[Dict[str, Job]] = None
    order_preparation: Optional[Requirements] = None
    time_zone: Optional[str] = None
    title: Optional[str] = None
    type: Optional[DeployType] = None
    version: Optional[str] = None
    """inventory repository version"""

    version_id: Optional[str] = None
    

class InventoryFileOrderSource(BaseModel):
    """com.sos.inventory.model.fileordersource.FileOrderSource"""

    agent_name: Optional[str] = None
    delay: Optional[int] = None
    directory: Optional[str] = None
    directory_expr: Optional[str] = None
    documentation_name: Optional[str] = None
    pattern: Optional[str] = None
    priority: Optional[int] = None
    tags: Optional[List[str]] = None
    time_zone: Optional[str] = None
    title: Optional[str] = None
    type: Optional[DeployType] = None
    version: Optional[str] = None
    """inventory repository version"""

    workflow_name: Optional[str] = None
    

class ControllerFileOrderSource(InventoryFileOrderSource):
    """com.sos.controller.model.fileordersource.FileOrderSource"""
    
    path: Optional[str] = None
    """absolute path of an object."""

    state: Optional[SyncState] = None
    version_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""
    
    
class ControllerWorkflow(InventoryWorkflow):
    """com.sos.controller.model.workflow.Workflow"""
    
    file_order_sources: Optional[List[ControllerFileOrderSource]] = None
    fork_list_variables: Optional[List[str]] = None
    has_add_order_dependencies: Optional[bool] = None
    has_consume_notice_boards: Optional[bool] = None
    has_expected_notice_boards: Optional[bool] = None
    has_post_notice_boards: Optional[bool] = None
    is_current_version: Optional[bool] = None
    num_of_skipped_instructions: Optional[int] = None
    num_of_stopped_instructions: Optional[int] = None
    path: Optional[str] = None
    """absolute path of an object."""

    state: Optional[SyncState] = None
    suspended: Optional[bool] = None
    """true if state._text == SUSPENDED or SUSPENDING"""

    version_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""
    

class Workflow(BaseModel):
    """com.sos.joc.model.workflow.Workflow"""
    
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    survey_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    workflow: Optional[ControllerWorkflow] = None
    
    
class Workflows(BaseModel):
    """com.sos.joc.model.workflow.Workflows"""
    
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    survey_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    workflows: Optional[List[ControllerWorkflow]] = None
    
    
class ModifyWorkflow(BaseModel):
    """com.sos.joc.model.workflow.ModifyWorkflow"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    workflow_id: Optional[WorkflowID] = None
    

class DailyPlanCancelOrders(DailyPlanOrderFilterBase):
    """com.sos.joc.model.dailyplan.DailyPlanCancelOrders"""
    
    audit_log: Optional[AuditParams] = None
    
    
class Cycle(BaseModel):
    """com.sos.joc.model.dailyplan.Cycle"""
    
    begin: Optional[str] = None
    end: Optional[str] = None
    repeat: Optional[str] = None


class DailyPlanBaseOrder(BaseModel):
    """com.sos.joc.model.dailyplan.DailyPlanBaseOrder"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    order_ids: Optional[List[str]] = None
    

class DailyPlanCopyOrder(DailyPlanBaseOrder):
    """com.sos.joc.model.dailyplan.DailyPlanCopyOrder"""
    
    cycle: Optional[Cycle] = None
    force_job_admission: Optional[bool] = None
    scheduled_for: Optional[str] = None
    """ISO format yyyy-mm-dd[ HH:MM[:SS]] or now or now + HH:MM[:SS] or now + SECONDS or empty"""

    stick_daily_plan_date: Optional[bool] = None
    time_zone: Optional[str] = None
    
    
class OrderIDMap200(BaseModel):
    """com.sos.joc.model.order.OrderIdMap200"""
    
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    order_ids: Optional[Dict[str, str]] = None
    

class PathItem(BaseModel):
    """com.sos.joc.model.dailyplan.generate.items.PathItem"""

    folders: Optional[List[Folder]] = None
    singles: Optional[List[str]] = None


class GenerateRequest(BaseModel):
    """com.sos.joc.model.dailyplan.generate.GenerateRequest"""

    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    daily_plan_date: Optional[datetime] = None
    """deprecated; use dailyPlanDates"""

    daily_plan_dates: Optional[List[date]] = None
    include_non_auto_planned_orders: Optional[bool] = None
    """includes non-automatically planned orders iff true"""

    overwrite: Optional[bool] = None
    """controls if the order should be overwritten"""

    schedule_paths: Optional[PathItem] = None
    """Define the path item of the selector to generate orders for the daily plan"""

    with_submit: Optional[bool] = None
    """controls if the order should be submitted to the controller"""

    workflow_paths: Optional[PathItem] = None
    """Define the path item of the selector to generate orders for the daily plan"""
    
    
class DailyPlanSubmitOrders(DailyPlanOrderFilterBase):
    """com.sos.joc.model.dailyplan.DailyPlanSubmitOrders"""
    
    audit_log: Optional[AuditParams] = None
    submission_history_ids: Optional[List[int]] = None
    
    
class DailyPlanDeleteOrders(DailyPlanOrderFilterBase):
    """com.sos.joc.model.dailyplan.DailyPlanDeleteOrders"""
    
    audit_log: Optional[AuditParams] = None
    late: Optional[bool] = None
    submission_history_ids: Optional[List[int]] = None
    
    
class DailyPlanModifyOrder(DailyPlanCopyOrder):
    """com.sos.joc.model.dailyplan.DailyPlanModifyOrder"""

    block_position: Optional[Union[List[Union[int, str]], str]] = None
    daily_plan_date: Optional[datetime] = None
    """ISO date YYYY-MM-DD"""

    end_positions: Optional[List[Union[List[Union[int, str]], str]]] = None
    remove_variables: Optional[List[str]] = None
    start_position: Optional[Union[List[Union[int, str]], str]] = None
    variables: Optional[Dict[str, Any]] = None
    """a map for arbitrary key-value pairs"""


class SubmissionsDeleteRequestFilter(BaseModel):
    """com.sos.joc.model.dailyplan.submissions.SubmissionsDeleteRequestFilter"""
    
    date_for: Optional[date] = None
    """ISO date YYYY-MM-DD"""

    date_from: Optional[date] = None
    """ISO date YYYY-MM-DD"""

    date_to: Optional[date] = None
    """ISO date YYYY-MM-DD"""
    
    
class SubmissionsDeleteRequest(BaseModel):
    """com.sos.joc.model.dailyplan.submissions.SubmissionsDeleteRequest"""
    
    audit_log: Optional[AuditParams] = None
    controller_id: Optional[str] = None
    filter: Optional[SubmissionsDeleteRequestFilter] = None
    
    
class ProjectionsRequest(BaseModel):
    """com.sos.joc.model.dailyplan.projections.ProjectionsRequest"""
    
    controller_ids: Optional[List[str]] = None
    date_from: Optional[date] = None
    """ISO date YYYY-MM-DD"""

    date_to: Optional[date] = None
    """ISO date YYYY-MM-DD"""

    schedule_folders: Optional[List[Folder]] = None
    schedule_paths: Optional[List[str]] = None
    without_start_time: Optional[bool] = None
    workflow_folders: Optional[List[Folder]] = None
    workflow_paths: Optional[List[str]] = None


class WhenHolidayType(str, Enum):
    """com.sos.inventory.model.calendar.WhenHolidayType"""

    IGNORE = "IGNORE"
    NEXTNONWORKINGDAY = "NEXTNONWORKINGDAY"
    PREVIOUSNONWORKINGDAY = "PREVIOUSNONWORKINGDAY"
    SUPPRESS = "SUPPRESS"
    
    
class CalendarPeriod(BaseModel):
    """com.sos.inventory.model.calendar.Period"""
    begin: Optional[str] = None
    end: Optional[str] = None
    repeat: Optional[str] = None
    single_start: Optional[str] = None
    when_holiday: Optional[WhenHolidayType] = None
    """default: SUPPRESS"""
    

class DatePeriodItem(BaseModel):
    """com.sos.joc.model.dailyplan.projections.items.year.DatePeriodItem"""
    
    period: Optional[CalendarPeriod] = None
    schedule: Optional[str] = None
    schedule_order_name: Optional[str] = None
    workflow: Optional[str] = None
    

class DateItem(BaseModel):
    """com.sos.joc.model.dailyplan.projections.items.year.DateItem"""
    
    non_periods: Optional[List[DatePeriodItem]] = None
    num_of_non_periods: Optional[int] = None
    num_of_orders: Optional[int] = None
    periods: Optional[List[DatePeriodItem]] = None
    planned: Optional[bool] = None
    

class MetaItem(BaseModel):
    """com.sos.joc.model.dailyplan.projections.items.meta.MetaItem"""
    
    excluded_from_projection: Optional[bool] = None
    order_names: Optional[List[str]] = None
    """this property is only set if the schedule defines orders"""

    total_orders: Optional[float] = None
    workflow_paths: Optional[List[str]] = None
    """this property is only used for a shorter response of ./projections/day API"""

    workflows: Optional[Dict[str, Workflow]] = None
    

class ProjectionsCalendarResponse(BaseModel):
    """com.sos.joc.model.dailyplan.projections.ProjectionsCalendarResponse"""

    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    meta: Optional[Dict[str, Dict[str, MetaItem]]] = None
    survey_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    years: Optional[Dict[str, Dict[str, Dict[str, DateItem]]]] = None
    
    
class ProjectionsDayRequest(BaseModel):
    """com.sos.joc.model.dailyplan.projections.ProjectionsDayRequest"""
    
    controller_ids: Optional[List[str]] = None
    date: Optional[datetime] = None
    """ISO date YYYY-MM-DD"""

    schedule_folders: Optional[List[Folder]] = None
    schedule_paths: Optional[List[str]] = None
    without_start_time: Optional[bool] = None
    workflow_folders: Optional[List[Folder]] = None
    workflow_paths: Optional[List[str]] = None
    

class WorkflowItem(BaseModel):
    """com.sos.joc.model.dailyplan.projections.items.meta.WorkflowItem"""
    
    avg: Optional[float] = None
    

class ScheduleInfoItem(BaseModel):
    """com.sos.joc.model.dailyplan.projections.items.meta.ScheduleInfoItem"""
    
    excluded_from_projection: Optional[bool] = None
    order_names: Optional[List[str]] = None
    """this property is only set if the schedule defines orders"""

    total_orders: Optional[float] = None
    workflow_paths: Optional[List[str]] = None
    """this property is only used for a shorter response of ./projections/day API"""

    workflows: Optional[Dict[str, WorkflowItem]] = None
    

class ProjectionsDayResponse(DateItem):
    """com.sos.joc.model.dailyplan.projections.ProjectionsDayResponse"""
    
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    meta: Optional[Dict[str, Dict[str, ScheduleInfoItem]]] = None
    survey_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""


class Configuration(BaseModel):
    """com.sos.joc.model.configuration.Configuration"""
    
    account: Optional[str] = None
    configuration_item: Optional[str] = None
    """JSON object as string,  depends on configuration type"""

    configuration_type: Optional[ConfigurationType] = None
    controller_id: Optional[str] = None
    id: Optional[float] = None
    name: Optional[str] = None
    object_type: Optional[str] = None
    shared: Optional[bool] = None


class ConfigurationOk(BaseModel):
    """com.sos.joc.model.configuration.ConfigurationOk"""
    
    delivery_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""

    id: Optional[int] = None
    survey_date: Optional[datetime] = None
    """Value is UTC timestamp in ISO 8601 YYYY-MM-DDThh:mm:ss.sZ or empty"""
    

class Notice(BaseModel):
    notice_board_path: Optional[str] = None
    notice_ids: Optional[List[str]] = None

class DeleteNotices(ModifyNotice):
    """com.sos.joc.model.board.DeleteNotices"""
    
    notice_board_path: Optional[str] = None
    notice_ids: Optional[List[str]] = None
    notices: Optional[List[Notice]] = None