import datetime

import pytest

from mock import patch

from django.utils import timezone

import conf

from db.models.build_jobs import BuildJobStatus
from db.models.experiment_jobs import ExperimentJobStatus
from db.models.jobs import JobStatus
from db.models.notebooks import NotebookJobStatus
from db.models.tensorboards import TensorboardJobStatus
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_experiments import ExperimentJobFactory
from factories.factory_jobs import JobFactory
from factories.factory_plugins import NotebookJobFactory, TensorboardJobFactory
from factories.factory_projects import ProjectFactory
from k8s_events_handlers.tasks.statuses import (
    k8s_events_handle_build_job_statuses,
    k8s_events_handle_experiment_job_statuses,
    k8s_events_handle_job_statuses,
    k8s_events_handle_plugin_job_statuses
)
from lifecycles.jobs import JobLifeCycle
from monitor_statuses.jobs import get_job_state
from options.registry.container_names import (
    CONTAINER_NAME_BUILD_JOBS,
    CONTAINER_NAME_EXPERIMENT_JOBS,
    CONTAINER_NAME_JOBS,
    CONTAINER_NAME_PLUGIN_JOBS
)
from options.registry.spawner import TYPE_LABELS_RUNNER
from tests.base.case import BaseTest
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


@pytest.mark.monitors_mark
class TestEventsBaseJobsStatusesHandling(BaseTest):
    STATUS_MODEL = None
    STATUS_HANDLER = None

    def get_event(self):
        raise NotImplementedError()

    def get_event_with_conditions(self):
        raise NotImplementedError()

    def get_job_object(self, job_state):
        raise NotImplementedError()

    def get_container_name(self):
        raise NotImplementedError()

    def test_handle_k8s_events_job_statuses_for_non_existing_job(self):
        assert self.STATUS_MODEL.objects.count() == 0
        job_state = get_job_state(
            event_type=self.get_event()['type'],  # pylint:disable=unsubscriptable-object
            event=self.get_event()['object'],  # pylint:disable=unsubscriptable-object
            created_at=timezone.now() + datetime.timedelta(days=1),
            job_container_names=(self.get_container_name(),),
            experiment_type_label=conf.get(TYPE_LABELS_RUNNER))
        self.STATUS_HANDLER(job_state.to_dict())  # pylint:disable=not-callable
        assert self.STATUS_MODEL.objects.count() == 0

    def test_handle_k8s_events_job_statuses_for_existing_job_with_unknown_conditions(self):
        assert self.STATUS_MODEL.objects.count() == 0
        job_state = get_job_state(
            event_type=self.get_event()['type'],  # pylint:disable=unsubscriptable-object
            event=self.get_event()['object'],  # pylint:disable=unsubscriptable-object
            created_at=timezone.now() + datetime.timedelta(days=1),
            job_container_names=(self.get_container_name(),),
            experiment_type_label=conf.get(TYPE_LABELS_RUNNER))

        job = self.get_job_object(job_state)

        self.STATUS_HANDLER(job_state.to_dict())  # pylint:disable=not-callable
        assert self.STATUS_MODEL.objects.count() == 2
        statuses = self.STATUS_MODEL.objects.filter(job=job).values_list('status', flat=True)
        assert set(statuses) == {JobLifeCycle.CREATED, JobLifeCycle.UNKNOWN}

    def test_handle_k8s_events_job_statuses_for_existing_job_with_known_conditions(self):
        assert self.STATUS_MODEL.objects.count() == 0
        job_state = get_job_state(
            event_type=self.get_event_with_conditions()['type'],  # pylint:disable=unsubscriptable-object
            event=self.get_event_with_conditions()['object'],  # pylint:disable=unsubscriptable-object
            created_at=timezone.now() + datetime.timedelta(days=1),
            job_container_names=(self.get_container_name(),),
            experiment_type_label=conf.get(TYPE_LABELS_RUNNER))

        job = self.get_job_object(job_state)

        self.STATUS_HANDLER(job_state.to_dict())  # pylint:disable=not-callable
        assert self.STATUS_MODEL.objects.count() == 2
        statuses = self.STATUS_MODEL.objects.filter(job=job).values_list('status', flat=True)
        assert set(statuses) == {JobLifeCycle.CREATED, JobLifeCycle.FAILED}


