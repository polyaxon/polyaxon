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

DEFAULT_PORT = 2222
ENV_VAR_TEMPLATE = '{name: "{var_name}", value: "{var_value}"}'
VOLUME_CLAIM_NAME = "plx-pvc-{vol_name}"
CONFIG_MAP_NAME = "plx-config-{uuid}"
SECRET_NAME = "plx-secret-{uuid}"  # noqa, secret

CONTEXT_VOLUME_DOCKER = "docker"
CONTEXT_VOLUME_SHM = "shm"
CONTEXT_VOLUME_CONFIGS = "configs-context"
CONTEXT_VOLUME_ARTIFACTS = "artifacts-context"
CONTEXT_VOLUME_CONNECTIONS_FORMAT = "connections-context-{}"
