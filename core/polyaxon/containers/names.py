#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

MAIN_JOB_CONTAINER = "polyaxon-main"
INIT_AUTH_CONTAINER = "polyaxon-init-auth"
SIDECAR_CONTAINER = "polyaxon-sidecar"
TFJOBS_CONTAINER = "tensorflow"
PYTORCHJOBS_CONTAINER = "pytorch"
INIT_DOCKERFILE_CONTAINER_PREFIX = "polyaxon-init-dockerfile"
INIT_FILE_CONTAINER_PREFIX = "polyaxon-init-file"
INIT_GIT_CONTAINER_PREFIX = "polyaxon-init-git"
INIT_CUSTOM_CONTAINER_PREFIX = "polyaxon-init-custom"
INIT_ARTIFACTS_CONTAINER_PREFIX = "polyaxon-init-artifacts"
POLYAXON_INIT_PREFIX = "polyaxon-init"
INIT_PREFIX = "init"
SIDECAR_PREFIX = "sidecar"


def generate_container_name(
    prefix: str, suffix: str = None, unique: bool = True
) -> str:
    import uuid

    prefix = prefix or "container"
    unique_value = uuid.uuid4().hex[:10]
    if suffix:
        suffix = suffix.replace("_", "-")
        if unique:
            suffix = "{}-{}".format(suffix, unique_value)
    else:
        suffix = unique_value
    return "{}-{}".format(prefix, suffix)
