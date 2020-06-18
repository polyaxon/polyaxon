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

import os

from polyaxon.env_vars.keys import POLYAXON_KEYS_CONTEXT_ROOT


def polyaxon_user_path():
    base_path = os.path.expanduser("~")
    if not os.access(base_path, os.W_OK):
        base_path = "/tmp"

    return os.path.join(base_path, ".polyaxon")


CONTEXT_ROOT = os.environ.get(POLYAXON_KEYS_CONTEXT_ROOT, "/plx-context")
CONTEXT_MOUNT_GC = "{}/.gc/gc-secret.json".format(CONTEXT_ROOT)
CONTEXT_MOUNT_CONFIGS = "{}/.configs".format(CONTEXT_ROOT)
CONTEXT_MOUNT_AUTH = "{}/.auth".format(CONTEXT_MOUNT_CONFIGS)
CONTEXT_MOUNT_ARTIFACTS = "{}/artifacts".format(CONTEXT_ROOT)
CONTEXT_MOUNT_ARTIFACTS_FORMAT = "{}/artifacts/{{}}".format(CONTEXT_ROOT)
CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT = "{}/outputs".format(CONTEXT_MOUNT_ARTIFACTS_FORMAT)
CONTEXT_MOUNT_RUN_EVENTS_FORMAT = "{}/events".format(CONTEXT_MOUNT_ARTIFACTS_FORMAT)
CONTEXT_MOUNT_SHM = "/dev/shm"
CONTEXT_MOUNT_DOCKER = "/var/run/docker.sock"

CONTEXT_TMP_POLYAXON_PATH = "/tmp/.polyaxon/"
CONTEXT_USER_POLYAXON_PATH = polyaxon_user_path()
CONTEXT_ARCHIVE_ROOT = "/tmp/plx/archives"
CONTEXT_ARTIFACTS_ROOT = "/tmp/plx/artifacts"
