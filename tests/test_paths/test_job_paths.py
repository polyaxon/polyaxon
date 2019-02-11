import os

import pytest

import stores

from factories.factory_jobs import JobFactory
from scheduler.tasks.storage import stores_schedule_logs_deletion, stores_schedule_outputs_deletion
from tests.utils import BaseTest


@pytest.mark.paths_mark
class TestJobPaths(BaseTest):
    def test_job_logs_path_creation_deletion(self):
        job = JobFactory()
        job_logs_path = stores.get_job_logs_path(job_name=job.unique_name, temp=False)
        stores.create_job_logs_path(job_name=job.unique_name, temp=False)
        open(job_logs_path, '+w')
        # Should be true, created by the signal
        assert os.path.exists(job_logs_path) is True
        stores_schedule_logs_deletion(persistence=None, subpath=job.subpath)
        assert os.path.exists(job_logs_path) is False

    def test_job_outputs_path_creation_deletion(self):
        job = JobFactory()
        stores.create_job_outputs_path(
            persistence=job.persistence_outputs,
            job_name=job.unique_name)
        job_outputs_path = stores.get_job_outputs_path(
            persistence=job.persistence_outputs,
            job_name=job.unique_name)
        assert os.path.exists(job_outputs_path) is True
        stores_schedule_outputs_deletion(persistence='outputs', subpath=job.subpath)
        assert os.path.exists(job_outputs_path) is False
