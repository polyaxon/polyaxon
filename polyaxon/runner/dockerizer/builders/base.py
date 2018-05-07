import jinja2
import json
import logging
import os
import stat
import time
import uuid

from docker import APIClient
from docker.errors import DockerException

from django.conf import settings

from libs.paths import copy_to_tmp_dir, delete_path, delete_tmp_dir
from libs.utils import get_list
from repos import git
from runner.dockerizer.dockerfile import POLYAXON_DOCKER_TEMPLATE

logger = logging.getLogger('polyaxon.dockerizer.builders')


class BaseDockerBuilder(object):
    CHECK_INTERVAL = 10
    LATEST_IMAGE_TAG = 'latest'
    WORKDIR = '/code'

    def __init__(self,
                 repo_path,
                 from_image,
                 image_name,
                 image_tag,
                 copy_code=True,
                 in_tmp_repo=True,
                 build_steps=None,
                 env_vars=None,
                 dockerfile_name='Dockerfile'):
        # This will help create a unique tmp folder for dockerizer in case of concurrent jobs
        self.uuid = uuid.uuid4().hex
        self.from_image = from_image
        self.image_name = image_name
        self.image_tag = image_tag
        self.repo_path = repo_path
        self.folder_name = repo_path.split('/')[-1]
        self.copy_code = copy_code
        self.in_tmp_repo = in_tmp_repo
        if in_tmp_repo and copy_code:
            self.build_repo_path = self.create_tmp_repo()
        else:
            self.build_repo_path = self.repo_path

        self.build_path = '/'.join(self.build_repo_path.split('/')[:-1])
        self.build_steps = get_list(build_steps)
        self.env_vars = get_list(env_vars)
        self.dockerfile_path = os.path.join(self.build_path, dockerfile_name)
        self.polyaxon_requirements_path = self._get_requirements_path()
        self.polyaxon_setup_path = self._get_setup_path()
        self.docker = APIClient(version='auto')
        self.registry_host = None
        self.docker_url = None

    def get_tagged_image(self):
        return '{}:{}'.format(self.image_name, self.image_tag)

    def create_tmp_repo(self):
        # Create a tmp copy of the repo before starting the build
        return copy_to_tmp_dir(path=self.repo_path,
                               dir_name=os.path.join(self.uuid, self.image_tag, self.folder_name))

    def check_image(self):
        return self.docker.images(self.get_tagged_image())

    def clean(self):
        # Clean dockerfile
        delete_path(self.dockerfile_path)

        # Clean tmp dir if created
        if self.in_tmp_repo and self.copy_code:
            delete_tmp_dir(self.image_tag)

    def login(self, registry_user, registry_password, registry_host):
        try:
            self.docker.login(username=registry_user,
                              password=registry_password,
                              registry=registry_host,
                              reauth=True)
        except DockerException as e:
            logger.exception('Failed to connect to registry %s\n', e)

    def _handle_logs(self, log_line):
        raise NotImplementedError

    def _check_pulse(self, check_pulse):
        """Checks if the job/experiment is still running.

        returns:
          * int: the updated check_pulse (+1) value
          * boolean: if the docker process should stop
        """
        raise NotImplementedError

    def _get_requirements_path(self):
        requirements_path = os.path.join(self.build_repo_path, 'polyaxon_requirements.txt')
        if os.path.isfile(requirements_path):
            return os.path.join(self.folder_name, 'polyaxon_requirements.txt')
        return None

    def _get_setup_path(self):
        setup_file_path = os.path.join(self.build_repo_path, 'polyaxon_setup.sh')
        has_setup = os.path.isfile(setup_file_path)
        if has_setup:
            st = os.stat(setup_file_path)
            os.chmod(setup_file_path, st.st_mode | stat.S_IEXEC)
            return os.path.join(self.folder_name, 'polyaxon_setup.sh')
        return None

    def render(self):
        docker_template = jinja2.Template(POLYAXON_DOCKER_TEMPLATE)
        return docker_template.render(
            from_image=self.from_image,
            polyaxon_requirements_path=self.polyaxon_requirements_path,
            polyaxon_setup_path=self.polyaxon_setup_path,
            build_steps=self.build_steps,
            env_vars=self.env_vars,
            folder_name=self.folder_name,
            workdir=self.WORKDIR,
            nvidia_bin=settings.MOUNT_PATHS_NVIDIA.get('bin'),
            copy_code=self.copy_code
        )

    def build(self, memory_limit=None):
        logger.debug('Starting build in `%s`', self.build_repo_path)
        # Checkout to the correct commit
        if self.image_tag != self.LATEST_IMAGE_TAG:
            git.checkout_commit(repo_path=self.build_repo_path, commit=self.image_tag)

        limits = {
            # Always disable memory swap for building, since mostly
            # nothing good can come of that.
            'memswap': -1
        }
        if memory_limit:
            limits['memory'] = memory_limit

        # Create DockerFile
        with open(self.dockerfile_path, 'w') as dockerfile:
            dockerfile.write(self.render())

        check_pulse = 0
        for log_line in self.docker.build(
            path=self.build_path,
            tag=self.get_tagged_image(),
            buildargs={},
            decode=True,
            forcerm=True,
            rm=True,
            pull=True,
            nocache=False,
            container_limits=limits,
            stream=True,
        ):
            self._handle_logs(log_line)
            # Check if we need to stop this process
            check_pulse, should_stop = self._check_pulse(check_pulse)
            if should_stop:
                return False

        # Checkout back to master
        if self.image_tag != self.LATEST_IMAGE_TAG:
            git.checkout_commit(repo_path=self.build_repo_path)
        return True

    def push(self):
        # Build a progress setup for each layer, and only emit per-layer info every 1.5s
        layers = {}
        last_emit_time = time.time()
        check_pulse = 0
        for log_line in self.docker.push(self.image_name, tag=self.image_tag, stream=True):
            lines = [l for l in log_line.decode('utf-8').split('\r\n') if l]
            lines = [json.loads(l) for l in lines]
            for progress in lines:
                if 'error' in progress:
                    logger.error(progress['error'], extra=dict(phase='failed'))
                    return
                if 'id' not in progress:
                    continue
                if 'progressDetail' in progress and progress['progressDetail']:
                    layers[progress['id']] = progress['progressDetail']
                else:
                    layers[progress['id']] = progress['status']
                if time.time() - last_emit_time > 1.5:
                    logger.debug('Pushing image\n', extra=dict(progress=layers, phase='pushing'))
                    last_emit_time = time.time()

                self._handle_logs(log_line)

                # Check if we need to stop this process
            check_pulse, should_stop = self._check_pulse(check_pulse)
            if should_stop:
                return False

        return True
