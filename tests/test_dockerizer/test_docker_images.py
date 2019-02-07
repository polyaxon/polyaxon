import pytest

import conf

from docker_images.image_info import (
    get_image_info,
    get_image_name,
    get_project_image_info,
    get_project_image_name,
    get_project_tagged_image,
    get_tagged_image
)
from factories.factory_build_jobs import BuildJobFactory
from tests.utils import BaseTest


@pytest.mark.dockerizer_mark
class TestDockerImageInfo(BaseTest):
    def setUp(self):
        super().setUp()
        self.build_job = BuildJobFactory()

    def test_get_image_name(self):
        image_name = get_image_name(self.build_job)
        project_image_name = get_project_image_name(project_name=self.build_job.project.name,
                                                    project_id=self.build_job.project.id)
        expected_name = '{}/{}_{}'.format(conf.get('REGISTRY_HOST'),
                                          self.build_job.project.name,
                                          self.build_job.project.id)
        assert image_name == expected_name
        assert project_image_name == expected_name

    def test_get_image_image_info(self):
        image_info = get_image_info(self.build_job)
        project_image_name = get_project_image_info(project_name=self.build_job.project.name,
                                                    project_id=self.build_job.project.id,
                                                    image_tag=self.build_job.uuid.hex)
        assert image_info[0] == get_image_name(self.build_job)
        assert image_info[1] == self.build_job.uuid.hex
        assert project_image_name[0] == get_image_name(self.build_job)
        assert project_image_name[1] == self.build_job.uuid.hex

    def test_get_tagged_image(self):
        tagged_image = get_tagged_image(self.build_job)
        project_tagged_image = get_project_tagged_image(project_name=self.build_job.project.name,
                                                        project_id=self.build_job.project.id,
                                                        image_tag=self.build_job.uuid.hex)
        image_name = get_image_info(self.build_job)
        assert tagged_image == ':'.join(image_name)
        assert project_tagged_image == ':'.join(image_name)
