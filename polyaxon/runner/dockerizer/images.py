import logging

from django.conf import settings

from repos.models import ExternalRepo
from runner.dockerizer.builders.notebooks import NotebookDockerBuilder

logger = logging.getLogger('polyaxon.dockerizer.images')


def get_experiment_image_info(experiment):
    """Return the image name and image tag for an experiment"""
    project_name = experiment.project.name
    experiment_spec = experiment.specification
    if experiment_spec.run_exec.git:

        try:
            repo = ExternalRepo.objects.get(project=experiment.project,
                                            git_url=experiment_spec.run_exec.git)
        except ExternalRepo.DoesNotExist:
            logger.error(
                'Something went wrong, the external repo `%s` was not found',
                experiment_spec.run_exec.git)
            raise ValueError('Repo was not found for `{}`.'.format(experiment_spec.run_exec.git))

        repo_name = repo.name
    else:
        repo_name = project_name

    image_name = '{}/{}'.format(settings.REGISTRY_HOST, repo_name)
    image_tag = experiment.code_reference.commit
    return image_name, image_tag


def get_job_image_info(project, job):
    """Return the image name and image tag for a job"""
    project_name = project.name
    job_spec = job.specification
    if job_spec.run_exec.git:

        try:
            repo = ExternalRepo.objects.get(project=project,
                                            git_url=job_spec.run_exec.git)
        except ExternalRepo.DoesNotExist:
            logger.error(
                'Something went wrong, the external repo `%s` was not found',
                job_spec.run_exec.git)
            raise ValueError('Repo was not found for `{}`.'.format(job_spec.run_exec.git))

        repo_name = repo.name
        last_commit = repo.last_commit
    else:
        repo_name = project_name
        last_commit = project.repo.last_commit

    image_name = '{}/{}'.format(settings.REGISTRY_HOST, repo_name)
    if not last_commit:
        raise ValueError('Repo was not found for project `{}`.'.format(project))
    return image_name, last_commit[0]


def get_notebook_image_info(project, job):
    """Return the image name and image tag for a job"""
    image_name, _ = get_job_image_info(project, job)
    return image_name, NotebookDockerBuilder.LATEST_IMAGE_TAG
