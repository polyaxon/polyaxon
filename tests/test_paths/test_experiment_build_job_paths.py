import os

import pytest

from factories.factory_build_jobs import BuildJobFactory
from libs.paths.jobs import (
    create_job_logs_path,
    delete_job_logs,
    get_job_logs_path,
)
from tests.utils import BaseTest


@pytest.mark.paths_mark
class TestBuildJobPaths(BaseTest):
    DISABLE_RUNNER = True

    def test_build_job_logs_path_creation_deletion(self):
        job = BuildJobFactory()
        job_logs_path = get_job_logs_path(job.unique_name)
        create_job_logs_path(job.unique_name)
        open(job_logs_path, '+w')
        # Should be true, created by the signal
        assert os.path.exists(job_logs_path) is True
        delete_job_logs(job.unique_name)
        assert os.path.exists(job_logs_path) is False
