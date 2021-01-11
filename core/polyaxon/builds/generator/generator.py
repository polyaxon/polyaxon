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

import jinja2
import os

from polyaxon.builds.generator.dockerfile import POLYAXON_DOCKER_TEMPLATE
from polyaxon.utils.list_utils import to_list


class DockerFileGenerator:
    def __init__(self, build_context, destination="."):
        self.build_context = build_context
        self.dockerfile_path = os.path.join(destination, build_context.filename)

    def clean(self):
        # Clean dockerfile
        if not os.path.exists(self.dockerfile_path):
            return
        os.remove(self.dockerfile_path)

    def create(self, save=True):
        # Create DockerFile
        rendered_dockerfile = self.render()
        if save:
            with open(self.dockerfile_path, "w") as dockerfile:
                dockerfile.write(rendered_dockerfile)
        return rendered_dockerfile

    def render(self):
        docker_template = jinja2.Template(POLYAXON_DOCKER_TEMPLATE)
        return docker_template.render(
            image=self.build_context.image,
            copy=to_list(self.build_context.copy, check_none=True),
            run=to_list(self.build_context.run, check_none=True),
            env=to_list(self.build_context.env, check_none=True, check_dict=True),
            workdir=self.build_context.workdir,
            path=to_list(self.build_context.path, check_none=True),
            workdir_path=self.build_context.workdir_path,
            lang_env=self.build_context.lang_env,
            uid=self.build_context.uid,
            gid=self.build_context.gid,
            shell=self.build_context.shell,
        )
