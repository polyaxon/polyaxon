import os

from pathlib import Path
from unittest.mock import patch

import pytest

from django.conf import settings

from dockerizer.builder import DockerBuilder
from factories.factory_build_jobs import BuildJobFactory
from tests.utils import BaseTest


@pytest.mark.dockerizer_mark
class TestDockerize(BaseTest):
    @patch('dockerizer.builder.APIClient')
    def test_get_requirements_and_setup_path_works_as_expected(self, _):
        build_job = BuildJobFactory()
        # Create a repo folder
        repo_path = os.path.join(settings.REPOS_MOUNT_PATH, 'repo')
        os.mkdir(repo_path)

        builder = DockerBuilder(build_job=build_job,
                                repo_path=repo_path,
                                from_image='busybox')
        assert builder.polyaxon_requirements_path is None
        assert builder.polyaxon_setup_path is None
        builder.clean()

        # Add a polyaxon_requirements.txt and polyaxon_setup.sh files to repo path
        Path(os.path.join(repo_path, 'polyaxon_requirements.txt')).touch()
        Path(os.path.join(repo_path, 'polyaxon_setup.sh')).touch()

        builder = DockerBuilder(build_job=build_job,
                                repo_path=repo_path,
                                from_image='busybox')
        assert builder.polyaxon_requirements_path == 'repo/polyaxon_requirements.txt'
        assert builder.polyaxon_setup_path == 'repo/polyaxon_setup.sh'
        builder.clean()

    @patch('dockerizer.builder.APIClient')
    def test_render_works_as_expected(self, _):
        build_job = BuildJobFactory()

        # Create a repo folder
        repo_path = os.path.join(settings.REPOS_MOUNT_PATH, 'repo')
        os.mkdir(repo_path)

        # By default it should user FROM image declare WORKDIR and COPY code
        builder = DockerBuilder(build_job=build_job,
                                repo_path=repo_path,
                                from_image='busybox')

        dockerfile = builder.render()
        builder.clean()

        assert 'FROM busybox' in dockerfile
        assert 'WORKDIR {}'.format(builder.WORKDIR) in dockerfile
        assert 'COPY {}'.format(builder.folder_name) in dockerfile

        # Add env vars
        builder = DockerBuilder(build_job=build_job,
                                repo_path=repo_path,
                                from_image='busybox',
                                env_vars=[('BLA', 'BLA')])

        dockerfile = builder.render()
        assert 'ENV BLA BLA' in dockerfile
        builder.clean()

        # Add a polyaxon_requirements.txt and polyaxon_setup.sh files to repo path
        Path(os.path.join(repo_path, 'polyaxon_requirements.txt')).touch()
        Path(os.path.join(repo_path, 'polyaxon_setup.sh')).touch()
        # Add step to act on them
        build_steps = [
            'pip install -r polyaxon_requirements.txt',
            './polyaxon_setup.sh'
        ]

        builder = DockerBuilder(build_job=build_job,
                                repo_path=repo_path,
                                from_image='busybox',
                                build_steps=build_steps)

        dockerfile = builder.render()
        assert 'COPY {} {}'.format(
            builder.polyaxon_requirements_path, builder.WORKDIR) in dockerfile
        assert 'COPY {} {}'.format(
            builder.polyaxon_setup_path, builder.WORKDIR) in dockerfile

        assert 'RUN {}'.format(build_steps[0]) in dockerfile
        assert 'RUN {}'.format(build_steps[1]) in dockerfile
        builder.clean()
