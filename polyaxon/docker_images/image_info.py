import logging

from typing import Any, Tuple

import conf

from constants.images_tags import LATEST_IMAGE_TAG

_logger = logging.getLogger('polyaxon.dockerizer.images')


def get_experiment_image_info(experiment: 'Experiment') -> Tuple[str, str]:
    """Return the image name and image tag for an experiment"""
    project_name = experiment.project.name
    repo_name = project_name

    image_name = '{}/{}'.format(conf.get('REGISTRY_HOST'), repo_name)
    image_tag = experiment.code_reference.commit
    return image_name, image_tag


def get_job_image_info(project: 'Project', job: Any) -> Tuple[str, str]:
    """Return the image name and image tag for a job"""
    project_name = project.name
    repo_name = project_name

    image_name = '{}/{}'.format(conf.get('REGISTRY_HOST'), repo_name)
    try:
        last_commit = project.repo.last_commit
    except ValueError:
        raise ValueError('Repo was not found for project `{}`.'.format(project))
    return image_name, last_commit[0]


def get_notebook_image_info(project: 'Project', job: Any) -> Tuple[str, str]:
    """Return the image name and image tag for a job"""
    image_name, _ = get_job_image_info(project, job)
    return image_name, LATEST_IMAGE_TAG


def get_project_image_name(project_name: str, project_id: int) -> str:
    return '{}/{}_{}'.format(conf.get('REGISTRY_HOST'),
                             project_name.lower(),
                             project_id)


def get_project_image_info(project_name: str, project_id: int, image_tag: str) -> Tuple[str, str]:
    return get_project_image_name(project_name=project_name, project_id=project_id), image_tag


def get_project_tagged_image(project_name: str, project_id: int, image_tag: str) -> str:
    image_name, image_tag = get_project_image_info(project_name=project_name,
                                                   project_id=project_id,
                                                   image_tag=image_tag)
    return '{}:{}'.format(image_name, image_tag)


def get_image_name(build_job: 'BuildJob') -> str:
    return get_project_image_name(project_name=build_job.project.name,
                                  project_id=build_job.project.id)


def get_image_info(build_job: 'BuildJob') -> Tuple[str, str]:
    return get_project_image_info(project_name=build_job.project.name,
                                  project_id=build_job.project.id,
                                  image_tag=build_job.uuid.hex)


def get_tagged_image(build_job: 'BuildJob') -> str:
    return get_project_tagged_image(project_name=build_job.project.name,
                                    project_id=build_job.project.id,
                                    image_tag=build_job.uuid.hex)
