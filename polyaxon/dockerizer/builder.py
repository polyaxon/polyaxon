import jinja2
import json
import logging
import os
import stat
from docker import APIClient
from docker.errors import DockerException, BuildError, APIError

from django.conf import settings

import publisher

from constants.jobs import JobLifeCycle
from docker_images.image_info import get_image_name, get_tagged_image
from dockerizer.dockerfile import POLYAXON_DOCKER_TEMPLATE
from libs.http import download, untar_file
from libs.paths.utils import delete_path
from libs.repos import git
from libs.utils import get_list
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import EventsCeleryTasks

_logger = logging.getLogger('polyaxon.dockerizer')


class DockerBuilder(object):
    LATEST_IMAGE_TAG = 'latest'
    WORKDIR = '/code'

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
        self.build_steps = get_list(build_steps)
        self.env_vars = get_list(env_vars)
        self.dockerfile_path = os.path.join(self.build_path, dockerfile_name)
        self.polyaxon_requirements_path = self._get_requirements_path()
        self.polyaxon_setup_path = self._get_setup_path()
        self.docker = APIClient(version='auto')
        self.registry_host = None
        self.docker_url = None

    def get_tagged_image(self):
        return get_tagged_image(self.build_job)

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

    def _prepare_log_lines(self, log_line):
        raw = log_line.decode('utf-8').strip()
        raw_lines = raw.split('\n')
        log_lines = []
        for raw_line in raw_lines:
            try:
                json_line = json.loads(raw_line)

                if json_line.get('error'):
                    raise BuildError(str(json_line.get('error', json_line)))
                else:
                    if json_line.get('stream'):
                        log_lines.append('Build: {}'.format(json_line['stream'].strip()))
                    elif json_line.get('status'):
                        log_lines.append('Push: {} {}'.format(
                            json_line['status'],
                            json_line.get('progress')
                        ))
                    elif json_line.get('aux'):
                        log_lines.append('Push finished: {}'.format(json_line.get('aux')))
                    else:
                        log_lines.append(str(json_line))
            except json.JSONDecodeError:
                log_lines.append('JSON decode error: {}'.format(raw_line))
        return log_lines

    def _handle_logs(self, log_lines):
        publisher.publish_build_job_log(
            log_lines=log_lines,
            job_uuid=self.job_uuid,
            job_name=self.job_name
        )

    def _handle_log_stream(self, stream):
        log_lines = []
        try:
            for log_line in stream:
                log_lines += self._prepare_log_lines(log_line)
                if len(log_lines) == 50:
                    self._handle_logs(log_lines)
                    log_lines = []
            if log_lines:
                self._handle_logs(log_lines)
        except BuildError as e:
            self._handle_logs('Build Error {}'.format(e))
            return False
        except APIError as e:
            self._handle_logs('Build Error {}'.format(e))
            return False

        return True

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

    def build(self, nocache=False, memory_limit=None):
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

        stream = self.docker.build(
                path=self.build_path,
                tag=self.get_tagged_image(),
                forcerm=True,
                rm=True,
                pull=True,
                nocache=nocache,
                container_limits=limits,
            )
        return self._handle_log_stream(stream=stream)

    def push(self):
        stream = self.docker.push(self.image_name, tag=self.image_tag, stream=True)
        return self._handle_log_stream(stream=stream)


def download_code(build_job, build_path, filename):
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    filename = '{}/{}'.format(build_path, filename)

    if build_job.code_reference.repo:
        download_url = build_job.code_reference.repo.download_url
    elif build_job.code_reference.external_repo:
        download_url = build_job.code_reference.external_repo.download_url
    else:
        raise ValueError('Code reference for this build job does not have any repo.')

    repo_file = download(
        url=download_url,
        filename=filename,
        logger=_logger,
        headers={settings.HEADERS_INTERNAL.replace('_', '-'): 'dockerizer'})
    untar_file(build_path=build_path, filename=filename, logger=_logger, delete_tar=True)
    if not repo_file:
        send_status(build_job=build_job,
                    status=JobLifeCycle.FAILED,
                    message='Could not download code to build the image.')


def build(build_job):
    """Build necessary code for a job to run"""
    build_path = '/tmp/build'
    filename = '_code'
    download_code(build_job=build_job,
                  build_path=build_path,
                  filename=filename)

    _logger.info('Starting build ...')
    # Build the image
    docker_builder = DockerBuilder(
        build_job=build_job,
        repo_path=build_path,
        from_image=build_job.image,
        build_steps=build_job.build_steps,
        env_vars=build_job.env_vars)
    docker_builder.login(registry_user=settings.REGISTRY_USER,
                         registry_password=settings.REGISTRY_PASSWORD,
                         registry_host=settings.REGISTRY_HOST)
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


def send_status(build_job, status, message=None):
    payload = {
        'details': {
            'labels': {
                'app': 'dockerizer',
                'job_uuid': build_job.uuid.hex,
                'job_name': build_job.unique_name
            }
        },
        'status': status,
        'message': message
    }
    celery_app.send_task(
        EventsCeleryTasks.EVENTS_HANDLE_BUILD_JOB_STATUSES,
        kwargs={'payload': payload})
