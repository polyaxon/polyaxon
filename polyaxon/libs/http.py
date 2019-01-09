import os
import requests
import tarfile

from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse

from hestia.auth import AuthenticationTypes
from hestia.fs import move_recursively

import conf

from libs.api import get_http_api_url


def absolute_uri(url):
    if not url:
        return None

    api_host = conf.get('API_HOST')
    if not api_host:
        return url

    url = urljoin(api_host.rstrip('/') + '/', url.lstrip('/'))
    return '{}://{}'.format(conf.get('PROTOCOL'), url)


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


def untar_file(build_path, filename, logger, delete_tar=False, internal=False, tar_suffix=None):
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
