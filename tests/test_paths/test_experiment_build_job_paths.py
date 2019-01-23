import os

import pytest

import stores

from factories.factory_build_jobs import BuildJobFactory
from scheduler.tasks.storage import stores_schedule_logs_deletion
from tests.utils import BaseTest


@pytest.mark.paths_mark
class TestBuildJobPaths(BaseTest):
    def test_build_job_logs_path_creation_deletion(self):
        job = BuildJobFactory()
        job_logs_path = stores.get_job_logs_path(job_name=job.unique_name, temp=False)
        stores.create_job_logs_path(job_name=job.unique_name, temp=False)
        open(job_logs_path, '+w')
        # Should be true, created by the signal
        assert os.path.exists(job_logs_path) is True
        stores_schedule_logs_deletion(persistence=None, subpath=job.subpath)
        assert os.path.exists(job_logs_path) is False
