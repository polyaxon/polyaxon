#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from polyaxon.env_vars.keys import (
    EV_KEYS_ARCHIVE_ROOT,
    EV_KEYS_ARTIFACTS_ROOT,
    EV_KEYS_CONTEXT_ROOT,
    EV_KEYS_OFFLINE_ROOT,
    EV_KEYS_SANDBOX_ROOT,
)


def polyaxon_user_path():
    base_path = os.path.expanduser("~")
    if not os.access(base_path, os.W_OK):
        base_path = "/tmp"

    return os.path.join(base_path, ".polyaxon")


CONTEXT_RELATED_RUNS = "_related_runs"

# Local contexts
CONTEXT_LOCAL_LINEAGES = "lineages.plx.json"
CONTEXT_LOCAL_CONTENT = "content.plx.json"
CONTEXT_LOCAL_README = "readme.plx.md"
CONTEXT_LOCAL_POLYAXONFILE = "polyaxonfile.plx.md"
CONTEXT_LOCAL_PROJECT = "project.plx.json"
CONTEXT_LOCAL_RUN = "run.plx.json"
CONTEXT_LOCAL_VERSION = "version.plx.json"

CONTEXT_ROOT = os.environ.get(EV_KEYS_CONTEXT_ROOT, "/plx-context")
CONTEXT_MOUNT_GC = "{}/.gc/gc-secret.json".format(CONTEXT_ROOT)
CONTEXT_MOUNT_CONFIGS = "{}/.configs".format(CONTEXT_ROOT)
CONTEXT_MOUNT_AUTH = "{}/.auth".format(CONTEXT_MOUNT_CONFIGS)
CONTEXT_MOUNT_FILE_WATCHER = "{}/.fs".format(CONTEXT_ROOT)
CONTEXT_MOUNT_ARTIFACTS = "{}/artifacts".format(CONTEXT_ROOT)
CONTEXT_MOUNT_ARTIFACTS_FORMAT = "{}/{{}}".format(CONTEXT_MOUNT_ARTIFACTS)
CONTEXT_MOUNT_ARTIFACTS_RELATED = CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(
    CONTEXT_RELATED_RUNS
)
CONTEXT_MOUNT_ARTIFACTS_RELATED_FORMAT = "{}/{{}}".format(
    CONTEXT_MOUNT_ARTIFACTS_RELATED
)
CONTEXT_MOUNT_RUN_ASSETS_FORMAT = "{}/assets".format(CONTEXT_MOUNT_ARTIFACTS_FORMAT)
CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT = "{}/outputs".format(CONTEXT_MOUNT_ARTIFACTS_FORMAT)
CONTEXT_MOUNT_RUN_EVENTS_FORMAT = "{}/events".format(CONTEXT_MOUNT_ARTIFACTS_FORMAT)
CONTEXT_MOUNT_RUN_SYSTEM_RESOURCES_EVENTS_FORMAT = "{}/resources".format(
    CONTEXT_MOUNT_ARTIFACTS_FORMAT
)
CONTEXT_MOUNT_SHM = "/dev/shm"
CONTEXT_MOUNT_DOCKER = "/var/run/docker.sock"

CONTEXT_TMP_POLYAXON_PATH = "/tmp/.polyaxon/"
CONTEXT_USER_POLYAXON_PATH = polyaxon_user_path()
CONTEXT_ARCHIVE_ROOT = os.environ.get(EV_KEYS_ARCHIVE_ROOT, "/tmp/plx/archives")
CONTEXT_ARTIFACTS_ROOT = os.environ.get(EV_KEYS_ARTIFACTS_ROOT, "/tmp/plx/artifacts")
CONTEXT_SANDBOX_ROOT = None
CONTEXT_OFFLINE_ROOT = os.environ.get(EV_KEYS_OFFLINE_ROOT, "/tmp/plx/offline")
CONTEXT_OFFLINE_FORMAT = "{}/{{}}".format(CONTEXT_OFFLINE_ROOT)
CONTEXT_ARTIFACTS_FORMAT = "{}/{{}}".format(CONTEXT_ARTIFACTS_ROOT)

CONTEXTS_OUTPUTS_SUBPATH_FORMAT = "{}/outputs"
CONTEXTS_EVENTS_SUBPATH_FORMAT = "{}/events"
CONTEXTS_SYSTEM_RESOURCES_EVENTS_SUBPATH_FORMAT = "{}/resources"


def get_offline_base_path(entity_kind: str, path: str = None):
    from polyaxon.lifecycle import V1ProjectFeature

    path = path or CONTEXT_OFFLINE_ROOT
    entity_kind = "run" if entity_kind == V1ProjectFeature.RUNTIME else entity_kind
    return "{}/{}s".format(path, entity_kind)


def get_offline_path(entity_value: str, entity_kind: str, path: str = None):
    from polyaxon.lifecycle import V1ProjectFeature

    path = path or CONTEXT_OFFLINE_ROOT
    entity_kind = "run" if entity_kind == V1ProjectFeature.RUNTIME else entity_kind
    return "{}/{}s/{}".format(path, entity_kind, entity_value)


def mount_sandbox():
    global CONTEXT_SANDBOX_ROOT
    global CONTEXT_OFFLINE_ROOT
    global CONTEXT_ARTIFACTS_ROOT
    global CONTEXT_OFFLINE_FORMAT
    global CONTEXT_ARTIFACTS_FORMAT

    CONTEXT_SANDBOX_ROOT = os.environ.get(EV_KEYS_SANDBOX_ROOT, CONTEXT_OFFLINE_ROOT)
    CONTEXT_OFFLINE_ROOT = CONTEXT_SANDBOX_ROOT
    CONTEXT_ARTIFACTS_ROOT = CONTEXT_SANDBOX_ROOT
    CONTEXT_OFFLINE_FORMAT = "{}/{{}}".format(CONTEXT_OFFLINE_ROOT)
    CONTEXT_ARTIFACTS_FORMAT = "{}/{{}}".format(CONTEXT_ARTIFACTS_ROOT)
