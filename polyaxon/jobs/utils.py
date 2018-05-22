import logging

from models.repos import ExternalRepo

logger = logging.getLogger('polyaxon.jobs.utils')


def get_job_repo_path(job, project):
    job_spec = job.specification
    if job_spec.run_exec.git:  # We need to fetch the repo first
        try:
            repo = ExternalRepo.objects.get(project=project,
                                            git_url=job_spec.run_exec.git)
        except ExternalRepo.DoesNotExist:
            logger.error(
                'Something went wrong, '
                'the external repo `%s` was not found', job_spec.run_exec.git)
            raise ValueError('Repo was not found for `{}`.'.format(job_spec.run_exec.git))

        repo_path = repo.path
    else:
        repo_path = project.repo.path
    return repo_path
