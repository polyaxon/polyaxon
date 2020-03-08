#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import getpass
import os
import platform
import socket
import sys

from polyaxon.logger import logger

PROJECT_CLIENT_NAME = "polyaxon-client"


def is_notebook():
    return "ipykernel" in sys.modules


def get_filename():
    if is_notebook():
        return "notebook"
    try:
        return os.path.basename(__file__)
    except Exception as e:
        logger.debug("Could not detect filename, %s", e)
        return "not found"


def get_module_path():
    try:
        return os.path.dirname(os.path.realpath("__file__"))
    except Exception as e:
        logger.debug("Could not detect module path, %s", e)
        return "not found"


def get_run_env():
    import pkg_resources

    def get_packages():
        try:
            installed_packages = [d for d in pkg_resources.working_set]  # noqa
            return sorted(
                ["{}=={}".format(pkg.key, pkg.version) for pkg in installed_packages]
            )
        except Exception as e:
            logger.debug("Could not detect installed packages, %s", e)
            return []

    try:
        version = pkg_resources.get_distribution(PROJECT_CLIENT_NAME).version
    except pkg_resources.DistributionNotFound:
        version = ""
    try:
        user = getpass.getuser()
    except Exception as e:
        logger.debug("Could not detect installed packages, %s", e)
        user = "unknown"
    return {
        "pid": os.getpid(),
        "hostname": socket.gethostname(),
        "os": platform.platform(aliased=True),
        "system": platform.system(),
        "python_version_verbose": sys.version,
        "python_version": platform.python_version(),
        "user": user,
        "client_version": version,
        "sys.argv": sys.argv,
        "is_notebook": is_notebook(),
        "filename": get_filename(),
        "module_path": get_module_path(),
        "packages": get_packages(),
    }
