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

# coding: utf-8
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from marshmallow import ValidationError

from polyaxon.schemas.polyflow.op import OpConfig


@pytest.mark.ops_mark
class TestOpConfigs(TestCase):
    def test_op_raises_for_template_action_event(self):
        config_dict = {"component_ref": {"hub": "foo", "name": "bar"}}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {"component_ref": {"path": "bar", "hub": "foo"}}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {"component_ref": {"url": "bar", "hub": "foo"}}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

    def test_op_passes_for_template_hub(self):
        config_dict = {"component_ref": {"hub": "bar"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"component_ref": {"hub": "foo"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"component_ref": {"path": "bar"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"component_ref": {"url": "bar"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"component_ref": {"name": "bar"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_validation(self):
        config_dict = {"component_ref": {"hub": "foo"}, "concurrency": "foo"}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {"component_ref": {"hub": "foo"}, "dependencies": "foo"}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {
            "component_ref": {"hub": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
        }
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"component_ref": {"hub": "foo"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {
            "component_ref": {"name": "foo"},
            "dependencies": [{"name": "foo"}, {"name": "bar"}],  # Wrong
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

    def test_op_with_embedded_job_template(self):
        # Embedding a bad template
        config_dict = {
            "component_ref": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "component": {
                "kind": "component",
                "not_supported_key": "build-template",
                "tags": ["kaniko"],
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "run": {"kind": "container", "image": "test"},
            },
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        # Embedding a template without container
        config_dict = {
            "component_ref": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "component": {
                "kind": "component",
                "name": "build-template",
                "tags": ["kaniko"],
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
            },
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        # Embedding a correct template
        config_dict = {
            "component_ref": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "component": {
                "kind": "component",
                "name": "build-template",
                "tags": ["kaniko"],
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "run": {"kind": "container", "image": "test"},
            },
        }
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_op_with_embedded_service_template(self):
        # Embedding a bad template
        config_dict = {
            "component_ref": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "component": {
                "kind": "component",
                "not_supported_key": "build-template",
                "tags": ["lab"],
                "environment": {
                    "node_selector": {"polyaxon.com": "node_for_notebook_jobs"}
                },
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "mounts": {"config_maps": [{"name": "config_map1"}]},
                "run": {"kind": "container", "image": "jupyterlab"},
            },
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        # Embedding a correct template
        config_dict = {
            "component_ref": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "component": {
                "kind": "component",
                "name": "build-template",
                "tags": ["lab"],
                "environment": {
                    "node_selector": {"polyaxon.com": "node_for_notebook_jobs"}
                },
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "mounts": {"config_maps": [{"name": "config_map1"}]},
                "run": {"kind": "container", "image": "jupyterlab"},
            },
        }
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_op_with_embedded_pipeline_template(self):
        # Embedding a bad template
        config_dict = {
            "component_ref": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "component": {
                "kind": "component",
                "version": 1.0,
                "key_not_supported": [
                    {"component_ref": {"name": "build-template"}, "name": "A"},
                    {
                        "component_ref": {"name": "job-template"},
                        "name": "B",
                        "dependencies": ["A"],
                    },
                ],
                "run": {
                    "kind": "dag",
                    "ops": [
                        {
                            "kind": "op",
                            "name": "job-template",
                            "component": {
                                "run": {"kind": "container", "image": "test"}
                            },
                        },
                        {
                            "kind": "op",
                            "name": "build-template",
                            "tags": ["kaniko"],
                            "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                        },
                    ],
                },
            },
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        # Embedding a template without container
        config_dict = {
            "component_ref": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "component": {
                "run": {
                    "kind": "dag",
                    "ops": [
                        {
                            "kind": "op",
                            "name": "A",
                            "component": {
                                "run": {"kind": "container", "image": "test"}
                            },
                        },
                        {
                            "kind": "op",
                            "name": "B",
                            "dependencies": ["A"],
                            "tags": ["kaniko"],
                            "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                        },
                    ],
                }
            },
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        # Embedding a correct template
        config_dict = {
            "component_ref": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "component": {
                "run": {
                    "kind": "dag",
                    "ops": [
                        {
                            "kind": "op",
                            "name": "A",
                            "component": {
                                "run": {"kind": "container", "image": "test"}
                            },
                        },
                        {
                            "kind": "op",
                            "name": "B",
                            "dependencies": ["A"],
                            "tags": ["kaniko"],
                            "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                            "component": {
                                "run": {"kind": "container", "image": "test"}
                            },
                        },
                    ],
                }
            },
        }
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_op_with_embedded_non_supported_kind_template(self):
        config_dict = {
            "component_ref": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "component": {"kind": "foo", "run": {"kind": "container", "image": "test"}},
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)
