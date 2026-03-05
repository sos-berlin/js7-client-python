from typing import List, Optional

from ....client.context import Context
from ....model.public.client.common.audit_log import AuditLog

from ...action.workflow.resume_workflows_action import resume_workflows_action
from ...action.workflow.skip_job_instructions_action import skip_job_instructions_action
from ...action.workflow.stop_job_instructions_action import stop_job_instructions_action
from ...action.workflow.suspend_workflows_action import suspend_workflows_action
from ...action.workflow.unskip_job_instructions_action import unskip_job_instructions_action
from ...action.workflow.unstop_job_instructions_action import unstop_job_instructions_action


class Operate:
    def __init__(self, context: Context):
        self._ctx = context
        
    def resume_workflow(
        self,
        controller_id: str,
        workflow_paths: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Resumes a suspended workflow.

        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.

            workflow_path (str):
                The full path of the workflow that should be resumed.

            audit_log (Optional[AuditLog]):
                Creates an audit log entry for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments such as `controller_id`
                or `workflow_path` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """

        return resume_workflows_action(
            context=self._ctx,
            controller_id=controller_id,
            workflow_paths=workflow_paths,
            audit_log=audit_log
        )
        
    def skip_job_instructions(
        self,
        controller_id: str,
        workflow_path: str,
        labels: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Skips one or more job instructions in a workflow.

        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.

            workflow_path (str):
                The full path of the workflow in which the specified job
                instructions should be skipped.

            labels (List[str]):
                A list of job instruction labels that should be skipped.

            audit_log (Optional[AuditLog]):
                Creates an audit log entry for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments such as `controller_id`,
                `workflow_path`, or `labels` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return skip_job_instructions_action(
            context=self._ctx,
            controller_id=controller_id,
            workflow_path=workflow_path,
            labels=labels,
            audit_log=audit_log
        )
        
    def stop_job_instructions(
        self,
        controller_id: str,
        workflow_path: str,
        labels: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Stops one or more job instructions in a workflow.

        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.

            workflow_path (str):
                The full path of the workflow in which the specified job
                instructions should be stopped.

            labels (List[str]):
                A list of job instruction labels identifying the job
                instructions that should be stopped.

            audit_log (Optional[AuditLog]):
                Creates an audit log entry for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments such as `controller_id`,
                `workflow_path`, or `labels` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return stop_job_instructions_action(
            context=self._ctx,
            controller_id=controller_id,
            workflow_path=workflow_path,
            labels=labels,
            audit_log=audit_log
        )
        
    def suspend_workflows(
        self,
        controller_id: str,
        workflow_paths: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Suspends one or more workflows.

        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.

            workflow_paths (List[str]):
                A list of workflow paths identifying the workflows
                that should be suspended.

            audit_log (Optional[AuditLog]):
                Creates an audit log entry for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments such as `controller_id`
                or `workflow_paths` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """
        
        return suspend_workflows_action(
            context=self._ctx,
            controller_id=controller_id,
            workflow_paths=workflow_paths,
            audit_log=audit_log
        )
        
    def unskip_job_instructions(
        self,
        controller_id: str,
        workflow_path: str,
        labels: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Unskips previously skipped job instructions in a workflow.

        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.

            workflow_path (str):
                The full path of the workflow in which the specified job
                instructions should be re-enabled.

            labels (List[str]):
                A list of job instruction labels identifying the job
                instructions that should no longer be skipped.

            audit_log (Optional[AuditLog]):
                Creates an audit log entry for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments such as `controller_id`,
                `workflow_path`, or `labels` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """

        return unskip_job_instructions_action(
            context=self._ctx,
            controller_id=controller_id,
            workflow_path=workflow_path,
            labels=labels,
            audit_log=audit_log
        )
        
    def unstop_job_instructions(
        self,
        controller_id: str,
        workflow_path: str,
        labels: List[str],
        audit_log: Optional[AuditLog] = None
    ) -> bool:
        """
        Releases previously stopped job instructions in a workflow.

        Args:
            controller_id (str):
                The ID of the controller on which the operation should be executed.

            workflow_path (str):
                The full path of the workflow in which the specified job
                instructions should be released.

            labels (List[str]):
                A list of job instruction labels identifying the job
                instructions that should no longer remain stopped.

            audit_log (Optional[AuditLog]):
                Creates an audit log entry for this operation.

        Returns:
            bool:
                Returns `True` if the operation was successful,
                otherwise `False`.

        Raises:
            ValueError:
                If required arguments such as `controller_id`,
                `workflow_path`, or `labels` are missing or invalid.

            RuntimeError:
                If the server version is not compatible or if an
                unexpected response is returned.
        """

        return unstop_job_instructions_action(
            context=self._ctx,
            controller_id=controller_id,
            workflow_path=workflow_path,
            labels=labels,
            audit_log=audit_log
        )