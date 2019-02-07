import jinja2
import logging
import os
import stat

from typing import Any, List, Optional, Tuple

from hestia.list_utils import to_list
from hestia.paths import delete_path

import conf

from docker_images.image_info import get_project_image_name, get_project_tagged_image
from dockerizer.init.dockerfile import POLYAXON_DOCKER_TEMPLATE
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks

_logger = logging.getLogger('polyaxon.dockerizer')


class DockerFileGenerator(object):
    LATEST_IMAGE_TAG = 'latest'
    WORKDIR = '/code'
    HEART_BEAT_INTERVAL = 60

    def __init__(self,
                 build_job: 'BuildJob',
                 repo_path: str,
                 from_image: str,
                 copy_code: bool = True,
                 build_steps: Optional[List[str]] = None,
                 env_vars: Optional[List[Tuple[str, str]]] = None,
                 dockerfile_name: str = 'Dockerfile') -> None:
        self.build_job = build_job
        self.job_uuid = build_job.uuid.hex
        self.job_name = build_job.unique_name
        self.from_image = from_image
        self.image_name = get_project_image_name(project_name=self.build_job.project.name,
                                                 project_id=self.build_job.project.id)
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
        # Clean dockerfile
        delete_path(self.dockerfile_path)

    def _get_requirements_path(self) -> Optional[str]:
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

    def render(self) -> str:
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


def generate(build_job: 'BuildJob', build_path: str) -> bool:
    """Build necessary code for a job to run"""
    _logger.info('Generating dockerfile ...')
    # Build the image
    dockerfile_generator = DockerFileGenerator(
        build_job=build_job,
        repo_path=build_path,
        from_image=build_job.image,
        build_steps=build_job.build_steps,
        env_vars=build_job.env_vars)

    # Create DockerFile
    with open(dockerfile_generator.dockerfile_path, 'w') as dockerfile:
        rendered_dockerfile = dockerfile_generator.render()
        celery_app.send_task(
            SchedulerCeleryTasks.BUILD_JOBS_SET_DOCKERFILE,
            kwargs={'build_job_uuid': dockerfile_generator.job_uuid,
                    'dockerfile': rendered_dockerfile})
        dockerfile.write(rendered_dockerfile)
    return True
