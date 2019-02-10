import logging
import os

_logger = logging.getLogger('polyaxon.dockerizer')


def download(job: 'Job', build_path: str, filename: str, commit: str):
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    filename = '{}/{}'.format(build_path, filename)

    repo_file = job.client.project.download_repo(
        username=job.username,
        project_name=job.project_name,
        commit=commit,
        filename=filename,
        untar=True,
        delete_tar=True,
        extract_path=build_path
    )
    if not repo_file:
        job.failed(message='Could not download code to build the image.')
        return False

    return True
