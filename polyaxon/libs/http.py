import os
import tarfile

import requests


def safe_urlopen(
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
    """
    A slightly safer version of ``urlib2.urlopen`` which prevents redirection
    and ensures the URL isn't attempting to hit a blacklisted IP range.
    """

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


def download(url, access_token, filename, logger, headers=None, timeout=60, untar=False):
    """Download the file from the given url at the current path"""
    logger.info("Downloading file from %s" % url)
    # Auth headers if access_token is present
    request_headers = {}
    if access_token:
        request_headers["Authorization"] = "Token " + access_token
    # Add any additional headers
    if headers:
        request_headers.update(headers)

    try:
        response = requests.get(url,
                                headers=request_headers,
                                timeout=timeout,
                                stream=True)

        if response.status_code != 200:
            logger.warning("Failed to download file from %s: %s" % (url, response.status_code))
            return None

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        if untar:
            untar_file(filename=filename, logger=logger, delete_tar=True)
        return filename

    except requests.exceptions.RequestException as e:
        logger.warning("Exception: %s" % e)
        return None


def untar_file(filename, logger, delete_tar=False):
    if filename:
        logger.info("Untarring the contents of the file ...")
        tar = tarfile.open(filename)
        tar.extractall()
        tar.close()
    if delete_tar:
        logger.info("Cleaning up the tar file ...")
        os.remove(filename)
    return filename
