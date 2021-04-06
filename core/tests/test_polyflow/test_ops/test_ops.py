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

import pytest

from marshmallow import ValidationError

from polyaxon.polyflow import V1EventKind, V1Hook, V1Param, V1RunKind
from polyaxon.polyflow.operations import V1Operation
from tests.utils import BaseTestCase


@pytest.mark.ops_mark
class TestV1Operations(BaseTestCase):
    def test_op_raises_for_template_action_event(self):
        config_dict = {"hubRef": "foo", "urlRef": "bar"}
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

        config_dict = {"pathRef": "bar", "urlRef": "foo"}
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

        config_dict = {"hubRef": "bar", "urlRef": "foo"}
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

    def test_op_passes_for_template_hub(self):
        config_dict = {"hubRef": "bar"}
        config = V1Operation.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"pathRef": "bar"}
        config = V1Operation.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"urlRef": "bar"}
        config = V1Operation.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"dagRef": "bar"}
        config = V1Operation.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_validation(self):
        config_dict = {"hubRef": "foo", "concurrency": "foo"}
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

        config_dict = {"hubRef": "foo", "dependencies": "foo"}
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

        config_dict = {
            "hubRef": "foo",
            "dependencies": ["foo", "bar"],
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
        }
        config = V1Operation.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"hubRef": "foo"}
        config = V1Operation.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {
            "hubRef": "foo",
            "dependencies": [{"name": "foo"}, {"name": "bar"}],  # Wrong
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
        }
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

    def test_op_with_embedded_job_template(self):
        # Embedding a bad template
        config_dict = {
            "dependencies": ["foo", "bar"],
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
            "component": {
                "not_supported_key": "build-template",
                "tags": ["kaniko"],
                "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
            },
        }
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

        # Embedding a template without container
        config_dict = {
            "dependencies": ["foo", "bar"],
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
            "component": {"name": "build-template", "tags": ["kaniko"]},
        }
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

        # Embedding a correct template
        config_dict = {
            "dependencies": ["foo", "bar"],
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
            "component": {
                "name": "build-template",
                "tags": ["kaniko"],
                "run": {
                    "kind": V1RunKind.JOB,
                    "container": {"image": "test"},
                    "init": [{"connection": "foo", "container": {"image": "dev"}}],
                },
            },
        }
        config = V1Operation.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_op_with_embedded_service_template(self):
        # Embedding a bad template
        config_dict = {
            "dependencies": ["foo", "bar"],
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
            "runPatch": {
                "kind": V1RunKind.JOB,
                "init": [{"connection": "foo", "git": {"revision": "dev"}}],
            },
            "component": {
                "not_supported_key": "build-template",
                "tags": ["lab"],
                "run": {
                    "kind": V1RunKind.JOB,
                    "container": {"image": "jupyterlab"},
                    "environment": {
                        "nodeSelector": {"polyaxon.com": "node_for_notebook_jobs"},
                        "config_maps": [{"name": "config_map1"}],
                    },
                },
            },
        }
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

        # Embedding a correct template
        config_dict = {
            "dependencies": ["foo", "bar"],
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
            "runPatch": {
                "kind": V1RunKind.JOB,
                "init": [
                    {"connection": "git-repo1", "git": {"revision": "dev"}},
                    {"connection": "git-repo1", "container": {"args": "--branch=dev"}},
                ],
            },
            "component": {
                "name": "build-template",
                "tags": ["lab"],
                "run": {
                    "kind": V1RunKind.JOB,
                    "environment": {
                        "nodeSelector": {"polyaxon.com": "node_for_notebook_jobs"}
                    },
                    "container": {"image": "jupyterlab"},
                },
            },
        }
        config = V1Operation.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_op_with_embedded_pipeline_template(self):
        # Embedding a bad template
        config_dict = {
            "dependencies": ["foo", "bar"],
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
            "component": {
                "version": 1.1,
                "key_not_supported": [
                    {"dagRef": "build-template", "name": "A"},
                    {"dagRef": "job-template", "name": "B", "dependencies": ["A"]},
                ],
                "run": {
                    "kind": "dag",
                    "operations": [
                        {
                            "kind": "operation",
                            "name": "job-template",
                            "component": {
                                "run": {
                                    "kind": V1RunKind.JOB,
                                    "container": {"image": "test"},
                                }
                            },
                        },
                        {
                            "kind": "operation",
                            "name": "build-template",
                            "tags": ["kaniko"],
                            "init": [{"connection": "foo", "git": {"branch": "dev"}}],
                        },
                    ],
                },
            },
        }
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

        # Embedding a template without container
        config_dict = {
            "dependencies": ["foo", "bar"],
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
            "component": {
                "run": {
                    "kind": "dag",
                    "operations": [
                        {
                            "kind": "operation",
                            "name": "A",
                            "component": {
                                "run": {
                                    "kind": V1RunKind.JOB,
                                    "container": {"image": "test"},
                                }
                            },
                        },
                        {
                            "kind": "operation",
                            "name": "B",
                            "dependencies": ["A"],
                            "tags": ["kaniko"],
                        },
                    ],
                }
            },
        }
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

        # Embedding a correct template
        config_dict = {
            "dependencies": ["foo", "bar"],
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
            "component": {
                "run": {
                    "kind": "dag",
                    "operations": [
                        {
                            "kind": "operation",
                            "name": "A",
                            "component": {
                                "run": {
                                    "kind": V1RunKind.JOB,
                                    "container": {"image": "test"},
                                }
                            },
                        },
                        {
                            "kind": "operation",
                            "name": "B",
                            "dependencies": ["A"],
                            "tags": ["kaniko"],
                            "component": {
                                "run": {
                                    "kind": V1RunKind.JOB,
                                    "init": [
                                        {
                                            "connection": "foo",
                                            "container": {"image": "foo"},
                                        }
                                    ],
                                    "container": {"image": "test"},
                                }
                            },
                        },
                    ],
                }
            },
        }
        config = V1Operation.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_op_with_embedded_non_supported_kind_template(self):
        config_dict = {
            "dependencies": ["foo", "bar"],
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "trigger": "all_succeeded",
            "component": {
                "run": {"run": {"kind": V1RunKind.JOB, "container": {"image": "test"}}}
            },
        }
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

    def test_op_and_hooks(self):
        config_dict = {
            "hooks": [
                {"trigger": "succeeded", "connection": "connection1", "hubRef": "ref1"},
                {"connection": "connection1", "hubRef": "ref2"},
            ],
            "component": {
                "run": {
                    "kind": V1RunKind.JOB,
                    "environment": {
                        "nodeSelector": {"polyaxon.com": "node_for_notebook_jobs"}
                    },
                    "container": {"image": "jupyterlab"},
                },
            },
        }
        config = V1Operation.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_op_and_joins(self):
        config_dict = {
            "joins": [
                {
                    "sort": 2,
                    "params": {
                        "u": {"value": "outputs.value"},
                    },
                },
            ],
            "component": {
                "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}}
            },
        }
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

        config_dict = {
            "joins": [
                {
                    "query": "dummy: query1",
                    "limit": "foo",
                },
            ],
            "component": {
                "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}}
            },
        }
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

        config_dict = {
            "joins": [
                {
                    "query": "dummy: query1",
                    "sort": "dummy sort1",
                    "params": {
                        "u": {"value": "outputs.value"},
                    },
                },
                {
                    "query": "dummy: query1",
                    "sort": "-dummy-sort2",
                    "params": {
                        "u": {"value": "artifacts"},
                    },
                },
            ],
            "component": {
                "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}}
            },
        }
        config = V1Operation.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_op_and_events(self):
        config_dict = {
            "events": [
                {"kinds": ["some-value"], "ref": "test"},
            ],
            "component": {
                "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}}
            },
        }
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

        config_dict = {
            "events": [
                {"kinds": [V1EventKind.RUN_STATUS_SCHEDULED]},
            ],
            "component": {
                "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}}
            },
        }
        with self.assertRaises(ValidationError):
            V1Operation.from_dict(config_dict)

        config_dict = {
            "events": [
                {"kinds": [V1EventKind.RUN_STATUS_SCHEDULED], "ref": "test.r1"},
            ],
            "component": {
                "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}}
            },
        }
        config = V1Operation.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_op_template(self):
        config_dict = {
            "hooks": [
                {"trigger": "succeeded", "connection": "connection1", "hubRef": "ref1"},
                {"connection": "connection1", "hubRef": "ref2"},
            ],
            "events": [
                {"kinds": [V1EventKind.RUN_STATUS_SCHEDULED], "ref": "test.r1"},
                {"kinds": [V1EventKind.RUN_NEW_ARTIFACTS], "ref": "test.r2"},
            ],
            "joins": [
                {
                    "query": "dummy: query1",
                    "sort": "dummy sort1",
                    "params": {
                        "u": {"value": "outputs.value"},
                    },
                },
                {
                    "query": "dummy: query1",
                    "sort": "-dummy-sort2",
                    "params": {
                        "u": {"value": "artifacts"},
                    },
                },
            ],
            "component": {
                "run": {
                    "kind": V1RunKind.JOB,
                    "environment": {
                        "nodeSelector": {"polyaxon.com": "node_for_notebook_jobs"}
                    },
                    "container": {"image": "jupyterlab"},
                },
            },
            "template": {
                "description": "This is a template, check the fields",
                "fields": ["actions[1].hubRef", "hooks[0].trigger"],
            },
        }
        config = V1Operation.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_from_hook(self):
        config_dict = {
            "connection": "test-connection",
            "trigger": "succeeded",
            "hubRef": "foo",
            "conditions": "foo > bar",
            "params": {"param1": {"value": "foo"}, "param2": {"value": "bar"}},
            "presets": ["pre1", "pre2"],
        }
        hook = V1Hook.from_dict(config_dict)

        op = V1Operation.from_hook(hook, None)
        assert op.run_patch["connections"] == [hook.connection]
        assert op.hub_ref == hook.hub_ref
        assert op.params == hook.params
        assert op.presets == hook.presets

        op = V1Operation.from_hook(
            hook,
            {
                "inputs": {"in1": "v1"},
                "outputs": {"out1": "v1"},
                "condition": {"c1": "v1"},
            },
        )
        assert op.run_patch["connections"] == [hook.connection]
        assert op.hub_ref == hook.hub_ref
        assert op.params == {
            **hook.params,
            "inputs": V1Param(value={"in1": "v1"}, context_only=True),
            "outputs": V1Param(value={"out1": "v1"}, context_only=True),
            "condition": V1Param(value={"c1": "v1"}, context_only=True),
        }
        assert op.presets == hook.presets
