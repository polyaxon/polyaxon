import traceback

from typing import Tuple

from . import settings
from .download import download
from .extract import extract_code, extract_dockerfile
from .generate import generate


def init(job: 'Job',  # pylint:disable=too-many-branches
         build_context: str,
         from_image: str,
         commit: str,
         context_path: str,
         dockerfile_path: str) -> Tuple[bool, str]:
    build_path = '{}/{}'.format(build_context, 'build')
    if context_path:
        # We only need a subpath from the extracted code
        extract_path = '{}/{}'.format(build_context, 'code')
    else:
        # We need the whole repo, no need to differentiate between extract and build path
        extract_path = build_path
    download_file = '{}/{}'.format(build_context, '_code')
    # Download repo
    status = download(
        job=job,
        extract_path=extract_path,
        download_file=download_file,
        commit=commit)
    if not status:
        return status, 'An error occurred while downloading the code.'

    if context_path:
        status = extract_code(extract_path=extract_path,
                              build_path=build_path,
                              context_path=context_path)
    if not status:
        return status, 'An error occurred while extracting the code.'
    if dockerfile_path:
        # Move dockerfile to the build context
        status = extract_dockerfile(job=job,
                                    extract_path=extract_path,
                                    dockerfile_path=dockerfile_path,
                                    build_context=build_context)
        if not status:
            return status, 'An error occurred while extracting the dockerfile from the context.'
        return True, ''
    else:
        # Generate dockerfile
        try:
            return generate(job=job,
                            build_path=build_path,
                            from_image=from_image,
                            build_steps=settings.CONTAINER_BUILD_STEPS,
                            env_vars=settings.CONTAINER_ENV_VARS,
                            nvidia_bin=settings.MOUNT_PATHS_NVIDIA), ''
        except Exception:
            return False, 'An error occurred while generating the dockerfile.'


def cmd(job: 'Job',
        build_context: str,
        from_image: str,
        commit: str,
        context_path: str,
        dockerfile_path: str):
    # Initializing the docker context
    try:
        status, message = init(job=job,
                               build_context=build_context,
                               from_image=from_image,
                               commit=commit,
                               context_path=context_path,
                               dockerfile_path=dockerfile_path)
        if not status:
            job.failed(message='Failed to initialize build job ({}).'.format(message))
            return
    except Exception as e:  # Other exceptions
        job.failed(
            message='Failed to build job encountered an {} exception'.format(e.__class__.__name__),
            traceback=traceback.format_exc())
        return
