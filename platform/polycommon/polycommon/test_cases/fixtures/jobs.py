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

from polyaxon.polyflow import V1RunKind


def get_fxt_job():
    return {
        "version": 1.1,
        "kind": "operation",
        "name": "foo",
        "description": "a description",
        "tags": ["tag1", "tag2"],
        "trigger": "all_succeeded",
        "component": {
            "name": "build-template",
            "tags": ["tag1", "tag2"],
            "run": {
                "kind": V1RunKind.JOB,
                "container": {"image": "test"},
                "init": [{"connection": "foo", "git": {"revision": "dev"}}],
            },
        },
    }


def get_fxt_job_with_inputs():
    return {
        "version": 1.1,
        "kind": "operation",
        "name": "foo",
        "description": "a description",
        "params": {"image": {"value": "foo/bar"}},
        "component": {
            "name": "build-template",
            "inputs": [{"name": "image", "type": "str"}],
            "tags": ["tag1", "tag2"],
            "run": {
                "kind": V1RunKind.JOB,
                "container": {"image": "{{ image }}"},
                "init": [{"connection": "foo", "git": {"revision": "dev"}}],
            },
        },
    }


def get_fxt_job_with_inputs_outputs():
    return {
        "version": 1.1,
        "kind": "operation",
        "name": "foo",
        "description": "a description",
        "params": {"image": {"value": "foo/bar"}},
        "component": {
            "name": "build-template",
            "inputs": [{"name": "image", "type": "str"}],
            "outputs": [
                {"name": "result1", "type": "str"},
                {
                    "name": "result2",
                    "type": "str",
                    "isOptional": True,
                    "value": "{{ image }}",
                },
            ],
            "tags": ["tag1", "tag2"],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "{{ image }}"}},
        },
    }


def get_fxt_job_with_inputs_and_conditions():
    return {
        "version": 1.1,
        "kind": "operation",
        "name": "foo",
        "description": "a description",
        "params": {
            "image": {"value": "foo/bar"},
            "context_param": {"value": "some-value", "contextOnly": True},
            "init_param": {
                "value": {"url": "https://git.url"},
                "connection": "git2",
                "toInit": True,
            },
        },
        "conditions": "{{ image == 'foo/bar' and context_param == 'some-value' }}",
        "component": {
            "name": "build-template",
            "inputs": [
                {"name": "image", "type": "str"},
                {"name": "init_param", "type": "git"},
            ],
            "tags": ["tag1", "tag2"],
            "run": {
                "kind": V1RunKind.JOB,
                "container": {"image": "{{ image }}"},
                "init": [{"connection": "foo", "git": {"revision": "dev"}}],
            },
        },
    }