@pytest.mark.monitors_mark
class TestEventsExperimentJobsStatusesHandling(TestEventsBaseJobsStatusesHandling):
    STATUS_MODEL = ExperimentJobStatus
    STATUS_HANDLER = k8s_events_handle_experiment_job_statuses

    def get_event(self):
        return status_experiment_job_event

    def get_event_with_conditions(self):
        return status_experiment_job_event_with_conditions

    def get_job_object(self, job_state):
        job_uuid = job_state.details.labels.job_uuid.hex
        return ExperimentJobFactory(uuid=job_uuid)

    def get_container_name(self):
        return conf.get(CONTAINER_NAME_EXPERIMENT_JOBS)


@pytest.mark.monitors_mark
class TestEventsJobsStatusesHandling(TestEventsBaseJobsStatusesHandling):
    STATUS_MODEL = JobStatus
    STATUS_HANDLER = k8s_events_handle_job_statuses

    def get_event(self):
        return status_job_event

    def get_event_with_conditions(self):
        return status_job_event_with_conditions

    def get_job_object(self, job_state):
        job_uuid = job_state.details.labels.job_uuid.hex
        with patch('scheduler.tasks.jobs.jobs_build.apply_async') as _:  # noqa
            return JobFactory(uuid=job_uuid)

    def get_container_name(self):
        return conf.get(CONTAINER_NAME_JOBS)


@pytest.mark.monitors_mark
class TestEventsTensorboardJobsStatusesHandling(TestEventsBaseJobsStatusesHandling):
    STATUS_MODEL = TensorboardJobStatus
    STATUS_HANDLER = k8s_events_handle_plugin_job_statuses

    def get_event(self):
        return status_tensorboard_job_event

    def get_event_with_conditions(self):
        return status_tensorboard_job_event_with_conditions

    def get_job_object(self, job_state):
        project_uuid = job_state.details.labels.project_uuid.hex
        project = ProjectFactory(uuid=project_uuid)
        job_uuid = job_state.details.labels.job_uuid.hex
        return TensorboardJobFactory(uuid=job_uuid, project=project)

    def get_container_name(self):
        return conf.get(CONTAINER_NAME_PLUGIN_JOBS)


@pytest.mark.monitors_mark
class TestEventsNotebookJobsStatusesHandling(TestEventsBaseJobsStatusesHandling):
    STATUS_MODEL = NotebookJobStatus
    STATUS_HANDLER = k8s_events_handle_plugin_job_statuses

    def get_event(self):
        return status_notebook_job_event

    def get_event_with_conditions(self):
        return status_notebook_job_event_with_conditions

    def get_job_object(self, job_state):
        project_uuid = job_state.details.labels.project_uuid.hex
        project = ProjectFactory(uuid=project_uuid)
        job_uuid = job_state.details.labels.job_uuid.hex
        return NotebookJobFactory(uuid=job_uuid, project=project)

    def get_container_name(self):
        return conf.get(CONTAINER_NAME_PLUGIN_JOBS)


@pytest.mark.monitors_mark
class TestEventsDockerizerJobsStatusesHandling(TestEventsBaseJobsStatusesHandling):
    STATUS_MODEL = BuildJobStatus
    STATUS_HANDLER = k8s_events_handle_build_job_statuses

    def get_event(self):
        return status_build_job_event

    def get_event_with_conditions(self):
        return status_build_job_event_with_conditions

    def get_job_object(self, job_state):
        project_uuid = job_state.details.labels.project_uuid.hex
        project = ProjectFactory(uuid=project_uuid)
        job_uuid = job_state.details.labels.job_uuid.hex

        return BuildJobFactory(uuid=job_uuid, project=project)

    def get_container_name(self):
        return conf.get(CONTAINER_NAME_BUILD_JOBS)


# Prevent this base class from running tests
del TestEventsBaseJobsStatusesHandling
