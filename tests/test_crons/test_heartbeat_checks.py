import pytest

from mock import patch

from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from crons.tasks.heartbeats import heartbeat_builds, heartbeat_experiments, heartbeat_jobs
from factories.factory_build_jobs import BuildJobFactory, BuildJobStatusFactory
from factories.factory_experiments import ExperimentFactory, ExperimentStatusFactory
from factories.factory_jobs import JobFactory, JobStatusFactory
from tests.utils import BaseTest


@pytest.mark.crons_mark
class TestHeartBeatCrons(BaseTest):
    def test_heartbeat_experiments(self):
        experiment1 = ExperimentFactory()
        ExperimentStatusFactory(experiment=experiment1, status=ExperimentLifeCycle.SCHEDULED)
        experiment2 = ExperimentFactory()
        ExperimentStatusFactory(experiment=experiment2, status=ExperimentLifeCycle.CREATED)
        experiment3 = ExperimentFactory()
        ExperimentStatusFactory(experiment=experiment3, status=ExperimentLifeCycle.FAILED)
        experiment4 = ExperimentFactory()
        ExperimentStatusFactory(experiment=experiment4, status=ExperimentLifeCycle.STARTING)
        experiment5 = ExperimentFactory()
        ExperimentStatusFactory(experiment=experiment5, status=ExperimentLifeCycle.RUNNING)

        with patch('scheduler.tasks.experiments'
                   '.experiments_check_heartbeat.apply_async') as mock_fct:
            heartbeat_experiments()

        assert mock_fct.call_count == 1

    def test_heartbeat_jobs(self):
        job1 = JobFactory()
        JobStatusFactory(job=job1, status=JobLifeCycle.SCHEDULED)
        job2 = JobFactory()
        JobStatusFactory(job=job2, status=JobLifeCycle.CREATED)
        job3 = JobFactory()
        JobStatusFactory(job=job3, status=JobLifeCycle.FAILED)
        job4 = JobFactory()
        JobStatusFactory(job=job4, status=JobLifeCycle.RUNNING)

        with patch('scheduler.tasks.jobs.jobs_check_heartbeat.apply_async') as mock_fct:
            heartbeat_jobs()

        assert mock_fct.call_count == 1

    def test_heartbeat_builds(self):
        build1 = BuildJobFactory()
        BuildJobStatusFactory(job=build1, status=JobLifeCycle.SCHEDULED)
        build2 = BuildJobFactory()
        BuildJobStatusFactory(job=build2, status=JobLifeCycle.CREATED)
        build3 = BuildJobFactory()
        BuildJobStatusFactory(job=build3, status=JobLifeCycle.FAILED)
        build4 = BuildJobFactory()
        BuildJobStatusFactory(job=build4, status=JobLifeCycle.RUNNING)

        with patch('scheduler.tasks.build_jobs.build_jobs_check_heartbeat.apply_async') as mock_fct:
            heartbeat_builds()

        assert mock_fct.call_count == 1
