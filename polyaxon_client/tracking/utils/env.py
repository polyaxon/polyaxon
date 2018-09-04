# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import getpass
import os
import platform
import socket
import sys

import pkg_resources

PROJECT_CLIENT_NAME = "polyaxon-client"


def get_run_env():
    try:
        version = pkg_resources.get_distribution(PROJECT_CLIENT_NAME).version
    except pkg_resources.DistributionNotFound:
        version = ''
    return {
        'pid': os.getpid(),
        'hostname': socket.gethostname(),
        'os': platform.platform(aliased=True),
        'system': platform.system(),
        'python_version_verbose': sys.version,
        'python_version': platform.python_version(),
        'user': getpass.getuser(),
        'client_version': version,
        'sys.argv': sys.argv,
    }
