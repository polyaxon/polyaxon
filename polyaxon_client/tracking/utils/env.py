# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import getpass
import os
import platform
import socket
import sys

from polyaxon_client.logger import logger

PROJECT_CLIENT_NAME = 'polyaxon-client'


def is_notebook():
    return 'ipykernel' in sys.modules


def get_filename():
    if is_notebook():
        return 'notebook'
    try:
        return os.path.basename(__file__)
    except Exception as e:
        logger.debug('Could not detect filename, %s', e)
        return 'not found'


def get_module_path():
    try:
        return os.path.dirname(os.path.realpath('__file__'))
    except Exception as e:
        logger.debug('Could not detect module path, %s', e)
        return 'not found'


def get_run_env():
    import pkg_resources

    def get_packages():
        try:
            installed_packages = [d for d in pkg_resources.working_set]  # noqa
            return sorted(["{}=={}".format(pkg.key, pkg.version) for pkg in installed_packages])
        except Exception as e:
            logger.debug('Could not detect installed packages, %s', e)
            return []

    try:
        version = pkg_resources.get_distribution(PROJECT_CLIENT_NAME).version
    except pkg_resources.DistributionNotFound:
        version = ''
    try:
        user = getpass.getuser()
    except Exception as e:
        logger.debug('Could not detect installed packages, %s', e)
        user = 'unknown'
    return {
        'pid': os.getpid(),
        'hostname': socket.gethostname(),
        'os': platform.platform(aliased=True),
        'system': platform.system(),
        'python_version_verbose': sys.version,
        'python_version': platform.python_version(),
        'user': user,
        'client_version': version,
        'sys.argv': sys.argv,
        'is_notebook': is_notebook(),
        'filename': get_filename(),
        'module_path': get_module_path(),
        'packages': get_packages(),
    }
