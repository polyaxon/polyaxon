import traceback

from docker.errors import DockerException

from . import settings, constants
from .builders import native


def cmd(job: 'Job', build_path: str = constants.BUILD_PATH):
    # Building the docker image
    error = {}
    try:
        status = native.build(job=job,
                              build_path=build_path,
                              image_tag=settings.CONTAINER_IMAGE_TAG,
                              from_image=settings.CONTAINER_FROM_IMAGE,
                              image_name=settings.CONTAINER_IMAGE_NAME)
        if not status:
            error = {
                'raised': True,
                'message': 'Failed to build job.'
            }
    except DockerException as e:
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Failed to build job encountered an {} exception'.format(
                e.__class__.__name__)
        }
    except Exception as e:  # Other exceptions
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Failed to build job encountered an {} exception'.format(
                e.__class__.__name__)
        }

    if error.get('raised'):
        job.failed(
            message=error.get('message'),
            traceback=error.get('traceback'))
        return
