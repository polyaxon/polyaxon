# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from django.conf import settings

from dockerizer.builders.base import BaseDockerBuilder
from events import publisher
from experiments.utils import is_experiment_still_running
from libs.registry import get_registry_host
from repos import git
from repos.models import Repo, ExternalRepo
from spawners.utils.constants import ExperimentLifeCycle


logger = logging.getLogger('polyaxon.dockerizer.builders')


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
                 steps=None,
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
            steps=steps,
            env_vars=env_vars,
            dockerfile_name=dockerfile_name)

    def _handle_logs(self, log_line):
        publisher.publish_log(
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
                logger.info('Experiment `{}` is not running, stopping build'.format(
                    self.experiment_name))
                return check_pulse, True
            else:
                check_pulse = 0
        return check_pulse, False


def get_experiment_repo_info(experiment):
    """Returns information required to create a build for an experiment."""
    project_name = experiment.project.name
    experiment_spec = experiment.compiled_spec
    if experiment_spec.run_exec.git:  # We need to fetch the repo first

        repo, is_created = ExternalRepo.objects.get_or_create(project=experiment.project,
                                                              git_url=experiment_spec.run_exec.git)
        if not is_created:
            # If the repo already exist, we just need to refetch it
            git.fetch(git_url=repo.git_url, repo_path=repo.path)
        if not experiment.commit:
            # Update experiment commit if not set already
            experiment.commit = repo.last_commit[0]
            experiment.save()

        repo_path = repo.path
        repo_name = repo.name
    else:
        repo_path = experiment.project.repo.path
        repo_name = project_name

    image_name = '{}/{}'.format(get_registry_host(), repo_name)
    image_tag = experiment.commit
    if not image_tag:
        raise Repo.DoesNotExist(
            'Repo was not found for project `{}`.'.format(experiment.unique_name))
    return {
        'repo_path': repo_path,
        'image_name': image_name,
        'image_tag': image_tag
    }


def build_experiment(experiment, image_tag=None):
    """Build necessary code for an experiment to run"""
    experiment_spec = experiment.compiled_spec
    build_info = get_experiment_repo_info(experiment)

    # Build the image
    docker_builder = ExperimentDockerBuilder(experiment_name=experiment.unique_name,
                                             experiment_uuid=experiment.uuid.hex,
                                             repo_path=build_info['repo_path'],
                                             from_image=experiment_spec.run_exec.image,
                                             image_name=build_info['image_name'],
                                             image_tag=image_tag or build_info['image_tag'],
                                             steps=experiment_spec.run_exec.steps,
                                             env_vars=experiment_spec.run_exec.env_vars)
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
