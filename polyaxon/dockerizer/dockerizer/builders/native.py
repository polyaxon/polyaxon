import json
import logging
import os

from typing import Any, List, Tuple

from docker import APIClient
from docker.errors import APIError, BuildError, DockerException
from hestia.logging_utils import LogLevels

from . import settings
from .exceptions import BuildException

_logger = logging.getLogger('polyaxon.dockerizer')


class DockerBuilder(object):
    LATEST_IMAGE_TAG = 'latest'
    WORKDIR = '/code'

    def __init__(self,
                 build_context: str,
                 image_name: str,
                 image_tag: str,
                 copy_code: bool = True,
                 dockerfile_name: str = 'Dockerfile') -> None:
        self.image_name = image_name
        self.image_tag = image_tag
        self.copy_code = copy_code

        self.build_context = build_context
        self.dockerfile_path = os.path.join(self.build_context, dockerfile_name)
        self.docker = APIClient(version='auto')
        self.is_pushing = False

    def get_tagged_image(self) -> str:
        return '{}:{}'.format(self.image_name, self.image_tag)

    def check_image(self) -> Any:
        return self.docker.images(self.get_tagged_image())

    def clean(self) -> None:
        pass

    def login_internal_registry(self) -> None:
        try:
            self.docker.login(username=settings.REGISTRY_USER,
                              password=settings.REGISTRY_PASSWORD,
                              registry=settings.REGISTRY_URI,
                              reauth=True)
        except DockerException as e:
            _logger.exception('Failed to connect to registry %s\n', e)

    def login_private_registries(self) -> None:
        if not settings.PRIVATE_REGISTRIES:
            return

        for registry in settings.PRIVATE_REGISTRIES:
            self.docker.login(username=registry.user,
                              password=registry.password,
                              registry=registry.host,
                              reauth=True)

    def _prepare_log_lines(self,  # pylint:disable=too-many-branches
                           log_line) -> Tuple[List[str], bool]:
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

    def build(self, nocache: bool = False, memory_limit: Any = None) -> bool:
        limits = {
            # Disable memory swap for building
            'memswap': -1
        }
        if memory_limit:
            limits['memory'] = memory_limit

        stream = self.docker.build(
            path=self.build_context,
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


def build(build_context: str,
          image_tag: str,
          image_name: str,
          nocache: bool) -> None:
    """Build necessary code for a job to run"""
    _logger.info('Starting build ...')

    # Build the image
    docker_builder = DockerBuilder(
        build_context=build_context,
        image_name=image_name,
        image_tag=image_tag)
    docker_builder.login_internal_registry()
    docker_builder.login_private_registries()
    if docker_builder.check_image():
        # Image already built
        docker_builder.clean()
        return
    if not docker_builder.build(nocache=nocache):
        docker_builder.clean()
        raise BuildException('The docker image could not be built.')
    if not docker_builder.push():
        docker_builder.clean()
        raise BuildException('The docker image could not be pushed.')
    docker_builder.clean()
