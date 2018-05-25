import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import publisher

from constants.experiments import ExperimentLifeCycle
from db.getters.experiments import is_experiment_still_running
from db.models.repos import CodeReference, ExternalRepo, Repo
from dockerizer.builders.base import BaseDockerBuilder
from libs.repos import git

_logger = logging.getLogger('polyaxon.dockerizer')


class ExperimentDockerBuilder(BaseDockerBuilder):
    CHECK_INTERVAL = 10

    def __init__(self,
                 experiment_name,
                 experiment_uuid,
                 repo_path,
                 from_image,
                 image_name,
                 image_tag,
                 copy_code=True,
                 in_tmp_repo=True,
                 build_steps=None,
                 env_vars=None,
                 dockerfile_name='Dockerfile'):
        self.experiment_name = experiment_name
        self.experiment_uuid = experiment_uuid
        super(ExperimentDockerBuilder, self).__init__(
            repo_path=repo_path,
            from_image=from_image,
            image_name=image_name,
            image_tag=image_tag,
            copy_code=copy_code,
            in_tmp_repo=in_tmp_repo,
            build_steps=build_steps,
            env_vars=env_vars,
            dockerfile_name=dockerfile_name)

    def _handle_logs(self, log_line):
        publisher.publish_experiment_log(
            log_line=log_line,
            status=ExperimentLifeCycle.BUILDING,
            experiment_uuid=self.experiment_uuid,
            experiment_name=self.experiment_name,
            job_uuid='all',
        )

    def _check_pulse(self, check_pulse):
        check_pulse += 1
        # Check if experiment is not stopped in the meanwhile
        if check_pulse > self.CHECK_INTERVAL:
            if not is_experiment_still_running(experiment_uuid=self.experiment_uuid):
                _logger.info('Experiment `%s` is not running, stopping build', self.experiment_name)
                return check_pulse, True
            else:
                check_pulse = 0
        return check_pulse, False


def get_experiment_repo_info(experiment):
    """Returns information required to create a build for an experiment."""
    project_name = experiment.project.name
    experiment_spec = experiment.specification
    if experiment_spec.run_exec.git:  # We need to fetch the repo first

        repo, is_created = ExternalRepo.objects.get_or_create(project=experiment.project,
                                                              git_url=experiment_spec.run_exec.git)
        if not is_created:
            # If the repo already exist, we just need to refetch it
            git.fetch(git_url=repo.git_url, repo_path=repo.path)
        if not experiment.code_reference.commit:
            # Update experiment commit if not set already
            code_reference, _ = CodeReference.objects.get_or_create(repo=repo,
                                                                    commit=repo.last_commit[0])
            experiment.code_reference = code_reference
            experiment.save()

        repo_path = repo.path
        repo_name = repo.name
    else:
        repo_path = experiment.project.repo.path
        repo_name = project_name

    image_name = '{}/{}'.format(settings.REGISTRY_HOST, repo_name)
    image_tag = experiment.code_reference.commit
    if not image_tag:
        raise Repo.DoesNotExist
    return {
        'repo_path': repo_path,
        'image_name': image_name,
        'image_tag': image_tag
    }


def build_experiment(experiment, image_tag=None):
    """Build necessary code for an experiment to run"""
    experiment_spec = experiment.specification
    build_info = get_experiment_repo_info(experiment)

    # Build the image
    docker_builder = ExperimentDockerBuilder(experiment_name=experiment.unique_name,
                                             experiment_uuid=experiment.uuid.hex,
                                             repo_path=build_info['repo_path'],
                                             from_image=experiment_spec.run_exec.image,
                                             image_name=build_info['image_name'],
                                             image_tag=image_tag or build_info['image_tag'],
                                             build_steps=experiment_spec.run_exec.build_steps,
                                             env_vars=experiment_spec.run_exec.env_vars)
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
            experiment.set_status(ExperimentLifeCycle.FAILED,
                                  message='The docker image could not be pushed.')
        except ObjectDoesNotExist:
            pass
        return False
    docker_builder.clean()
    return True
