import pytest

from factories.factory_build_jobs import BuildJobFactory
from scheduler.tasks.build_jobs import build_jobs_set_dockerfile
from tests.utils import BaseTest


@pytest.mark.build_jobs_mark
class TestBuildJobModels(BaseTest):
    DISABLE_RUNNER = True

    def test_set_dockerfile(self):
        build_job = BuildJobFactory()

        assert build_job.dockerfile is None

        build_jobs_set_dockerfile(build_job_uuid=build_job.uuid.hex, dockerfile='dockerfile')

        build_job.refresh_from_db()
        assert build_job.dockerfile == 'dockerfile'
