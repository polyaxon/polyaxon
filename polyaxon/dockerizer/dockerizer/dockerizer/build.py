import traceback

from docker.errors import DockerException

from .builders import native


def cmd(job: 'Job', build_context: str, image_name: str, image_tag: str, nocache: bool):
    # Building the docker image
    error = {}
    try:
        status = native.build(job=job,
                              build_context=build_context,
                              image_name=image_name,
                              image_tag=image_tag,
                              nocache=nocache)
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
