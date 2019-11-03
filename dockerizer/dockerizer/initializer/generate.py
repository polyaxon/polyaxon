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

import logging

from typing import List, Optional, Tuple

from polyaxon_dockerizer import generate as dockerizer_generate

_logger = logging.getLogger('polyaxon.dockerizer')


def generate(job,
             build_path: str,
             from_image: str,
             build_steps: Optional[List[str]] = None,
             env_vars: Optional[List[Tuple[str, str]]] = None,
             nvidia_bin: str = None,
             lang_env: str = None,
             uid: int = None,
             gid: int = None) -> bool:
    """Build necessary code for a job to run"""
    rendered_dockerfile = dockerizer_generate(repo_path=build_path,
                                              from_image=from_image,
                                              build_steps=build_steps,
                                              env_vars=env_vars,
                                              nvidia_bin=nvidia_bin,
                                              lang_env=lang_env,
                                              uid=uid,
                                              gid=gid)

    if rendered_dockerfile:
        job.log_dockerfile(dockerfile=rendered_dockerfile)
    return True
