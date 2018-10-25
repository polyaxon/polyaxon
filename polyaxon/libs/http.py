import os
import shutil
import tarfile
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse

import requests
from django.conf import settings
from rest_framework.authentication import TokenAuthentication

from libs.api import get_http_api_url
from libs.authentication.internal import InternalAuthentication


def absolute_uri(url):
    if not url or not settings.API_HOST:
        return None

    return urljoin(settings.API_HOST.rstrip('/') + '/', url.lstrip('/'))


def add_notification_referrer_param(url, provider, is_absolute=True):
    if not is_absolute:
        url = absolute_uri(url)
    if not url:
        return None
    parsed_url = urlparse(url)
    query = parse_qs(parsed_url.query)
    query['referrer'] = provider
    url_list = list(parsed_url)
    url_list[4] = urlencode(query, doseq=True)
    return urlunparse(url_list)


def safe_request(
    url,
    method=None,
    params=None,
    data=None,
    json=None,
    headers=None,
    allow_redirects=False,
    timeout=30,
    verify_ssl=True,
):
    """A slightly safer version of `request`."""

    session = requests.Session()

    kwargs = {}

    if json:
        kwargs['json'] = json
        if not headers:
            headers = {}
        headers.setdefault('Content-Type', 'application/json')

    if data:
        kwargs['data'] = data

    if params:
        kwargs['params'] = params

    if headers:
        kwargs['headers'] = headers

    if method is None:
        method = 'POST' if (data or json) else 'GET'

    response = session.request(
        method=method,
        url=url,
        allow_redirects=allow_redirects,
        timeout=timeout,
        verify=verify_ssl,
        **kwargs
    )

    return response


def download(url,
             filename,
             logger,
             authentication_type=None,
             access_token=None,
             headers=None,
             internal=True,
             timeout=60):
    """Get download url from the internal api."""
    if internal:
        authentication_type = authentication_type or InternalAuthentication.keyword
    else:
        authentication_type = settings.SECRET_INTERNAL_TOKEN

    if authentication_type == InternalAuthentication.keyword and not access_token:
        access_token = settings.SECRET_INTERNAL_TOKEN
    elif authentication_type == TokenAuthentication.keyword and not access_token:
        raise ValueError('Access token is required')

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
        logger.info("Downloading file from %s using %s" % (url, authentication_type))
        response = requests.get(url,
                                headers=request_headers,
                                timeout=timeout,
                                stream=True)

        if response.status_code != 200:
            logger.error("Failed to download file from %s: %s" % (url, response.status_code),
                         extra={'stack': True})
            return None

        with open(filename, 'wb') as f:
            logger.info("Processing file %s" % filename)
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return filename

    except requests.exceptions.RequestException:
        logger.error("Download exception", exc_info=True)
        return None


def move_recursively(src, dst):
    files = os.listdir(src)

    for f in files:
        shutil.move(os.path.join(src, f), dst)


def untar_file(build_path, filename, logger, delete_tar=False, internal=False, tar_suffix=None):
    extract_path = build_path if internal else '/tmp'
    if filename and os.path.exists(filename):
        logger.info("Untarring the contents of the file ...")
        tar = tarfile.open(filename)
        tar.extractall(extract_path)
        tar.close()
        if delete_tar:
            logger.info("Cleaning up the tar file ...")
            os.remove(filename)

        if internal:
            tarf = [f for f in os.listdir(extract_path) if tar_suffix in f]
            if tarf:
                move_recursively(tarf[0], build_path)
        return filename
    else:
        logger.info("File was not found, build_path: %s" % os.listdir(build_path))
        return None
