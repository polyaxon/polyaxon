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

from uuid import UUID

from polyaxon.polyflow import V1RunKind


def get_fxt_service():
    return {
        "version": 1.1,
        "kind": "operation",
        "name": "foo",
        "description": "a description",
        "tags": ["tag1", "tag2"],
        "trigger": "all_succeeded",
        "component": {
            "name": "service-template",
            "tags": ["backend", "lab"],
            "run": {
                "kind": V1RunKind.SERVICE,
                "container": {"image": "jupyter"},
                "init": [{"connection": "foo", "git": {"revision": "dev"}}],
                "ports": [5555],
            },
        },
    }


def get_fxt_service_with_inputs():
    return {
        "version": 1.1,
        "kind": "operation",
        "name": "foo",
        "description": "a description",
        "params": {"image": {"value": "foo/bar"}},
        "component": {
            "name": "service-template",
            "inputs": [{"name": "image", "type": "str"}],
            "tags": ["backend", "lab"],
            "run": {
                "kind": V1RunKind.SERVICE,
                "container": {"image": "{{ image }}"},
                "init": [{"connection": "foo", "git": {"revision": "dev"}}],
                "ports": [5555],
            },
        },
    }
