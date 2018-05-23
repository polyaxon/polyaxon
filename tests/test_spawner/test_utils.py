from django.conf import settings

from event_monitors.monitors.statuses import update_job_containers
from db.models.experiments import ExperimentJob
from factories.factory_experiments import ExperimentJobFactory
from constants.jobs import JobLifeCycle
from libs.redis_db import RedisJobContainers
from polyaxon_schemas.experiment import JobStateConfig, PodStateConfig
from runner.spawners.utils.constants import EventTypes, PodConditions, PodLifeCycle
from runner.spawners.utils.jobs import get_job_state
from tests.fixtures import status_experiment_job_event, status_experiment_job_event_with_conditions
from tests.utils import BaseTest


class TestSpawner(BaseTest):
    def test_get_pending_job_state(self):
        job_state = get_job_state(event_type=status_experiment_job_event['type'],
                                  event=status_experiment_job_event['object'],
                                  job_container_names=(settings.CONTAINER_NAME_JOB, ),
                                  experiment_type_label=settings.TYPE_LABELS_EXPERIMENT)

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
                                  event=status_experiment_job_event_with_conditions['object'],
                                  job_container_names=(settings.CONTAINER_NAME_JOB,),
                                  experiment_type_label=settings.TYPE_LABELS_EXPERIMENT)

        assert isinstance(job_state, JobStateConfig)
        assert isinstance(job_state.details, PodStateConfig)
        assert job_state.details.event_type == EventTypes.ADDED
        assert job_state.details.phase == PodLifeCycle.FAILED
        labels = status_experiment_job_event_with_conditions['object']['metadata']['labels']
        assert job_state.details.labels.to_dict() == labels
        assert job_state.details.deletion_timestamp is None
        assert set(job_state.details.pod_conditions.keys()) == set(PodConditions.VALUES)
        assert set(job_state.details.container_statuses.keys()) == {settings.CONTAINER_NAME_JOB, }
        assert job_state.status == JobLifeCycle.FAILED
        assert job_state.message is None

    def test_update_job_containers_with_no_container_statuses(self):
        update_job_containers(event=status_experiment_job_event['object'],
                              status=JobLifeCycle.BUILDING,
                              job_container_name=settings.CONTAINER_NAME_JOB)
        assert len(RedisJobContainers.get_containers()) == 0  # pylint:disable=len-as-condition

    def test_update_job_containers(self):
        update_job_containers(event=status_experiment_job_event_with_conditions['object'],
                              status=JobLifeCycle.BUILDING,
                              job_container_name=settings.CONTAINER_NAME_JOB)
        # Assert it's still 0 because no job was created with that job_uuid
        assert len(RedisJobContainers.get_containers()) == 0  # pylint:disable=len-as-condition

        # Create a job with a specific uuid
        labels = status_experiment_job_event_with_conditions['object']['metadata']['labels']
        ExperimentJobFactory(uuid=labels['job_uuid'])
        job = ExperimentJob.objects.get(uuid=labels['job_uuid'])
        update_job_containers(event=status_experiment_job_event_with_conditions['object'],
                              status=JobLifeCycle.BUILDING,
                              job_container_name=settings.CONTAINER_NAME_JOB)
        # Assert now it has started monitoring the container
        assert len(RedisJobContainers.get_containers()) == 1
        container_id = '539e6a6f4209997094802b0657f90576fe129b7f81697120172836073d9bbd75'
        assert RedisJobContainers.get_containers() == [container_id]
        job_uuid, experiment_uuid = RedisJobContainers.get_job(container_id)
        assert job.uuid.hex == job_uuid
        assert job.experiment.uuid.hex == experiment_uuid
