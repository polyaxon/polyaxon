import logging

from .utils import ensure_path

_logger = logging.getLogger('polyaxon.dockerizer')


def download(job: 'Job', extract_path: str, download_file: str, commit: str):
    ensure_path(extract_path)

    repo_file = job.client.project.download_repo(
        username=job.username,
        project_name=job.project_name,
        commit=commit,
        filename=download_file,
        untar=True,
        delete_tar=True,
        extract_path=extract_path
    )
    if not repo_file:
        job.failed(message='Could not download code to build the image.')
        return False

    return True
