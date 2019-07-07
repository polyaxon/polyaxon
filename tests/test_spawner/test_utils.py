import pytest

from django.utils import timezone

import conf

from constants.pods import EventTypes, PodConditions
from db.models.experiment_jobs import ExperimentJob
from db.redis.containers import RedisJobContainers
from factories.factory_experiments import ExperimentJobFactory
from lifecycles.jobs import JobLifeCycle
from monitor_statuses.jobs import get_job_state
from monitor_statuses.monitor import update_job_containers
from monitor_statuses.schemas import JobStateConfig, PodStateConfig
from options.registry.container_names import CONTAINER_NAME_EXPERIMENT_JOBS
from options.registry.spawner import TYPE_LABELS_RUNNER
from schemas import PodLifeCycle
from tests.base.case import BaseTest
from tests.fixtures import status_experiment_job_event, status_experiment_job_event_with_conditions


@pytest.mark.spawner_mark
class TestSpawner(BaseTest):
    def test_get_pending_job_state(self):
        job_state = get_job_state(
            event_type=status_experiment_job_event['type'],
            created_at=timezone.now(),
            event=status_experiment_job_event['object'],
            job_container_names=(conf.get(CONTAINER_NAME_EXPERIMENT_JOBS),),
            experiment_type_label=conf.get(TYPE_LABELS_RUNNER))

        assert isinstance(job_state, JobStateConfig)
        assert isinstance(job_state.details, PodStateConfig)
        assert job_state.details.event_type == EventTypes.ADDED
        assert job_state.details.phase == PodLifeCycle.PENDING
        assert job_state.details.labels.to_dict() == status_experiment_job_event[
            'object']['metadata']['labels']
        assert job_state.details.deletion_timestamp is None
        assert job_state.details.pod_conditions is None
        assert job_state.details.container_statuses == {}
        assert job_state.status == JobLifeCycle.UNKNOWN
        assert job_state.message == 'Unknown pod conditions'

    def test_get_failed_job_state(self):
        job_state = get_job_state(event_type=status_experiment_job_event_with_conditions['type'],
                                  created_at=timezone.now(),
                                  event=status_experiment_job_event_with_conditions['object'],
                                  job_container_names=(conf.get(CONTAINER_NAME_EXPERIMENT_JOBS),),
                                  experiment_type_label=conf.get(TYPE_LABELS_RUNNER))

        assert isinstance(job_state, JobStateConfig)
        assert isinstance(job_state.details, PodStateConfig)
        assert job_state.details.event_type == EventTypes.ADDED
        assert job_state.details.phase == PodLifeCycle.FAILED
        labels = status_experiment_job_event_with_conditions['object']['metadata']['labels']
        assert job_state.details.labels.to_dict() == labels
        assert job_state.details.deletion_timestamp is None
        assert set(job_state.details.pod_conditions.keys()) == set(PodConditions.VALUES)
        assert set(job_state.details.container_statuses.keys()) == {
            conf.get(CONTAINER_NAME_EXPERIMENT_JOBS), }
        assert job_state.status == JobLifeCycle.FAILED
        assert job_state.message is not None

    def test_update_job_containers_with_no_container_statuses(self):
        update_job_containers(event=status_experiment_job_event['object'],
                              status=JobLifeCycle.BUILDING,
                              job_container_name=conf.get(CONTAINER_NAME_EXPERIMENT_JOBS))
        assert len(RedisJobContainers().get_containers()) == 0  # pylint:disable=len-as-condition

    def test_update_job_containers(self):
        update_job_containers(event=status_experiment_job_event_with_conditions['object'],
                              status=JobLifeCycle.BUILDING,
                              job_container_name=conf.get(CONTAINER_NAME_EXPERIMENT_JOBS))
        # Assert it's still 0 because no job was created with that job_uuid
        assert len(RedisJobContainers().get_containers()) == 0  # pylint:disable=len-as-condition

        # Create a job with a specific uuid
        labels = status_experiment_job_event_with_conditions['object']['metadata']['labels']
        ExperimentJobFactory(uuid=labels['job_uuid'])
        job = ExperimentJob.objects.get(uuid=labels['job_uuid'])
        update_job_containers(event=status_experiment_job_event_with_conditions['object'],
                              status=JobLifeCycle.BUILDING,
                              job_container_name=conf.get(CONTAINER_NAME_EXPERIMENT_JOBS))
        # Assert now it has started monitoring the container
        assert len(RedisJobContainers().get_containers()) == 1
        container_id = '539e6a6f4209997094802b0657f90576fe129b7f81697120172836073d9bbd75'
        assert RedisJobContainers().get_containers() == [container_id]
        job_uuid, experiment_uuid = RedisJobContainers().get_job(container_id)
        assert job.uuid.hex == job_uuid
        assert job.experiment.uuid.hex == experiment_uuid
