# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import tempfile

from unittest import TestCase

from polyaxon_dockerizer import constants
from polyaxon_dockerizer.dockerfile import POLYAXON_DOCKERFILE_NAME
from polyaxon_dockerizer.generator import DockerFileGenerator, generate


class TestDockerfileGenerator(TestCase):
    @staticmethod
    def touch(path):
        with open(path, 'w') as f:
            f.write('test')

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
        self.touch(os.path.join(repo_path, 'polyaxon_requirements.txt'))
        self.touch(os.path.join(repo_path, 'polyaxon_setup.sh'))

        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox')
        assert builder.polyaxon_requirements_path == 'repo/polyaxon_requirements.txt'
        assert builder.polyaxon_setup_path == 'repo/polyaxon_setup.sh'
        builder.clean()

        # Delete previous files
        os.remove(os.path.join(repo_path, 'polyaxon_requirements.txt'))
        os.remove(os.path.join(repo_path, 'polyaxon_setup.sh'))

        # Add a requirements.txt and setup.sh files to repo path
        self.touch(os.path.join(repo_path, 'requirements.txt'))
        self.touch(os.path.join(repo_path, 'setup.sh'))

        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox')
        assert builder.polyaxon_requirements_path == 'repo/requirements.txt'
        assert builder.polyaxon_setup_path == 'repo/setup.sh'
        builder.clean()

        # Add a conda_env.yaml
        self.touch(os.path.join(repo_path, 'conda_env.yaml'))
        self.touch(os.path.join(repo_path, 'polyaxon_setup.sh'))

        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox')
        assert builder.polyaxon_conda_env_path == 'repo/conda_env.yaml'
        assert builder.polyaxon_setup_path == 'repo/polyaxon_setup.sh'
        builder.clean()

    def test_render_works_as_expected(self):  # pylint:disable=too-many-statements
        # Create a repo folder
        repo_path = os.path.join(tempfile.mkdtemp(), 'repo')
        os.mkdir(repo_path)

        # By default it should use FROM image declare WORKDIR and COPY code
        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox')

        dockerfile = builder.render
        builder.clean()

        assert 'FROM busybox' in dockerfile
        assert 'WORKDIR {}'.format(constants.WORKDIR) in dockerfile
        assert 'COPY {}'.format(builder.folder_name) in dockerfile

        # No lang env
        assert 'LC_ALL' not in dockerfile
        assert 'LANG' not in dockerfile
        assert 'LANGUAGE' not in dockerfile

        # Add env vars
        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      env_vars=[('BLA', 'BLA')])

        dockerfile = builder.render
        assert 'ENV BLA BLA' in dockerfile
        assert 'groupadd' not in dockerfile
        assert 'useradd' not in dockerfile
        builder.clean()

        # Add a polyaxon_requirements.txt and polyaxon_setup.sh files to repo path
        self.touch(os.path.join(repo_path, 'polyaxon_requirements.txt'))
        self.touch(os.path.join(repo_path, 'polyaxon_setup.sh'))

        # Add step to act on them
        build_steps = [
            'pip install -r polyaxon_requirements.txt',
            './polyaxon_setup.sh'
        ]

        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      build_steps=build_steps)

        dockerfile = builder.render
        assert 'COPY {} {}'.format(
            builder.polyaxon_requirements_path, constants.WORKDIR) in dockerfile
        assert 'COPY {} {}'.format(
            builder.polyaxon_setup_path, constants.WORKDIR) in dockerfile

        assert 'RUN {}'.format(build_steps[0]) in dockerfile
        assert 'RUN {}'.format(build_steps[1]) in dockerfile
        assert 'groupadd' not in dockerfile
        assert 'useradd' not in dockerfile
        builder.clean()

        # Add conda env
        self.touch(os.path.join(repo_path, 'conda_env.yml'))
        build_steps.append('conda env update -n base -f environment.yml')
        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      build_steps=build_steps)

        dockerfile = builder.render
        assert 'COPY {} {}'.format(
            builder.polyaxon_requirements_path, constants.WORKDIR) in dockerfile
        assert 'COPY {} {}'.format(
            builder.polyaxon_setup_path, constants.WORKDIR) in dockerfile
        assert 'COPY {} {}'.format(
            builder.polyaxon_conda_env_path, constants.WORKDIR) in dockerfile

        assert 'RUN {}'.format(build_steps[0]) in dockerfile
        assert 'RUN {}'.format(build_steps[1]) in dockerfile
        assert 'groupadd' not in dockerfile
        assert 'useradd' not in dockerfile
        builder.clean()

        # Add uid but no gid
        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      uid=1000)

        dockerfile = builder.render
        assert 'groupadd' not in dockerfile
        assert 'useradd' not in dockerfile
        builder.clean()

        # Add gid but no uid
        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      gid=1000)

        dockerfile = builder.render
        assert 'groupadd' not in dockerfile
        assert 'useradd' not in dockerfile
        builder.clean()

        # Add uid and gid
        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      uid=1000,
                                      gid=1000)

        dockerfile = builder.render
        assert 'groupadd' in dockerfile
        assert 'useradd' in dockerfile
        builder.clean()

        # Add lan env
        builder = DockerFileGenerator(repo_path=repo_path,
                                      from_image='busybox',
                                      lang_env='en_US.UTF-8')

        dockerfile = builder.render
        assert 'en_US.UTF-8' in dockerfile
        assert 'LC_ALL' in dockerfile
        assert 'LANG' in dockerfile
        assert 'LANGUAGE' in dockerfile
        builder.clean()


class TestGenerate(TestCase):
    def test_generate(self):
        # Create a repo folder
        tmp_path = tempfile.mkdtemp()
        repo_path = os.path.join(tmp_path, 'repo')
        os.mkdir(repo_path)

        assert not os.path.isfile('{}/{}'.format(tmp_path, POLYAXON_DOCKERFILE_NAME))
        generate(
            repo_path=repo_path,
            from_image='from_image',
            build_steps=[],
            env_vars=[],
            nvidia_bin=None,
            lang_env=None,
            uid=100,
            gid=100)
        assert os.path.isfile('{}/{}'.format(tmp_path, POLYAXON_DOCKERFILE_NAME))
