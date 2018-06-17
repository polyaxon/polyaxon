import pytest

from mock import patch

from django.conf import settings

from constants.jobs import JobLifeCycle
from db.models.build_jobs import BuildJobStatus
from db.models.experiment_jobs import ExperimentJobStatus
from db.models.jobs import JobStatus
from db.models.notebooks import NotebookJobStatus
from db.models.tensorboards import TensorboardJobStatus
from events_handlers.tasks import (
    events_handle_build_job_statuses,
    events_handle_experiment_job_statuses,
    events_handle_job_statuses,
    events_handle_plugin_job_statuses
)
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_experiments import ExperimentJobFactory
from factories.factory_jobs import JobFactory
from factories.factory_plugins import NotebookJobFactory, TensorboardJobFactory
from factories.factory_projects import ProjectFactory
from monitor_statuses.jobs import get_job_state
from tests.fixtures import (
    status_build_job_event,
    status_build_job_event_with_conditions,
    status_experiment_job_event,
    status_experiment_job_event_with_conditions,
    status_job_event,
    status_job_event_with_conditions,
    status_notebook_job_event,
    status_notebook_job_event_with_conditions,
    status_tensorboard_job_event,
    status_tensorboard_job_event_with_conditions
)
from tests.utils import BaseTest


@pytest.mark.monitors_mark
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


@pytest.mark.monitors_mark
class TestEventsExperimentJobsStatusesHandling(TestEventsBaseJobsStatusesHandling):
    EVENT = status_experiment_job_event
    EVENT_WITH_CONDITIONS = status_experiment_job_event_with_conditions
    CONTAINER_NAME = settings.CONTAINER_NAME_EXPERIMENT_JOB
    STATUS_MODEL = ExperimentJobStatus
    STATUS_HANDLER = events_handle_experiment_job_statuses

    def get_job_object(self, job_state):
        job_uuid = job_state.details.labels.job_uuid.hex
        return ExperimentJobFactory(uuid=job_uuid)


@pytest.mark.monitors_mark
class TestEventsJobsStatusesHandling(TestEventsBaseJobsStatusesHandling):
    EVENT = status_job_event
    EVENT_WITH_CONDITIONS = status_job_event_with_conditions
    CONTAINER_NAME = settings.CONTAINER_NAME_JOB
    STATUS_MODEL = JobStatus
    STATUS_HANDLER = events_handle_job_statuses

    def get_job_object(self, job_state):
        job_uuid = job_state.details.labels.job_uuid.hex
        with patch('scheduler.tasks.jobs.jobs_build.apply_async') as _:
            return JobFactory(uuid=job_uuid)


@pytest.mark.monitors_mark
class TestEventsTensorboardJobsStatusesHandling(TestEventsBaseJobsStatusesHandling):
    EVENT = status_tensorboard_job_event
    EVENT_WITH_CONDITIONS = status_tensorboard_job_event_with_conditions
    CONTAINER_NAME = settings.CONTAINER_NAME_PLUGIN_JOB
    STATUS_MODEL = TensorboardJobStatus
    STATUS_HANDLER = events_handle_plugin_job_statuses

    def get_job_object(self, job_state):
        project_uuid = job_state.details.labels.project_uuid.hex
        project = ProjectFactory(uuid=project_uuid)
        job_uuid = job_state.details.labels.job_uuid.hex
        return TensorboardJobFactory(uuid=job_uuid, project=project)


@pytest.mark.monitors_mark
class TestEventsNotebookJobsStatusesHandling(TestEventsBaseJobsStatusesHandling):
    EVENT = status_notebook_job_event
    EVENT_WITH_CONDITIONS = status_notebook_job_event_with_conditions
    CONTAINER_NAME = settings.CONTAINER_NAME_PLUGIN_JOB
    STATUS_MODEL = NotebookJobStatus
    STATUS_HANDLER = events_handle_plugin_job_statuses

    def get_job_object(self, job_state):
        project_uuid = job_state.details.labels.project_uuid.hex
        project = ProjectFactory(uuid=project_uuid)
        job_uuid = job_state.details.labels.job_uuid.hex
        return NotebookJobFactory(uuid=job_uuid, project=project)


@pytest.mark.monitors_mark
class TestEventsDockerizerJobsStatusesHandling(TestEventsBaseJobsStatusesHandling):
    EVENT = status_build_job_event
    EVENT_WITH_CONDITIONS = status_build_job_event_with_conditions
    CONTAINER_NAME = settings.CONTAINER_NAME_DOCKERIZER_JOB
    STATUS_MODEL = BuildJobStatus
    STATUS_HANDLER = events_handle_build_job_statuses

    def get_job_object(self, job_state):
        project_uuid = job_state.details.labels.project_uuid.hex
        project = ProjectFactory(uuid=project_uuid)
        job_uuid = job_state.details.labels.job_uuid.hex

        return BuildJobFactory(uuid=job_uuid, project=project)


# Prevent this base class from running tests
del TestEventsBaseJobsStatusesHandling
