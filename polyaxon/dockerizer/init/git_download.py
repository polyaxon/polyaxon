import logging
import os

from hestia.internal_services import InternalServices

import conf

from constants.jobs import JobLifeCycle
from dockerizer.utils import send_status
from libs.http import download, untar_file

_logger = logging.getLogger('polyaxon.dockerizer')


def download_code(build_job: 'BuildJob', build_path: str, filename: str):
    if not os.path.exists(build_path):
        os.makedirs(build_path)

    filename = '{}/{}'.format(build_path, filename)

    if build_job.code_reference.repo or build_job.code_reference.external_repo:
        if build_job.code_reference.repo:
            download_url = build_job.code_reference.repo.download_url
        else:
            download_url = build_job.code_reference.external_repo.download_url
        internal = True
        headers = {
            conf.get('HEADERS_INTERNAL').replace('_', '-'): InternalServices.DOCKERIZER
        }
        access_token = None
    elif build_job.code_reference.git_url:
        download_url = build_job.code_reference.git_url
        internal = False
        access_token = conf.get('REPOS_ACCESS_TOKEN')
        # Gitlab requires header `private-token`
        headers = {}
    else:
        raise ValueError('Code reference for this build job does not have any repo.')

    if internal:
        if build_job.code_reference.commit:
            download_url = '{}?commit={}'.format(download_url, build_job.code_reference.commit)
        tar_suffix = None
    else:
        tar_suffix = (
            build_job.code_reference.commit
            if build_job.code_reference.commit
            else 'master'
        )
        archive_url = '/archive'
        if 'bitbucket' in download_url.lower():
            if access_token:
                headers = {'Authorization': 'Bearer {}'.format(access_token)}
            archive_url = '/get'
        elif 'github' not in download_url.lower():
            # We assume it's a gitlab (either saas or on-premis)
            if access_token:
                headers = {'PRIVATE-TOKEN': access_token}
            download_url += '/-'  # Gitlab requires this underscore for valid urls
        download_url += archive_url
        download_url += '/{}'.format(tar_suffix)
        download_url += '.tar.gz'

    repo_file = download(
        url=download_url,
        filename=filename,
        logger=_logger,
        headers=headers,
        access_token=access_token,
        internal=internal)
    if not repo_file:
        send_status(build_job=build_job,
                    status=JobLifeCycle.FAILED,
                    message='Could not download code to build the image.')
        return False
    status = untar_file(
        build_path=build_path,
        filename=filename,
        logger=_logger,
        delete_tar=True,
        internal=internal,
        tar_suffix=tar_suffix)
    if not status:
        send_status(build_job=build_job,
                    status=JobLifeCycle.FAILED,
                    message='Could not handle downloaded code to build the image.')
        return False

    return True
