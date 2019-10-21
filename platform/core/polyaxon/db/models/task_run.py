# import logging
# import uuid
#
# from typing import Dict, Optional, Tuple
#
# from hestia.datetime_typing import AwareDT
#
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
# from django.conf import settings
# from django.contrib.postgres.fields import JSONField
# from django.db import models
# from django.dispatch import Signal
#
# from db.models.statuses import LastStatusMixin, StatusModel
# from db.models.unique_names import OPS_UNIQUE_NAME_FORMAT, PIPELINES_UNIQUE_NAME_FORMAT
# from db.models.utils import (
#     BackendModel,
#     DeletedModel,
#     DescribableModel,
#     DiffModel,
#     IsManagedModel,
#     NameableModel,
#     RunTimeModel,
#     TagModel
# )
# from lifecycles.operations import OperationStatuses
# from lifecycles.pipelines import PipelineLifeCycle, TriggerPolicy
# from polyaxon.settings import Intervals
#
#
# class TaskRunStatus(StatusModel):
#     """A model that represents an operation run status at certain time."""
#     STATUSES = OperationStatuses
#
#     status = models.CharField(
#         max_length=64,
#         blank=True,
#         null=True,
#         default=STATUSES.CREATED,
#         choices=STATUSES.CHOICES)
#     operation_run = models.ForeignKey(
#         'db.OperationRun',
#         on_delete=models.CASCADE,
#         related_name='statuses')
#
#     class Meta:
#         app_label = 'db'
#         verbose_name_plural = 'Operation Run Statuses'
#         ordering = ['created_at']
#
#     def __str__(self) -> str:
#         return '{} <{}>'.format(self.operation_run, self.status)
#
#
#
# class OperationRun(RunModel):
#     """A model that represents an execution behaviour/run of instance of an operation."""
#     STATUSES = OperationStatuses
#
#     operation = models.ForeignKey(
#         'db.Operation',
#         on_delete=models.CASCADE,
#         related_name='runs')
#     pipeline_run = models.ForeignKey(
#         'db.PipelineRun',
#         on_delete=models.CASCADE,
#         related_name='operation_runs')
#     upstream_runs = models.ManyToManyField(
#         'self',
#         blank=True,
#         symmetrical=False,
#         related_name='downstream_runs')
#     status = models.OneToOneField(
#         'db.OperationRunStatus',
#         related_name='+',
#         blank=True,
#         null=True,
#         editable=True,
#         on_delete=models.SET_NULL)
#     celery_task_context = JSONField(
#         blank=True,
#         null=True,
#         help_text='The kwargs required to execute the celery task.')
#     celery_task_id = models.CharField(max_length=36, null=False, blank=True)
#
#     class Meta:
#         app_label = 'db'
#
#     def last_status_before(self, status_date: AwareDT = None) -> Optional[str]:
#         if not status_date:
#             return self.last_status
#         status = OperationRunStatus.objects.filter(
#             operation_run=self,
#             created_at__lte=status_date).last()
#         return status.status if status else None
#
#     def set_status(self,
#                    status: str,
#                    created_at: AwareDT = None,
#                    message: str = None,
#                    traceback: Dict = None,
#                    **kwargs) -> None:
#         last_status = self.last_status_before(status_date=created_at)
#         if self.can_transition(status_from=last_status, status_to=status):
#             params = {'created_at': created_at} if created_at else {}
#             OperationRunStatus.objects.create(operation_run=self,
#                                               status=status,
#                                               traceback=traceback,
#                                               message=message,
#                                               **params)
#
#     def check_concurrency(self) -> bool:
#         """Checks the concurrency of the operation run.
#         Checks the concurrency of the operation run
#         to validate if we can start a new operation run.
#         Returns:
#             boolean: Whether to start a new operation run or not.
#         """
#         if not self.operation.concurrency:  # No concurrency set
#             return True
#
#         ops_count = self.operation.runs.filter(
#             status__status__in=self.STATUSES.RUNNING_STATUS).count()
#         return ops_count < self.operation.concurrency
#
#     def check_upstream_trigger(self) -> bool:
#         """Checks the upstream and the trigger rule."""
#         if self.operation.trigger_policy == TriggerPolicy.ONE_DONE:
#             return self.upstream_runs.filter(
#                 status__status__in=self.STATUSES.DONE_STATUS).exists()
#         if self.operation.trigger_policy == TriggerPolicy.ONE_SUCCEEDED:
#             return self.upstream_runs.filter(
#                 status__status=self.STATUSES.SUCCEEDED).exists()
#         if self.operation.trigger_policy == TriggerPolicy.ONE_FAILED:
#             return self.upstream_runs.filter(
#                 status__status=self.STATUSES.FAILED).exists()
#
#         statuses = self.upstream_runs.values_list('status__status', flat=True)
#         if self.operation.trigger_policy == TriggerPolicy.ALL_DONE:
#             return not bool([True for status in statuses
#                              if status not in self.STATUSES.DONE_STATUS])
#         if self.operation.trigger_policy == TriggerPolicy.ALL_SUCCEEDED:
#             return not bool([True for status in statuses
#                              if status != self.STATUSES.SUCCEEDED])
#         if self.operation.trigger_policy == TriggerPolicy.ALL_FAILED:
#             return not bool([True for status in statuses
#                              if status not in self.STATUSES.FAILED_STATUS])
#
#     @property
#     def is_upstream_done(self) -> bool:
#         statuses = self.upstream_runs.values_list('status__status', flat=True)
#         return not bool([True for status in statuses
#                          if status not in self.STATUSES.DONE_STATUS])
#
#     def schedule_start(self) -> bool:
#         """Schedule the task: check first if the task can start:
#             1. we check that the task is still in the CREATED state.
#             2. we check that the upstream dependency is met.
#             3. we check that pipeline can start a new task;
#               i.e. we check the concurrency of the pipeline.
#             4. we check that operation can start a new instance;
#               i.e. we check the concurrency of the operation.
#         -> If all checks pass we schedule the task start it.
#         -> 1. If the operation is not in created status, nothing to do.
#         -> 2. If the upstream dependency check is not met, two use cases need to be validated:
#             * The upstream dependency is not met but could be met in the future,
#               because some ops are still CREATED/SCHEDULED/RUNNING/...
#               in this case nothing need to be done, every time an upstream operation finishes,
#               it will notify all the downstream ops including this one.
#             * The upstream dependency is not met and could not be met at all.
#               In this case we need to mark the task with `UPSTREAM_FAILED`.
#         -> 3. If the pipeline has reached it's concurrency limit,
#            we just delay schedule based on the interval/time delay defined by the user.
#            The pipeline scheduler will keep checking until the task can be scheduled or stopped.
#         -> 4. If the operation has reached it's concurrency limit,
#            Same as above we keep trying based on an interval defined by the user.
#         Returns:
#             boolean: Whether to try to schedule this operation run in the future or not.
#         """
#         if self.last_status != self.STATUSES.CREATED:
#             return False
#
#         upstream_trigger_check = self.check_upstream_trigger()
#         if not upstream_trigger_check and self.is_upstream_done:
#             # This task cannot be scheduled anymore
#             self.on_upstream_failed()
#             return False
#
#         if not self.pipeline_run.check_concurrency():
#             return True
#
#         if not self.check_concurrency():
#             return True
#
#         self.on_scheduled()
#         self.start()
#         return False
#
#     def start(self) -> None:
#         """Start the celery task of this operation."""
#         kwargs = self.celery_task_context
#         # Update we the operation run id
#         kwargs['operation_run_id'] = self.id  # pylint:disable=unsupported-assignment-operation
#
#         async_result = celery_app.send_task(
#             self.operation.celery_task,
#             kwargs=kwargs,
#             **self.operation.get_run_params())
#         self.celery_task_id = async_result.id
#         self.save()
#
#     def stop(self, message: str = None) -> None:
#         if self.is_stoppable:
#             task = AsyncResult(self.celery_task_id)
#             task.revoke(terminate=True, signal='SIGKILL')
#         self.on_stop(message=message)
#
#     def skip(self, message: str = None) -> None:
#         self.on_skip(message=message)
#
#     def on_retry(self) -> None:
#         self.set_status(status=self.STATUSES.RETRYING)
#
#     def on_upstream_failed(self) -> None:
#         self.set_status(status=self.STATUSES.UPSTREAM_FAILED)
#
#     def on_failure(self, message: str = None) -> None:
#         self.set_status(status=self.STATUSES.FAILED, message=message)
#         self.save()
#
#     def on_success(self, message: str = None) -> None:
#         self.set_status(status=self.STATUSES.SUCCEEDED, message=message)
