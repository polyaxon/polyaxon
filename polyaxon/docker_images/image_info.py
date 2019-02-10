import logging

from typing import Any, Tuple

import conf

from constants.images_tags import LATEST_IMAGE_TAG

_logger = logging.getLogger('polyaxon.dockerizer.images')


def get_experiment_image_info(experiment: 'Experiment') -> Tuple[str, str]:
    """Return the image name and image tag for an experiment"""
    project_name = experiment.project.name
    repo_name = project_name

    image_name = '{}/{}'.format(conf.get('REGISTRY_URI'), repo_name)
    image_tag = experiment.code_reference.commit
    return image_name, image_tag


def get_job_image_info(project: 'Project', job: Any) -> Tuple[str, str]:
    """Return the image name and image tag for a job"""
    project_name = project.name
    repo_name = project_name

    image_name = '{}/{}'.format(conf.get('REGISTRY_URI'), repo_name)
    try:
        last_commit = project.repo.last_commit
    except ValueError:
        raise ValueError('Repo was not found for project `{}`.'.format(project))
    return image_name, last_commit[0]


def get_notebook_image_info(project: 'Project', job: Any) -> Tuple[str, str]:
    """Return the image name and image tag for a job"""
    image_name, _ = get_job_image_info(project, job)
    return image_name, LATEST_IMAGE_TAG


def get_image_name(build_job: 'BuildJob', local=True) -> str:
    if conf.get('REGISTRY_IN_CLUSTER'):
        registry = conf.get('REGISTRY_LOCAL_URI') if local else conf.get('REGISTRY_URI')
    else:
        registry = conf.get('REGISTRY_URI')
    return '{}/{}_{}'.format(registry,
                             build_job.project.name.lower(),
                             build_job.project.id)


def get_image_info(build_job: 'BuildJob') -> Tuple[str, str]:
    return get_image_name(build_job=build_job), build_job.uuid.hex


def get_tagged_image(build_job: 'BuildJob') -> str:
    image_name, image_tag = get_image_info(build_job)
    return '{}:{}'.format(image_name, image_tag)
