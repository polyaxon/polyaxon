import logging

from typing import Tuple, Optional

_logger = logging.getLogger('polyaxon.dockerizer.images')


def get_image_name(build_job: 'BuildJob', registry_host: Optional[str]) -> str:
    if registry_host:
        return '{}/{}_{}'.format(registry_host,
                                 build_job.project.name.lower(),
                                 build_job.project.id)
    return '{}_{}'.format(build_job.project.name.lower(), build_job.project.id)


def get_image_info(build_job: 'BuildJob', registry_host: str) -> Tuple[str, str]:
    return get_image_name(build_job=build_job, registry_host=registry_host), build_job.uuid.hex
