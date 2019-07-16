# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import jinja2
import os
import stat

from hestia.list_utils import to_list
from polyaxon_dockerizer.dockerfile import POLYAXON_DOCKER_TEMPLATE, POLYAXON_DOCKERFILE_NAME


class DockerFileGenerator(object):
    WORKDIR = '/code'

    def __init__(self,
                 repo_path,
                 from_image,
                 copy_code=True,
                 build_steps=None,
                 env_vars=None,
                 nvidia_bin=None,
                 dockerfile_name=POLYAXON_DOCKERFILE_NAME,
                 lang_env=None,
                 uid=None,
                 gid=None):
        self.from_image = from_image
        self.folder_name = repo_path.split('/')[-1]
        self.repo_path = repo_path
        self.copy_code = copy_code

        self.build_path = '/'.join(self.repo_path.split('/')[:-1])
        self.build_steps = to_list(build_steps, check_none=True)
        self.env_vars = to_list(env_vars, check_none=True)
        self.nvidia_bin = nvidia_bin
        self.dockerfile_path = os.path.join(self.build_path, dockerfile_name)
        self.polyaxon_requirements_path = self._get_requirements_path()
        self.polyaxon_conda_env_path = self._get_conda_env_path()
        self.polyaxon_setup_path = self._get_setup_path()
        self.lang_env = lang_env
        self.uid = uid
        self.gid = gid
        self.is_pushing = False

    def _get_requirements_path(self):
        def get_requirements(requirements_file):
            requirements_path = os.path.join(self.repo_path, requirements_file)
            if os.path.isfile(requirements_path):
                return os.path.join(self.folder_name, requirements_file)
            return None

        requirements = get_requirements('polyaxon_requirements.txt')
        if requirements:
            return requirements

        requirements = get_requirements('requirements.txt')
        if requirements:
            return requirements
        return None

    def _get_conda_env_path(self):  # pylint:disable=too-many-statements
        def get_conda_env(conda_file):
            conda_path = os.path.join(self.repo_path, conda_file)
            if os.path.isfile(conda_path):
                return os.path.join(self.folder_name, conda_file)
            return None

        conda_env = get_conda_env('polyaxon_conda_env.yaml')
        if conda_env:
            return conda_env

        conda_env = get_conda_env('polyaxon_conda_env.yml')
        if conda_env:
            return conda_env

        conda_env = get_conda_env('conda_env.yaml')
        if conda_env:
            return conda_env

        conda_env = get_conda_env('conda_env.yml')
        if conda_env:
            return conda_env
        return None

    def _get_setup_path(self):
        def get_setup(setup_file):
            setup_file_path = os.path.join(self.repo_path, setup_file)
            has_setup = os.path.isfile(setup_file_path)
            if has_setup:
                st = os.stat(setup_file_path)
                os.chmod(setup_file_path, st.st_mode | stat.S_IEXEC)
                return os.path.join(self.folder_name, setup_file)
            return None

        setup_file = get_setup('polyaxon_setup.sh')
        if setup_file:
            return setup_file

        setup_file = get_setup('setup.sh')
        if setup_file:
            return setup_file
        return None

    def clean(self):
        # Clean dockerfile
        if not os.path.exists(self.dockerfile_path):
            return
        os.remove(self.dockerfile_path)

    def render(self):
        docker_template = jinja2.Template(POLYAXON_DOCKER_TEMPLATE)
        return docker_template.render(
            from_image=self.from_image,
            polyaxon_requirements_path=self.polyaxon_requirements_path,
            polyaxon_conda_env_path=self.polyaxon_conda_env_path,
            polyaxon_setup_path=self.polyaxon_setup_path,
            build_steps=self.build_steps,
            env_vars=self.env_vars,
            folder_name=self.folder_name,
            workdir=self.WORKDIR,
            nvidia_bin=self.nvidia_bin,
            copy_code=self.copy_code,
            lang_env=self.lang_env,
            uid=self.uid,
            gid=self.gid,
        )


def generate(repo_path,
             from_image,
             build_steps=None,
             env_vars=None,
             nvidia_bin=None,
             lang_env=None,
             uid=None,
             gid=None):
    # Build the image
    dockerfile_generator = DockerFileGenerator(
        repo_path=repo_path,
        from_image=from_image,
        build_steps=build_steps,
        env_vars=env_vars,
        nvidia_bin=nvidia_bin,
        lang_env=lang_env,
        uid=uid,
        gid=gid)

    # Create DockerFile
    with open(dockerfile_generator.dockerfile_path, 'w') as dockerfile:
        rendered_dockerfile = dockerfile_generator.render()
        dockerfile.write(rendered_dockerfile)
        return rendered_dockerfile
