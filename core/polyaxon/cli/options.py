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

OPTIONS_OWNER = {
    "args": ["--owner", "-o"],
    "kwargs": dict(
        type=str,
        help="Name of the owner/namespace, "
        "if not provided it will default to the namespace of the current user.",
    ),
}

OPTIONS_PROJECT = {
    "args": ["--project", "-p"],
    "kwargs": dict(type=str, help="The project name, e.g. 'mnist' or 'adam/mnist'."),
}

OPTIONS_RUN_UID = {
    "args": ["--uid", "-uid"],
    "kwargs": dict(type=str, help="The run uuid."),
}
