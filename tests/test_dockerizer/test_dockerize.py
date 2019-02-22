import os

from pathlib import Path

import pytest

import conf

from dockerizer.dockerizer.initializer.generate import DockerFileGenerator
from factories.factory_build_jobs import BuildJobFactory
from tests.utils import BaseTest


@pytest.mark.dockerizer_mark
class TestDockerize(BaseTest):
    def test_get_requirements_and_setup_path_works_as_expected(self):
        build_job = BuildJobFactory()
        # Create a repo folder
        repo_path = os.path.join(conf.get('REPOS_MOUNT_PATH'), 'repo')
        os.mkdir(repo_path)

        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      build_steps=build_job.build_steps,
                                      env_vars=build_job.build_env_vars)
        assert builder.polyaxon_requirements_path is None
        assert builder.polyaxon_setup_path is None
        builder.clean()

        # Add a polyaxon_requirements.txt and polyaxon_setup.sh files to repo path
        Path(os.path.join(repo_path, 'polyaxon_requirements.txt')).touch()
        Path(os.path.join(repo_path, 'polyaxon_setup.sh')).touch()

        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      build_steps=build_job.build_steps,
                                      env_vars=build_job.build_env_vars)
        assert builder.polyaxon_requirements_path == 'repo/polyaxon_requirements.txt'
        assert builder.polyaxon_setup_path == 'repo/polyaxon_setup.sh'
        builder.clean()

        # Delete previous files
        os.remove(os.path.join(repo_path, 'polyaxon_requirements.txt'))
        os.remove(os.path.join(repo_path, 'polyaxon_setup.sh'))

        # Add a requirements.txt and setup.sh files to repo path
        Path(os.path.join(repo_path, 'requirements.txt')).touch()
        Path(os.path.join(repo_path, 'setup.sh')).touch()

        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      build_steps=build_job.build_steps,
                                      env_vars=build_job.build_env_vars)
        assert builder.polyaxon_requirements_path == 'repo/requirements.txt'
        assert builder.polyaxon_setup_path == 'repo/setup.sh'
        builder.clean()

        # Add a conda_env.yaml
        Path(os.path.join(repo_path, 'conda_env.yaml')).touch()
        Path(os.path.join(repo_path, 'polyaxon_setup.sh')).touch()

        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      build_steps=build_job.build_steps,
                                      env_vars=build_job.build_env_vars)
        assert builder.polyaxon_conda_env_path == 'repo/conda_env.yaml'
        assert builder.polyaxon_setup_path == 'repo/polyaxon_setup.sh'
        builder.clean()

    def test_render_works_as_expected(self):
        build_job = BuildJobFactory()

        # Create a repo folder
        repo_path = os.path.join(conf.get('REPOS_MOUNT_PATH'), 'repo')
        os.mkdir(repo_path)

        # By default it should user FROM image declare WORKDIR and COPY code
        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      build_steps=build_job.build_steps,
                                      env_vars=build_job.build_env_vars)

        dockerfile = builder.render()
        builder.clean()

        assert 'FROM busybox' in dockerfile
        assert 'WORKDIR {}'.format(builder.WORKDIR) in dockerfile
        assert 'COPY {}'.format(builder.folder_name) in dockerfile

        # Add env vars
        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      build_steps=build_job.build_steps,
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

        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      env_vars=build_job.build_env_vars,
                                      build_steps=build_steps)

        dockerfile = builder.render()
        assert 'COPY {} {}'.format(
            builder.polyaxon_requirements_path, builder.WORKDIR) in dockerfile
        assert 'COPY {} {}'.format(
            builder.polyaxon_setup_path, builder.WORKDIR) in dockerfile

        assert 'RUN {}'.format(build_steps[0]) in dockerfile
        assert 'RUN {}'.format(build_steps[1]) in dockerfile
        builder.clean()

        # Add conda env
        Path(os.path.join(repo_path, 'conda_env.yml')).touch()
        build_steps.append('conda env update -n base -f environment.yml')
        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      env_vars=build_job.build_env_vars,
                                      build_steps=build_steps)

        dockerfile = builder.render()
        assert 'COPY {} {}'.format(
            builder.polyaxon_requirements_path, builder.WORKDIR) in dockerfile
        assert 'COPY {} {}'.format(
            builder.polyaxon_setup_path, builder.WORKDIR) in dockerfile
        assert 'COPY {} {}'.format(
            builder.polyaxon_conda_env_path, builder.WORKDIR) in dockerfile

        assert 'RUN {}'.format(build_steps[0]) in dockerfile
        assert 'RUN {}'.format(build_steps[1]) in dockerfile
        builder.clean()
