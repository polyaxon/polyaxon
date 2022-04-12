#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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
                "container": {
                    "image": "{{ image }}",
                    "command": ["foo"],
                    "args": ["foo"],
                },
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
        "cost": 2.2,
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
        "cost": 0.3,
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


def get_fxt_job_with_inputs_and_joins():
    return {
        "version": 1.1,
        "kind": "operation",
        "name": "foo",
        "description": "a description",
        "joins": [
            {
                "query": "metrics.metric: > {{ metric_level }}",
                "sort": "-metrics.metric",
                "limit": "{{ top }}",
                "params": {
                    "metrics": {"value": "outputs.metric"},
                },
            },
            {
                "query": "metrics.metric: < -1",
                "params": {
                    "excluded": {"value": "outputs.metric", "contextOnly": True},
                    "excluded_statuses": {
                        "value": "globals.status",
                        "contextOnly": True,
                    },
                    "excluded_uuids": {"value": "globals.uuid"},
                    "run_metrics_events": {
                        "value": "artifacts.metric1",
                        "contextOnly": True,
                    },
                    "artifact_paths": {
                        "value": "artifacts.base",
                    },
                    "run_outputs_paths": {
                        "value": "artifacts.outputs",
                    },
                    "all_outputs": {
                        "value": "outputs",
                    },
                    "all_inputs": {
                        "value": "inputs",
                    },
                    "all_artifacts": {
                        "value": "artifacts",
                    },
                    "files": {
                        "value": {
                            "files": ["subpath/file1", "different/subpath/file2"],
                        },
                        "toInit": True,
                    },
                    "files2": {
                        "value": {
                            "files": ["subpath/file21", "different/subpath/file22"],
                        },
                        "contextOnly": True,
                    },
                },
            },
        ],
        "params": {
            "top": {"value": 3, "contextOnly": True},
            "metric_level": {"value": 0, "contextOnly": True},
            "init_param": {
                "value": {"url": "https://git.url"},
                "connection": "git2",
                "toInit": True,
            },
        },
        "component": {
            "name": "build-template",
            "inputs": [
                {"name": "metrics", "type": "float", "isList": True},
                {"name": "excluded_uuids", "type": "uuid", "isList": True},
                {"name": "init_param", "type": "git"},
                {"name": "files", "type": "artifacts"},
                {"name": "artifact_paths", "type": "path", "isList": True},
                {"name": "run_outputs_paths", "type": "path", "isList": True},
                {"name": "all_outputs", "type": "dict", "isList": True},
                {"name": "all_inputs", "type": "dict", "isList": True},
                {"name": "all_artifacts", "type": "dict", "isList": True},
            ],
            "tags": ["tag1", "tag2"],
            "run": {
                "kind": V1RunKind.JOB,
                "container": {"image": "test"},
                "init": [
                    {"connection": "foo", "git": {"revision": "dev"}},
                    {"artifacts": {"dirs": "{{run_outputs}}"}},
                ],
            },
        },
    }


def get_fxt_tf_job():
    return {
        "version": 1.1,
        "kind": "operation",
        "name": "foo",
        "description": "a description",
        "component": {
            "name": "tf-distributed-gpu",
            "tags": ["tag1", "tag2"],
            "run": {
                "kind": "tfjob",
                "chief": {
                    "environment": {
                        "nodeSelector": {"polyaxon": "experiments-gpu-t4"},
                        "tolerations": [
                            {
                                "key": "nvidia.com/gpu",
                                "operator": "Equal",
                                "value": "present",
                                "effect": "NoSchedule",
                            }
                        ],
                    },
                    "container": {
                        "resources": {
                            "requests": {"cpu": 4, "memory": "4Gi"},
                            "limits": {"nvidia.com/gpu": 1, "cpu": 4, "memory": "8Gi"},
                        },
                        "image": "foo/bar:gpu",
                        "workingDir": "{{ globals.run_artifacts_path }}/uploads/src",
                        "command": ["python", "-u", "mnist.py"],
                    },
                },
                "worker": {
                    "replicas": 2,
                    "environment": {
                        "restartPolicy": "OnFailure",
                        "nodeSelector": {"polyaxon": "experiments-gpu-t4"},
                        "tolerations": [
                            {
                                "key": "nvidia.com/gpu",
                                "operator": "Equal",
                                "value": "present",
                                "effect": "NoSchedule",
                            }
                        ],
                    },
                    "container": {
                        "resources": {
                            "requests": {"cpu": 4, "memory": "4Gi"},
                            "limits": {"nvidia.com/gpu": 1, "cpu": 4, "memory": "8Gi"},
                        },
                        "image": "foo/bar:gpu",
                        "workingDir": "{{ globals.run_artifacts_path }}/uploads/src",
                        "command": ["python", "-u", "mnist.py"],
                    },
                },
            },
        },
    }
