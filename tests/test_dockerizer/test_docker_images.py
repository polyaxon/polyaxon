import pytest

from factories.factory_build_jobs import BuildJobFactory
from registry.image_info import get_image_info, get_image_name
from tests.base.case import BaseTest


@pytest.mark.dockerizer_mark
class TestDockerImageInfo(BaseTest):
    def setUp(self):
        super().setUp()
        self.build_job = BuildJobFactory()

    def test_get_image_name(self):
        host = 'foo'
        image_name = get_image_name(build_job=self.build_job, registry_host=host)
        expected_name = '{}/{}_{}'.format(host,
                                          self.build_job.project.name,
                                          self.build_job.project.id)
        assert image_name == expected_name

    def test_get_image_image_info(self):
        image_info = get_image_info(build_job=self.build_job, registry_host='some_host')
        assert image_info[0] == get_image_name(build_job=self.build_job, registry_host='some_host')
        assert image_info[1] == self.build_job.uuid.hex
