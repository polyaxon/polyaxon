#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8

CONTEXT_MOUNT_CODE = "/plx-context/code"
CONTEXT_MOUNT_BUILD = "/plx-context/build"
CONTEXT_MOUNT_CONFIGS = "/plx-context/.configs"
CONTEXT_MOUNT_AUTH = "{}/.polyaxonauth".format(CONTEXT_MOUNT_CONFIGS)
CONTEXT_MOUNT_OUTPUTS = "/plx-context/outputs"
CONTEXT_MOUNT_LOGS = "/plx-context/logs"
CONTEXT_MOUNT_ARTIFACTS = "/plx-context/artifacts/{}"
CONTEXT_MOUNT_SHM = "/dev/shm"
CONTEXT_MOUNT_DOCKER = "/var/run/docker.sock"
