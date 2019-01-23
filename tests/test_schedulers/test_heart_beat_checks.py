import pytest

from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from db.redis.heartbeat import RedisHeartBeat
from factories.factory_build_jobs import BuildJobFactory, BuildJobStatusFactory
from factories.factory_experiments import ExperimentFactory, ExperimentStatusFactory
from factories.factory_jobs import JobFactory, JobStatusFactory
from scheduler.tasks.build_jobs import build_jobs_check_heartbeat
from scheduler.tasks.experiments import experiments_check_heartbeat
from scheduler.tasks.jobs import jobs_check_heartbeat
from tests.utils import BaseTest


@pytest.mark.scheduler_mark
class TestHeartBeatChecks(BaseTest):
    def test_experiments_check_heartbeat(self):
        experiment1 = ExperimentFactory()
        ExperimentStatusFactory(experiment=experiment1, status=ExperimentLifeCycle.RUNNING)
        RedisHeartBeat.experiment_ping(experiment_id=experiment1.id)
        experiment2 = ExperimentFactory()
        ExperimentStatusFactory(experiment=experiment2, status=ExperimentLifeCycle.RUNNING)

        experiments_check_heartbeat(experiment1.id)
        experiment1.refresh_from_db()
        self.assertEqual(experiment1.last_status, ExperimentLifeCycle.RUNNING)

        experiments_check_heartbeat(experiment2.id)
        experiment2.refresh_from_db()
        self.assertEqual(experiment2.last_status, ExperimentLifeCycle.FAILED)

    def test_jobs_check_heartbeat(self):
        job1 = JobFactory()
        JobStatusFactory(job=job1, status=JobLifeCycle.RUNNING)
        RedisHeartBeat.job_ping(job_id=job1.id)
        job2 = JobFactory()
        JobStatusFactory(job=job2, status=JobLifeCycle.RUNNING)

        jobs_check_heartbeat(job1.id)
        job1.refresh_from_db()
        self.assertEqual(job1.last_status, JobLifeCycle.RUNNING)

        jobs_check_heartbeat(job2.id)
        job2.refresh_from_db()
        self.assertEqual(job2.last_status, JobLifeCycle.FAILED)

    def test_build_jobs_check_heartbeat(self):
        build1 = BuildJobFactory()
        BuildJobStatusFactory(job=build1, status=JobLifeCycle.RUNNING)
        RedisHeartBeat.build_ping(build_id=build1.id)
        build2 = BuildJobFactory()
        BuildJobStatusFactory(job=build2, status=JobLifeCycle.RUNNING)

        build_jobs_check_heartbeat(build1.id)
        build1.refresh_from_db()
        self.assertEqual(build1.last_status, JobLifeCycle.RUNNING)

        build_jobs_check_heartbeat(build2.id)
        build2.refresh_from_db()
        self.assertEqual(build2.last_status, JobLifeCycle.FAILED)
