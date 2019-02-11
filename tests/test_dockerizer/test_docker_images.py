import pytest

import conf

from docker_images.image_info import get_image_info, get_image_name, get_tagged_image
from factories.factory_build_jobs import BuildJobFactory
from tests.utils import BaseTest


@pytest.mark.dockerizer_mark
class TestDockerImageInfo(BaseTest):
    def setUp(self):
        super().setUp()
        self.build_job = BuildJobFactory()

    def test_get_image_name(self):
        image_name = get_image_name(self.build_job)
        expected_name = '{}/{}_{}'.format(conf.get('REGISTRY_URI'),
                                          self.build_job.project.name,
                                          self.build_job.project.id)
        assert image_name == expected_name

    def test_get_image_image_info(self):
        image_info = get_image_info(self.build_job)
        assert image_info[0] == get_image_name(self.build_job)
        assert image_info[1] == self.build_job.uuid.hex

    def test_get_tagged_image(self):
        tagged_image = get_tagged_image(self.build_job)
        image_name = get_image_info(self.build_job)
        assert tagged_image == ':'.join(image_name)
