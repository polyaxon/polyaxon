import logging

from django.conf import settings

from dockerizer.builders.base import BaseDockerBuilder
from libs.registry import get_registry_host
from repos import git
from repos.models import Repo, ExternalRepo


logger = logging.getLogger('polyaxon.dockerizer.builders')


class BaseJobDockerBuilder(BaseDockerBuilder):
    CHECK_INTERVAL = 10

    def __init__(self,
                 project_id,
                 project_name,
                 repo_path,
                 from_image,
                 image_name,
                 image_tag,
                 copy_code=True,
                 in_tmp_repo=True,
                 steps=None,
                 env_vars=None,
                 dockerfile_name='Dockerfile'):
        self.project_id = project_id
        self.project_name = project_name
        super(BaseJobDockerBuilder, self).__init__(
            repo_path=repo_path,
            from_image=from_image,
            image_name=image_name,
            image_tag=image_tag,
            copy_code=copy_code,
            in_tmp_repo=in_tmp_repo,
            steps=steps,
            env_vars=env_vars,
            dockerfile_name=dockerfile_name)

    def _handle_logs(self, log_line):
        pass

    def _check_pulse(self, check_pulse):
        pass


def get_job_repo_info(project, job):
    project_name = project.name
    job_spec = job.compiled_spec
    if job_spec.run_exec.git:  # We need to fetch the repo first

        repo, is_created = ExternalRepo.objects.get_or_create(project=project,
                                                              git_url=job_spec.run_exec.git)
        if not is_created:
            # If the repo already exist, we just need to refetch it
            git.fetch(git_url=repo.git_url, repo_path=repo.path)

        repo_path = repo.path
        repo_name = repo.name
        last_commit = repo.last_commit
    else:
        repo_path = project.repo.path
        last_commit = project.repo.last_commit
        repo_name = project_name

    image_name = '{}/{}'.format(get_registry_host(), repo_name)
    if not last_commit:
        raise Repo.DoesNotExist(
            'Repo was not found for project `{}`.'.format(project.unique_name))
    image_tag = last_commit[0]
    return {
        'repo_path': repo_path,
        'image_name': image_name,
        'image_tag': image_tag
    }


def build_job(project, job, job_builder, image_tag=None):
    """Build necessary code for a job to run"""
    job_spec = job.compiled_spec
    build_info = get_job_repo_info(project, job)

    # Build the image
    docker_builder = job_builder(project_id=project.id,
                                 project_name=project.unique_name,
                                 repo_path=build_info['repo_path'],
                                 from_image=job_spec.run_exec.image,
                                 image_name=build_info['image_name'],
                                 image_tag=image_tag or build_info['image_tag'],
                                 steps=job_spec.run_exec.steps,
                                 env_vars=job_spec.run_exec.env_vars)
    docker_builder.login(registry_user=settings.REGISTRY_USER,
                         registry_password=settings.REGISTRY_PASSWORD,
                         registry_host=get_registry_host())
    if not docker_builder.build():
        docker_builder.clean()
        return False
    if not docker_builder.push():
        docker_builder.clean()
        return False
    docker_builder.clean()
    return True
