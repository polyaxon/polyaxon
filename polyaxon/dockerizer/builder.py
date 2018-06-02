import jinja2
import json
import logging
import os
import stat
import time

from docker import APIClient
from docker.errors import DockerException

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import publisher

from constants.jobs import JobLifeCycle
from dockerizer.dockerfile import POLYAXON_DOCKER_TEMPLATE
from libs.http import download
from libs.paths.utils import delete_path
from libs.repos import git
from libs.utils import get_list

_logger = logging.getLogger('polyaxon.dockerizer')


class DockerBuilder(object):
    LATEST_IMAGE_TAG = 'latest'
    WORKDIR = '/code'

    def __init__(self,
                 job_uuid,
                 repo_path,
                 from_image,
                 image_name,
                 image_tag,
                 copy_code=True,
                 build_steps=None,
                 env_vars=None,
                 dockerfile_name='Dockerfile'):
        self.job_uuid = job_uuid
        self.from_image = from_image
        self.image_name = image_name
        self.image_tag = image_tag
        self.folder_name = repo_path.split('/')[-1]
        self.repo_path = repo_path
        self.copy_code = copy_code

        self.build_path = '/'.join(self.repo_path.split('/')[:-1])
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

    def check_image(self):
        return self.docker.images(self.get_tagged_image())

    def clean(self):
        # Clean dockerfile
        delete_path(self.dockerfile_path)

    def login(self, registry_user, registry_password, registry_host):
        try:
            self.docker.login(username=registry_user,
                              password=registry_password,
                              registry=registry_host,
                              reauth=True)
        except DockerException as e:
            _logger.exception('Failed to connect to registry %s\n', e)

    def _handle_logs(self, log_line):
        publisher.publish_build_job_log(
            log_line=log_line,
            job_uuid=self.job_uuid,
        )

    def _get_requirements_path(self):
        requirements_path = os.path.join(self.repo_path, 'polyaxon_requirements.txt')
        if os.path.isfile(requirements_path):
            return os.path.join(self.folder_name, 'polyaxon_requirements.txt')
        return None

    def _get_setup_path(self):
        setup_file_path = os.path.join(self.repo_path, 'polyaxon_setup.sh')
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
        _logger.debug('Starting build in `%s`', self.repo_path)
        # Checkout to the correct commit
        if self.image_tag != self.LATEST_IMAGE_TAG:
            git.checkout_commit(repo_path=self.repo_path, commit=self.image_tag)

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

        return True

    def push(self):
        # Build a progress setup for each layer, and only emit per-layer info every 1.5s
        layers = {}
        last_emit_time = time.time()
        for log_line in self.docker.push(self.image_name, tag=self.image_tag, stream=True):
            lines = [l for l in log_line.decode('utf-8').split('\r\n') if l]
            lines = [json.loads(l) for l in lines]
            for progress in lines:
                if 'error' in progress:
                    _logger.error(progress['error'], extra=dict(phase='failed'))
                    return
                if 'id' not in progress:
                    continue
                if 'progressDetail' in progress and progress['progressDetail']:
                    layers[progress['id']] = progress['progressDetail']
                else:
                    layers[progress['id']] = progress['status']
                if time.time() - last_emit_time > 1.5:
                    _logger.debug('Pushing image\n', extra=dict(progress=layers, phase='pushing'))
                    last_emit_time = time.time()

                self._handle_logs(log_line)

        return True


def download_code(build_job, build_path, filename):
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    download_url = build_job.download_url

    repo_file = download(url=download_url,
                         filename=filename,
                         logger=_logger,
                         headers={settings.HEADERS_INTERNAL: 'dockerizer'},
                         untar=True)
    if not repo_file:
        build_job.set_status(JobLifeCycle.FAILED,
                             message='Could not download code to build the image.')


def build(build_job, image_tag=None):
    """Build necessary code for a job to run"""
    build_path = '/tmp/build'
    filename = 'code'
    download_code(build_job=build_job,
                  build_path=build_path,
                  filename=filename)

    repo_path = '{}/{}'.format(build_path, filename)
    image_name = '{}/{}'.format(settings.REGISTRY_HOST, build_job.project.name)

    # Build the image
    docker_builder = DockerBuilder(
        job_uuid=build_job.uuid.hex,
        repo_path=repo_path,
        from_image=build_job.image,
        image_name=image_name,
        image_tag=image_tag or build_job.code_reference.commit,
        build_steps=build_job.conig.build_steps,
        env_vars=build_job.config.env_vars)
    docker_builder.login(registry_user=settings.REGISTRY_USER,
                         registry_password=settings.REGISTRY_PASSWORD,
                         registry_host=settings.REGISTRY_HOST)
    if docker_builder.check_image():
        # Image already built
        docker_builder.clean()
        return True
    if not docker_builder.build():
        docker_builder.clean()
        return False
    if not docker_builder.push():
        docker_builder.clean()
        try:
            build_job.set_status(JobLifeCycle.FAILED,
                                 message='The docker image could not be pushed.')
        except ObjectDoesNotExist:
            pass
        return False
    docker_builder.clean()
    return True
