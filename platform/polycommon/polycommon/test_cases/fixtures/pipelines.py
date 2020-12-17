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


def get_fxt_templated_pipeline_without_params():
    return {
        "version": 1.1,
        "kind": "operation",
        "component": {
            "name": "test-build-run",
            "description": "testing a build and run pipeline",
            "tags": ["backend", "native"],
            "run": {
                "kind": V1RunKind.DAG,
                "operations": [
                    {
                        "dagRef": "build-template",
                        "name": "build",
                        "params": {
                            "env_vars": {
                                "value": [["env1", "value1"], ["env2", "value2"]]
                            }
                        },
                    },
                    {
                        "dagRef": "experiment-template",
                        "name": "run",
                        "dependencies": ["build"],
                        "params": {
                            "image": {
                                "ref": "ops.build",
                                "value": "outputs.docker-image",
                            },
                            "lr": {"value": 0.001},
                            "dag_uuid": {
                                "value": "uuid",
                                "ref": "dag",
                                "contextOnly": True,
                            },
                            "op_uuid": {
                                "value": "uuid",
                                "ref": "ops.build",
                                "contextOnly": True,
                            },
                        },
                    },
                ],
                "components": [
                    {
                        "name": "experiment-template",
                        "description": "experiment to predict something",
                        "tags": ["key", "value"],
                        "inputs": [
                            {
                                "name": "lr",
                                "type": "float",
                                "value": 0.1,
                                "isOptional": True,
                            },
                            {"name": "image", "type": "str"},
                        ],
                        "termination": {"maxRetries": 2},
                        "run": {
                            "kind": V1RunKind.JOB,
                            "environment": {
                                "nodeSelector": {"polyaxon": "experiments"},
                                "serviceAccountName": "service",
                                "imagePullSecrets": ["secret1", "secret2"],
                            },
                            "container": {
                                "image": "{{ image }}",
                                "command": ["python3", "main.py"],
                                "args": "--lr={{ lr }}",
                                "resources": {"requests": {"cpu": 1}},
                            },
                        },
                    },
                    {
                        "name": "build-template",
                        "description": "build images",
                        "tags": ["backend", "kaniko"],
                        "inputs": [
                            {"name": "env_vars", "type": "list", "isList": "true"}
                        ],
                        "outputs": [{"name": "docker-image", "type": "str"}],
                        "termination": {"maxRetries": 2},
                        "run": {
                            "kind": V1RunKind.JOB,
                            "environment": {
                                "nodeSelector": {"polyaxon": "experiments"},
                                "serviceAccountName": "service",
                                "imagePullSecrets": ["secret1", "secret2"],
                            },
                            "container": {
                                "image": "base",
                                "resources": {"requests": {"cpu": 1}},
                            },
                            "init": [
                                {
                                    "dockerfile": {
                                        "image": "base",
                                        "env": "{{ env_vars }}",
                                    }
                                }
                            ],
                        },
                    },
                ],
            },
        },
    }


def get_fxt_templated_pipeline_with_upstream_run(run_uuid: UUID):
    return {
        "version": 1.1,
        "kind": "operation",
        "component": {
            "name": "test-build-run",
            "description": "testing a build and run pipeline",
            "tags": ["backend", "native"],
            "inputs": [
                {
                    "name": "top",
                    "type": "int",
                    "value": 5,
                    "isOptional": True,
                    "description": "top jobs.",
                }
            ],
            "run": {
                "kind": V1RunKind.DAG,
                "operations": [
                    {
                        "dagRef": "build-template",
                        "name": "build",
                        "params": {
                            "env_vars": {
                                "value": [["env1", "value1"], ["env2", "value2"]]
                            }
                        },
                    },
                    {
                        "dagRef": "experiment-template",
                        "name": "run",
                        "dependencies": ["build"],
                        "runPatch": {
                            "environment": {
                                "nodeSelector": {
                                    "{{ dag_uuid }}": "node-{{ context_param }}",
                                }
                            }
                        },
                        "params": {
                            "image": {
                                "ref": "ops.build",
                                "value": "outputs.docker-image",
                            },
                            "lr": {"value": 0.001},
                            "some-run": {
                                "value": "outputs.some-int",
                                "ref": "runs.{}".format(run_uuid.hex),
                            },
                            "context_param": {
                                "value": "inputs.top",
                                "ref": "dag",
                                "contextOnly": True,
                            },
                            "dag_uuid": {
                                "value": "uuid",
                                "ref": "dag",
                                "contextOnly": True,
                            },
                            "op_uuid": {
                                "value": "uuid",
                                "ref": "ops.build",
                                "contextOnly": True,
                            },
                        },
                    },
                ],
                "components": [
                    {
                        "name": "experiment-template",
                        "description": "experiment to predict something",
                        "tags": ["key", "value"],
                        "inputs": [
                            {
                                "name": "lr",
                                "type": "float",
                                "value": 0.1,
                                "isOptional": True,
                            },
                            {"name": "image", "type": "str"},
                            {"name": "some-run", "type": "int"},
                        ],
                        "termination": {"maxRetries": 2},
                        "run": {
                            "kind": V1RunKind.JOB,
                            "environment": {
                                "nodeSelector": {"polyaxon": "experiments"},
                                "serviceAccountName": "service",
                                "imagePullSecrets": ["secret1", "secret2"],
                            },
                            "container": {
                                "image": "{{ image }}",
                                "command": ["python3", "main.py"],
                                "args": "--lr={{ lr }}",
                                "resources": {"requests": {"cpu": 1}},
                            },
                        },
                    },
                    {
                        "name": "build-template",
                        "description": "build images",
                        "tags": ["backend", "kaniko"],
                        "inputs": [
                            {"name": "env_vars", "type": "list", "isList": "true"}
                        ],
                        "outputs": [{"name": "docker-image", "type": "str"}],
                        "termination": {"maxRetries": 2},
                        "run": {
                            "kind": V1RunKind.JOB,
                            "environment": {
                                "nodeSelector": {"polyaxon": "experiments"},
                                "serviceAccountName": "service",
                                "imagePullSecrets": ["secret1", "secret2"],
                            },
                            "container": {
                                "image": "base",
                                "resources": {"requests": {"cpu": 1}},
                            },
                            "init": [
                                {
                                    "dockerfile": {
                                        "image": "base",
                                        "env": "{{ env_vars }}",
                                    }
                                }
                            ],
                        },
                    },
                ],
            },
        },
    }


