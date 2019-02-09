import traceback

from . import settings
from .constants import BUILD_PATH
from .initializer.generate import generate
from .initializer.download import download


def init(job: 'Job', build_path: str = BUILD_PATH) -> bool:
    # Check image if exists
    # Download repo
    filename = '_code'
    status = download(
        job=job,
        build_path=build_path,
        filename=filename)
    if not status:
        return status
    # Generate dockerfile
    return generate(build_path=build_path,
                    image_tag=settings.CONTAINER_IMAGE_TAG,
                    from_image=settings.CONTAINER_FROM_IMAGE,
                    image_name=settings.CONTAINER_IMAGE_NAME,
                    build_steps=settings.CONTAINER_BUILD_STEPS,
                    env_vars=settings.CONTAINER_ENV_VARS,
                    nvidia_bin=settings.MOUNT_PATHS_NVIDIA)


def cmd(job: 'Job'):
    # Initializing the docker context
    try:
        status = init(job=job)
        if not status:
            job.failed(message='Failed to initialize build job job.')
            return
    except Exception as e:  # Other exceptions
        job.failed(
            message='Failed to build job encountered an {} exception'.format(e.__class__.__name__),
            traceback=traceback.format_exc())
        return
