import json
import logging
import os
import stat

from typing import Any, List, Optional, Tuple

from docker import APIClient
from docker.errors import APIError, BuildError, DockerException
from hestia.logging_utils import LogLevels

import conf

from constants.jobs import JobLifeCycle
from docker_images.image_info import get_project_image_name, get_project_tagged_image
from dockerizer.constants import BUILD_CONTEXT
from dockerizer.utils import send_status

_logger = logging.getLogger('polyaxon.dockerizer')


class DockerBuilder(object):
    LATEST_IMAGE_TAG = 'latest'
    WORKDIR = '/code'

    def __init__(self,
                 build_job: 'BuildJob',
                 repo_path: str,
                 from_image: str,
                 copy_code: bool = True,
                 dockerfile_name: str = 'Dockerfile') -> None:
        self.build_job = build_job
        self.job_uuid = build_job.uuid.hex
        self.from_image = from_image
        self.image_name = get_project_image_name(project_name=self.build_job.project.name,
                                                 project_id=self.build_job.project.id)
        self.image_tag = self.job_uuid
        self.folder_name = repo_path.split('/')[-1]
        self.repo_path = repo_path
        self.copy_code = copy_code

        self.build_path = '/'.join(self.repo_path.split('/')[:-1])
        self.dockerfile_path = os.path.join(self.build_path, dockerfile_name)
        self.docker = APIClient(version='auto')
        self.registry_host = None
        self.docker_url = None
        self.is_pushing = False

    def get_tagged_image(self) -> str:
        return get_project_tagged_image(project_name=self.build_job.project.name,
                                        project_id=self.build_job.project.id,
                                        image_tag=self.build_job.uuid.hex)

    def check_image(self) -> Any:
        return self.docker.images(self.get_tagged_image())

    def clean(self) -> None:
        pass

    def login_internal_registry(self) -> None:
        try:
            self.docker.login(username=conf.get('REGISTRY_USER'),
                              password=conf.get('REGISTRY_PASSWORD'),
                              registry=conf.get('REGISTRY_HOST'),
                              reauth=True)
        except DockerException as e:
            _logger.exception('Failed to connect to registry %s\n', e)

    def login_private_registries(self) -> None:
        if not conf.get('PRIVATE_REGISTRIES'):
            return

        for registry in conf.get('PRIVATE_REGISTRIES'):
            self.docker.login(username=registry.user,
                              password=registry.password,
                              registry=registry.host,
                              reauth=True)

    def _prepare_log_lines(self, log_line) -> Tuple[List[str], bool]:
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

    def _handle_logs(self, log_lines) -> None:
        for log_line in log_lines:
            print(log_line)

    def _handle_log_stream(self, stream) -> bool:
        log_lines = []
        status = True
        try:
            for log_line in stream:
                new_log_lines, new_status = self._prepare_log_lines(log_line)
                log_lines += new_log_lines
                if not new_status:
                    status = new_status
                self._handle_logs(log_lines)
                log_lines = []
            if log_lines:
                self._handle_logs(log_lines)
        except (BuildError, APIError) as e:
            self._handle_logs('{}: Could not build the image, '
                              'encountered {}'.format(LogLevels.ERROR, e))
            return False

        return status

    def _get_setup_path(self) -> Optional[str]:
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

    def build(self, nocache: bool = False, memory_limit: Any = None) -> bool:
        _logger.debug('Starting build for `%s`', self.repo_path)

        limits = {
            # Disable memory swap for building
            'memswap': -1
        }
        if memory_limit:
            limits['memory'] = memory_limit

        stream = self.docker.build(
            path=self.build_path,
            tag=self.get_tagged_image(),
            forcerm=True,
            rm=True,
            pull=True,
            nocache=nocache,
            container_limits=limits)
        return self._handle_log_stream(stream=stream)

    def push(self) -> bool:
        stream = self.docker.push(self.image_name, tag=self.image_tag, stream=True)
        return self._handle_log_stream(stream=stream)


def build(build_job: 'BuildJob', build_path: str = BUILD_CONTEXT) -> bool:
    """Build necessary code for a job to run"""
    _logger.info('Starting build ...')

    # Build the image
    docker_builder = DockerBuilder(
        build_job=build_job,
        repo_path=build_path,
        from_image=build_job.image)
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
