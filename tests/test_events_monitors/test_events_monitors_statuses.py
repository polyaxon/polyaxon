from django.conf import settings

from event_monitors.tasks import handle_events_job_statuses, handle_events_plugin_job_statuses
from models.experiments import ExperimentJobStatus
from factories.factory_experiments import ExperimentJobFactory
from factories.factory_plugins import NotebookJobFactory, TensorboardJobFactory
from factories.factory_projects import ProjectFactory
from statuses.jobs import JobLifeCycle
from models.plugins import NotebookJobStatus, TensorboardJobStatus
from runner.spawners.utils.jobs import get_job_state
from tests.fixtures import (
    status_experiment_job_event,
    status_experiment_job_event_with_conditions,
    status_notebook_job_event,
    status_notebook_job_event_with_conditions,
    status_tensorboard_job_event,
    status_tensorboard_job_event_with_conditions
)
from tests.utils import BaseTest


class TestEventsBaseJobsStatusesHandling(BaseTest):
    EVENT = None
    EVENT_WITH_CONDITIONS = None
    CONTAINER_NAME = None
    STATUS_MODEL = None
    STATUS_HANDLER = None

    def get_job_object(self, job_state):
        raise NotImplemented  # noqa

    def test_handle_events_job_statuses_for_non_existing_job(self):
        assert self.STATUS_MODEL.objects.count() == 0
        job_state = get_job_state(
            event_type=self.EVENT['type'],  # pylint:disable=unsubscriptable-object
            event=self.EVENT['object'],  # pylint:disable=unsubscriptable-object
            job_container_names=(self.CONTAINER_NAME,),
            experiment_type_label=settings.TYPE_LABELS_EXPERIMENT)
        self.STATUS_HANDLER(job_state.to_dict())  # pylint:disable=not-callable
        assert self.STATUS_MODEL.objects.count() == 0

    def test_handle_events_job_statuses_for_existing_job_with_unknown_conditions(self):
        assert self.STATUS_MODEL.objects.count() == 0
        job_state = get_job_state(
            event_type=self.EVENT['type'],  # pylint:disable=unsubscriptable-object
            event=self.EVENT['object'],  # pylint:disable=unsubscriptable-object
            job_container_names=(self.CONTAINER_NAME,),
            experiment_type_label=settings.TYPE_LABELS_EXPERIMENT)

        job = self.get_job_object(job_state)

        self.STATUS_HANDLER(job_state.to_dict())  # pylint:disable=not-callable
        assert self.STATUS_MODEL.objects.count() == 2
        statuses = self.STATUS_MODEL.objects.filter(job=job).values_list('status', flat=True)
        assert set(statuses) == {JobLifeCycle.CREATED, JobLifeCycle.UNKNOWN}

    def test_handle_events_job_statuses_for_existing_job_with_known_conditions(self):
        assert self.STATUS_MODEL.objects.count() == 0
        job_state = get_job_state(
            event_type=self.EVENT_WITH_CONDITIONS['type'],  # pylint:disable=unsubscriptable-object
            event=self.EVENT_WITH_CONDITIONS['object'],  # pylint:disable=unsubscriptable-object
            job_container_names=(self.CONTAINER_NAME,),
            experiment_type_label=settings.TYPE_LABELS_EXPERIMENT)

        job = self.get_job_object(job_state)

        self.STATUS_HANDLER(job_state.to_dict())  # pylint:disable=not-callable
        assert self.STATUS_MODEL.objects.count() == 2
        statuses = self.STATUS_MODEL.objects.filter(job=job).values_list('status', flat=True)
        assert set(statuses) == {JobLifeCycle.CREATED, JobLifeCycle.FAILED}


class TestEventsExperimentJobsStatusesHandling(TestEventsBaseJobsStatusesHandling):
    EVENT = status_experiment_job_event
    EVENT_WITH_CONDITIONS = status_experiment_job_event_with_conditions
    CONTAINER_NAME = settings.CONTAINER_NAME_JOB
    STATUS_MODEL = ExperimentJobStatus
    STATUS_HANDLER = handle_events_job_statuses

    def get_job_object(self, job_state):
        job_uuid = job_state.details.labels.job_uuid.hex
        return ExperimentJobFactory(uuid=job_uuid)


class TestEventsTensorboardJobsStatusesHandling(TestEventsBaseJobsStatusesHandling):
    EVENT = status_tensorboard_job_event
    EVENT_WITH_CONDITIONS = status_tensorboard_job_event_with_conditions
    CONTAINER_NAME = settings.CONTAINER_NAME_PLUGIN_JOB
    STATUS_MODEL = TensorboardJobStatus
    STATUS_HANDLER = handle_events_plugin_job_statuses

    def get_job_object(self, job_state):
        project_uuid = job_state.details.labels.project_uuid.hex
        project = ProjectFactory(uuid=project_uuid)
        return TensorboardJobFactory(project=project)


class TestEventsNotebookJobsStatusesHandling(TestEventsBaseJobsStatusesHandling):
    EVENT = status_notebook_job_event
    EVENT_WITH_CONDITIONS = status_notebook_job_event_with_conditions
    CONTAINER_NAME = settings.CONTAINER_NAME_PLUGIN_JOB
    STATUS_MODEL = NotebookJobStatus
    STATUS_HANDLER = handle_events_plugin_job_statuses

    def get_job_object(self, job_state):
        project_uuid = job_state.details.labels.project_uuid.hex
        project = ProjectFactory(uuid=project_uuid)
        return NotebookJobFactory(project=project)


# Prevent this base class from running tests
del TestEventsBaseJobsStatusesHandling
