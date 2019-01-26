import jinja2
import json
import logging
import os
import stat
import time

from docker import APIClient
from docker.errors import APIError, BuildError, DockerException
from hestia.list_utils import to_list
from hestia.logging_utils import LogLevels

import conf

from constants.jobs import JobLifeCycle
from db.redis.heartbeat import RedisHeartBeat
from docker_images.image_info import get_image_name, get_tagged_image
from dockerizer.dockerfile import POLYAXON_DOCKER_TEMPLATE
from dockerizer.init.git_download import download_code
from dockerizer.utils import send_status
from libs.paths.utils import delete_path
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks

_logger = logging.getLogger('polyaxon.dockerizer')


class DockerBuilder(object):
    LATEST_IMAGE_TAG = 'latest'
    WORKDIR = '/code'
    HEART_BEAT_INTERVAL = 60

    def __init__(self,
                 build_job,
                 repo_path,
                 from_image,
                 copy_code=True,
                 build_steps=None,
                 env_vars=None,
                 dockerfile_name='Dockerfile'):
        self.build_job = build_job
        self.job_uuid = build_job.uuid.hex
        self.job_name = build_job.unique_name
        self.from_image = from_image
        self.image_name = get_image_name(self.build_job)
        self.image_tag = self.job_uuid
        self.folder_name = repo_path.split('/')[-1]
        self.repo_path = repo_path
        self.copy_code = copy_code

        self.build_path = '/'.join(self.repo_path.split('/')[:-1])
        self.build_steps = to_list(build_steps, check_none=True)
        self.env_vars = to_list(env_vars, check_none=True)
        self.dockerfile_path = os.path.join(self.build_path, dockerfile_name)
        self.polyaxon_requirements_path = self._get_requirements_path()
        self.polyaxon_setup_path = self._get_setup_path()
        self.docker = APIClient(version='auto')
        self.registry_host = None
        self.docker_url = None
        self.is_pushing = False

    def get_tagged_image(self):
        return get_tagged_image(self.build_job)

    def check_image(self):
        return self.docker.images(self.get_tagged_image())

    def clean(self):
        # Clean dockerfile
        delete_path(self.dockerfile_path)

    def login_internal_registry(self):
        try:
            self.docker.login(username=conf.get('REGISTRY_USER'),
                              password=conf.get('REGISTRY_PASSWORD'),
                              registry=conf.get('REGISTRY_HOST'),
                              reauth=True)
        except DockerException as e:
            _logger.exception('Failed to connect to registry %s\n', e)

    def login_private_registries(self):
        if not conf.get('PRIVATE_REGISTRIES'):
            return

        for registry in conf.get('PRIVATE_REGISTRIES'):
            self.docker.login(username=registry.user,
                              password=registry.password,
                              registry=registry.host,
                              reauth=True)

    def _prepare_log_lines(self, log_line):
        raw = log_line.decode('utf-8').strip()
        raw_lines = raw.split('\n')
        log_lines = []
        status = True
        for raw_line in raw_lines:
            try:
                json_line = json.loads(raw_line)

                if json_line.get('error'):
                    log_lines.append('{}: {}'.format(
                        LogLevels.ERROR, str(json_line.get('error', json_line))))
                    status = False
                else:
                    if json_line.get('stream'):
                        log_lines.append('Building: {}'.format(json_line['stream'].strip()))
                    elif json_line.get('status'):
                        if not self.is_pushing:
                            self.is_pushing = True
                            log_lines.append('Pushing ...')
                    elif json_line.get('aux'):
                        log_lines.append('Pushing finished: {}'.format(json_line.get('aux')))
                    else:
                        log_lines.append(str(json_line))
            except json.JSONDecodeError:
                log_lines.append('JSON decode error: {}'.format(raw_line))
        return log_lines, status

    def _handle_logs(self, log_lines):
        for log_line in log_lines:
            print(log_line)

    def _handle_log_stream(self, stream):
        log_lines = []
        last_heart_beat = time.time()
        status = True
        try:
            for log_line in stream:
                new_log_lines, new_status = self._prepare_log_lines(log_line)
                log_lines += new_log_lines
                if not new_status:
                    status = new_status
                self._handle_logs(log_lines)
                log_lines = []
                if time.time() - last_heart_beat > self.HEART_BEAT_INTERVAL:
                    last_heart_beat = time.time()
                    RedisHeartBeat.build_ping(build_id=self.build_job.id)
            if log_lines:
                self._handle_logs(log_lines)
        except (BuildError, APIError) as e:
            self._handle_logs('{}: Could not build the image, '
                              'encountered {}'.format(LogLevels.ERROR, e))
            return False

        return status

    def _get_requirements_path(self):
        def get_requirements(requirements_file):
            requirements_path = os.path.join(self.repo_path, requirements_file)
            if os.path.isfile(requirements_path):
                return os.path.join(self.folder_name, requirements_file)

        requirements = get_requirements('polyaxon_requirements.txt')
        if requirements:
            return requirements

        requirements = get_requirements('requirements.txt')
        if requirements:
            return requirements
        return None

    def _get_setup_path(self):
        def get_setup(setup_file):
            setup_file_path = os.path.join(self.repo_path, setup_file)
            has_setup = os.path.isfile(setup_file_path)
            if has_setup:
                st = os.stat(setup_file_path)
                os.chmod(setup_file_path, st.st_mode | stat.S_IEXEC)
                return os.path.join(self.folder_name, setup_file)

        setup_file = get_setup('polyaxon_setup.sh')
        if setup_file:
            return setup_file

        setup_file = get_setup('setup.sh')
        if setup_file:
            return setup_file
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
            nvidia_bin=conf.get('MOUNT_PATHS_NVIDIA').get('bin'),
            copy_code=self.copy_code
        )

    def build(self, nocache=False, memory_limit=None):
        _logger.debug('Starting build for `%s`', self.repo_path)
        # Checkout to the correct commit
        # if self.image_tag != self.LATEST_IMAGE_TAG:
        #     git.checkout_commit(repo_path=self.repo_path, commit=self.image_tag)

        limits = {
            # Disable memory swap for building
            'memswap': -1
        }
        if memory_limit:
            limits['memory'] = memory_limit

        # Create DockerFile
        with open(self.dockerfile_path, 'w') as dockerfile:
            rendered_dockerfile = self.render()
            celery_app.send_task(
                SchedulerCeleryTasks.BUILD_JOBS_SET_DOCKERFILE,
                kwargs={'build_job_uuid': self.job_uuid, 'dockerfile': rendered_dockerfile})
            dockerfile.write(rendered_dockerfile)

        stream = self.docker.build(
            path=self.build_path,
            tag=self.get_tagged_image(),
            forcerm=True,
            rm=True,
            pull=True,
            nocache=nocache,
            container_limits=limits)
        return self._handle_log_stream(stream=stream)

    def push(self):
        stream = self.docker.push(self.image_name, tag=self.image_tag, stream=True)
        return self._handle_log_stream(stream=stream)


def build(build_job):
    """Build necessary code for a job to run"""
    build_path = '/tmp/build'
    filename = '_code'
    status = download_code(
        build_job=build_job,
        build_path=build_path,
        filename=filename)
    if not status:
        return status

    _logger.info('Starting build ...')
    # Build the image
    docker_builder = DockerBuilder(
        build_job=build_job,
        repo_path=build_path,
        from_image=build_job.image,
        build_steps=build_job.build_steps,
        env_vars=build_job.env_vars)
    docker_builder.login_internal_registry()
    docker_builder.login_private_registries()
    if docker_builder.check_image():
        # Image already built
        docker_builder.clean()
        return True
    nocache = True if build_job.specification.build.nocache is True else False
    if not docker_builder.build(nocache=nocache):
        docker_builder.clean()
        return False
    if not docker_builder.push():
        docker_builder.clean()
        send_status(build_job=build_job,
                    status=JobLifeCycle.FAILED,
                    message='The docker image could not be pushed.')
        return False
    docker_builder.clean()
    return True
