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

import argparse
import json

from initializer.init import cmd  # noqa
from polyaxon_client.tracking import BuildJob

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--build_context',
        type=str
    )
    parser.add_argument(
        '--from_image',
        type=str
    )
    parser.add_argument(
        '--commit',
        type=str,
        default=None,
    )
    parser.add_argument(
        '--context_path',
        type=str,
        default=None,
    )
    parser.add_argument(
        '--dockerfile_path',
        type=str,
        default=None,
    )
    parser.add_argument(
        '--lang_env',
        type=str,
        default=None,
    )
    parser.add_argument(
        '--uid',
        type=int,
        default=None,
    )
    parser.add_argument(
        '--gid',
        type=int,
        default=None,
    )
    parser.add_argument(
        '--env_vars',
        type=str,
        default=None,
    )
    parser.add_argument(
        '--build_steps',
        type=str,
        default=None,
    )
    parser.add_argument(
        '--mount_paths_nvidia',
        type=str,
        default=None,
    )
    args = parser.parse_args()
    arguments = args.__dict__

    build_context = arguments.pop('build_context')
    from_image = arguments.pop('from_image')
    commit = arguments.pop('commit')
    context_path = arguments.pop('context_path')
    dockerfile_path = arguments.pop('dockerfile_path')
    lang_env = arguments.pop('lang_env')
    uid = arguments.pop('uid')
    gid = arguments.pop('gid')
    env_vars = arguments.pop('env_vars')
    if env_vars:
        env_vars = json.loads(env_vars)
    build_steps = arguments.pop('build_steps')
    if build_steps:
        build_steps = json.loads(build_steps)
    mount_paths_nvidia = arguments.pop('mount_paths_nvidia')

    job = BuildJob()
    cmd(job=job,
        build_context=build_context,
        from_image=from_image,
        commit=commit,
        context_path=context_path,
        dockerfile_path=dockerfile_path,
        lang_env=lang_env,
        uid=uid,
        gid=gid,
        env_vars=env_vars,
        build_steps=build_steps,
        nvidia_bin=mount_paths_nvidia)
