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

import os
import shutil

from polyaxon_dockerizer.dockerfile import POLYAXON_DOCKERFILE_NAME


def extract_code(extract_path: str, build_path: str, context_path: str) -> bool:
    try:
        # We copy all files under the context to the build path
        extract_context_path = os.path.join(extract_path, context_path)
        shutil.copytree(extract_context_path, build_path)
        return True
    except Exception:
        return False


def extract_dockerfile(job: 'DockerJob',
                       extract_path: str,
                       dockerfile_path: str,
                       build_context: str) -> bool:
    try:
        # We move all files under the context to the build path
        context_dockerfile_path = os.path.join(extract_path, dockerfile_path)
        build_dockerfile_path = os.path.join(build_context, POLYAXON_DOCKERFILE_NAME)
        shutil.copy(context_dockerfile_path, build_dockerfile_path)

        # Log dockerfile
        with open(build_dockerfile_path) as rendered_dockerfile:
            job.log_dockerfile(dockerfile=rendered_dockerfile.read())
        return True
    except Exception:
        return False
