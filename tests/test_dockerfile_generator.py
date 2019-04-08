# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import tempfile

from pathlib import Path
from unittest import TestCase

from polyaxon_dockgen.generator import DockerFileGenerator


class TestDockerfileGenerator(TestCase):
    def test_get_environment_paths_detection_work_as_expected(self):
        # Create a repo folder
        repo_path = os.path.join(tempfile.mkdtemp(), 'repo')
        os.mkdir(repo_path)

        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      build_steps=None,
                                      env_vars=None)
        assert builder.polyaxon_requirements_path is None
        assert builder.polyaxon_setup_path is None
        builder.clean()

        # Add a polyaxon_requirements.txt and polyaxon_setup.sh files to repo path
        Path(os.path.join(repo_path, 'polyaxon_requirements.txt')).touch()
        Path(os.path.join(repo_path, 'polyaxon_setup.sh')).touch()

        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox')
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
                                      from_image='busybox')
        assert builder.polyaxon_requirements_path == 'repo/requirements.txt'
        assert builder.polyaxon_setup_path == 'repo/setup.sh'
        builder.clean()

        # Add a conda_env.yaml
        Path(os.path.join(repo_path, 'conda_env.yaml')).touch()
        Path(os.path.join(repo_path, 'polyaxon_setup.sh')).touch()

        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox')
        assert builder.polyaxon_conda_env_path == 'repo/conda_env.yaml'
        assert builder.polyaxon_setup_path == 'repo/polyaxon_setup.sh'
        builder.clean()

    def test_render_works_as_expected(self):
        # Create a repo folder
        repo_path = os.path.join(tempfile.mkdtemp(), 'repo')
        os.mkdir(repo_path)

        # By default it should use FROM image declare WORKDIR and COPY code
        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox')

        dockerfile = builder.render()
        builder.clean()

        assert 'FROM busybox' in dockerfile
        assert 'WORKDIR {}'.format(builder.WORKDIR) in dockerfile
        assert 'COPY {}'.format(builder.folder_name) in dockerfile

        # Add env vars
        builder = DockerFileGenerator(repo_path=repo_path,
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

        builder = DockerFileGenerator(repo_path=repo_path,
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

        # Add conda env
        Path(os.path.join(repo_path, 'conda_env.yml')).touch()
        build_steps.append('conda env update -n base -f environment.yml')
        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
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
