import logging
import os
from typing import Dict, Optional

import requests
import tarfile


from hestia.internal_services import InternalServices
from hestia.auth import AuthenticationTypes
from hestia.fs import move_recursively

import conf

from constants.jobs import JobLifeCycle
from dockerizer.utils import send_status
from libs.api import get_http_api_url

_logger = logging.getLogger('polyaxon.dockerizer')


def download(url: str,
             filename: str,
             logger,
             authentication_type: str = None,
             access_token: str = None,
             headers: Dict = None,
             internal: bool = True,
             timeout: int = 60) -> Optional[str]:
    """Get download url from the internal api."""
    if internal:
        authentication_type = authentication_type or AuthenticationTypes.INTERNAL_TOKEN
    else:
        authentication_type = AuthenticationTypes.TOKEN

    if authentication_type == AuthenticationTypes.INTERNAL_TOKEN and not access_token:
        access_token = conf.get('SECRET_INTERNAL_TOKEN')

    # Auth headers if access_token is present
    request_headers = {}
    if access_token:
        request_headers["Authorization"] = "{} {}".format(authentication_type, access_token)
    # Add any additional headers
    if headers:
        request_headers.update(headers)

    try:
        if internal:
            api_url = get_http_api_url()
            url = '{}/{}'.format(api_url, url)
        print("Downloading file from %s using %s" % (url, authentication_type))
        response = requests.get(url,
                                headers=request_headers,
                                timeout=timeout,
                                stream=True)

        if response.status_code != 200:
            logger.error("Failed to download file from %s: %s" % (url, response.status_code),
                         extra={'stack': True})
            return None

        with open(filename, 'wb') as f:
            logger.debug("Processing file %s" % filename)
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return filename

    except requests.exceptions.RequestException:
        logger.error("Download exception", exc_info=True)
        return None


def untar_file(build_path: str,
               filename: str,
               logger,
               delete_tar: bool = False,
               internal: bool = False,
               tar_suffix: str = None) -> Optional[str]:
    extract_path = build_path if internal else '/tmp'
    if filename and os.path.exists(filename):
        logger.debug("Untarring the contents of the file ...")
        tar = tarfile.open(filename)
        tar.extractall(extract_path)
        tar.close()
        if delete_tar:
            logger.debug("Cleaning up the tar file ...")
            os.remove(filename)

        if not internal:
            tarf = [f for f in os.listdir(extract_path) if tar_suffix in f]
            if tarf:
                src = os.path.join(extract_path, tarf[0])
                move_recursively(src, build_path)
        return filename
    else:
        print("File was not found, build_path: %s" % os.listdir(build_path))
        return None


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