def get_fxt_build_run_pipeline():
    return {
        "version": 1.1,
        "kind": "operation",
        "dependencies": ["foo", "bar"],
        "trigger": "all_succeeded",
        "component": {
            "name": "build_run_pipeline",
            "tags": ["foo", "bar"],
            "description": "testing a build and run pipeline",
            "run": {
                "kind": V1RunKind.DAG,
                "operations": [
                    {"dagRef": "build-template", "name": "A"},
                    {"dagRef": "job-template", "name": "B", "dependencies": ["A"]},
                ],
                "components": [
                    {
                        "name": "job-template",
                        "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                    },
                    {
                        "name": "build-template",
                        "tags": ["backend", "kaniko"],
                        "run": {
                            "kind": V1RunKind.JOB,
                            "container": {"image": "test"},
                            "init": [{"connection": "foo", "git": {"revision": "dev"}}],
                        },
                    },
                ],
            },
        },
    }


def get_fxt_build_run_pipeline_with_inputs():
    return {
        "version": 1.1,
        "kind": "operation",
        "dependencies": ["foo", "bar"],
        "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
        "trigger": "all_succeeded",
        "component": {
            "name": "my-pipe-test",
            "description": "testing a pipe",
            "tags": ["key", "value"],
            "inputs": [
                {"name": "param1", "type": "str"},
                {"name": "param2", "type": "str"},
            ],
            "run": {
                "kind": V1RunKind.DAG,
                "operations": [
                    {"dagRef": "build-template", "name": "A"},
                    {"dagRef": "job-template", "name": "B", "dependencies": ["A"]},
                ],
                "components": [
                    {
                        "name": "job-template",
                        "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                    },
                    {
                        "name": "build-template",
                        "tags": ["backend", "kaniko"],
                        "run": {
                            "kind": V1RunKind.JOB,
                            "container": {"image": "test"},
                            "init": [{"connection": "foo", "git": {"revision": "dev"}}],
                        },
                    },
                ],
            },
        },
    }


def get_fxt_pipeline_params_env_termination():
    return {
        "version": 1.1,
        "name": "params_env_termination",
        "kind": "operation",
        "dependencies": ["foo", "bar"],
        "trigger": "all_succeeded",
        "params": {"pipe_param1": {"value": "foo"}, "pipe_param2": {"value": "bar"}},
        "termination": {"maxRetries": 2},
        "runPatch": {
            "kind": V1RunKind.DAG,
            "environment": {
                "nodeSelector": {"polyaxon": "experiments"},
                "serviceAccountName": "service",
                "imagePullSecrets": ["secret1", "secret2"],
            },
        },
        "component": {
            "inputs": [
                {"name": "pipe_param1", "type": "str"},
                {"name": "pipe_param2", "type": "str"},
            ],
            "run": {
                "kind": V1RunKind.DAG,
                "operations": [
                    {
                        "dagRef": "build-template",
                        "name": "A",
                        "params": {
                            "param2": {"ref": "dag", "value": "inputs.pipe_param2"}
                        },
                    },
                    {
                        "dagRef": "job-template",
                        "name": "B",
                        "dependencies": ["A"],
                        "params": {
                            "param1": {"ref": "dag", "value": "inputs.pipe_param1"}
                        },
                        "termination": {"maxRetries": 3},
                        "runPatch": {"kind": V1RunKind.JOB},
                    },
                ],
                "components": [
                    {
                        "name": "job-template",
                        "inputs": [{"name": "param1", "type": "str"}],
                        "termination": {"maxRetries": 1},
                        "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                    },
                    {
                        "name": "build-template",
                        "tags": ["backend", "kaniko"],
                        "inputs": [{"name": "param2", "type": "str"}],
                        "termination": {"maxRetries": 1},
                        "run": {
                            "kind": V1RunKind.JOB,
                            "container": {"image": "test"},
                            "init": [{"connection": "foo", "git": {"revision": "dev"}}],
                        },
                    },
                ],
            },
        },
    }
