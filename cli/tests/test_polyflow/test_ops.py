# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from marshmallow import ValidationError

from polyaxon.schemas.polyflow.ops import OpConfig


@pytest.mark.polyflow_mark
class TestOpConfigs(TestCase):
    def test_op_raises_for_template_action_event(self):
        config_dict = {"template": {"hub": "foo", "name": "bar"}}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {"template": {"path": "bar", "hub": "foo"}}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {"template": {"url": "bar", "hub": "foo"}}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

    def test_op_passes_for_template_hub(self):
        config_dict = {"template": {"hub": "bar"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"template": {"hub": "foo"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"template": {"path": "bar"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"template": {"url": "bar"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"template": {"name": "bar"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_validation(self):
        config_dict = {"template": {"hub": "foo"}, "concurrency": "foo"}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {"template": {"hub": "foo"}, "dependencies": "foo"}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {
            "template": {"hub": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
        }
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"template": {"hub": "foo"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {
            "template": {"name": "foo"},
            "dependencies": [{"name": "foo"}, {"name": "bar"}],  # Wrong
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

    def test_op_with_embedded_job_template(self):
        # Embedding a bad template
        config_dict = {
            "template": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "_template": {
                "kind": "job",
                "not_supported_key": "build-template",
                "tags": ["kaniko"],
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "container": {"image": "foo"},
            },
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        # Embedding a template without container
        config_dict = {
            "template": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "_template": {
                "kind": "job",
                "name": "build-template",
                "tags": ["kaniko"],
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
            },
        }
        with self.assertRaises(TypeError):
            OpConfig.from_dict(config_dict)

        # Embedding a correct template
        config_dict = {
            "template": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "_template": {
                "kind": "job",
                "name": "build-template",
                "tags": ["kaniko"],
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "container": {"image": "foo"},
            },
        }
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_op_with_embedded_service_template(self):
        # Embedding a bad template
        config_dict = {
            "template": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "_template": {
                "kind": "service",
                "not_supported_key": "build-template",
                "tags": ["lab"],
                "environment": {
                    "node_selector": {"polyaxon.com": "node_for_notebook_jobs"}
                },
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "mounts": {"config_maps": [{"name": "config_map1"}]},
                "container": {"image": "jupyterlab"},
            },
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        # Embedding a template without container
        config_dict = {
            "template": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "_template": {
                "kind": "service",
                "name": "build-template",
                "tags": ["lab"],
                "environment": {
                    "node_selector": {"polyaxon.com": "node_for_notebook_jobs"}
                },
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "mounts": {"config_maps": [{"name": "config_map1"}]},
            },
        }
        with self.assertRaises(TypeError):
            OpConfig.from_dict(config_dict)

        # Embedding a correct template
        config_dict = {
            "template": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "_template": {
                "kind": "service",
                "name": "build-template",
                "tags": ["lab"],
                "environment": {
                    "node_selector": {"polyaxon.com": "node_for_notebook_jobs"}
                },
                "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                "mounts": {"config_maps": [{"name": "config_map1"}]},
                "container": {"image": "jupyterlab"},
            },
        }
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_op_with_embedded_pipeline_template(self):
        # Embedding a bad template
        config_dict = {
            "template": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "_template": {
                "kind": "pipeline",
                "version": 0.6,
                "key_not_supported": [
                    {"template": {"name": "build-template"}, "name": "A"},
                    {
                        "template": {"name": "job-template"},
                        "name": "B",
                        "dependencies": ["A"],
                    },
                ],
                "templates": [
                    {
                        "kind": "job",
                        "name": "job-template",
                        "container": {"image": "test"},
                    },
                    {
                        "kind": "job",
                        "name": "build-template",
                        "tags": ["kaniko"],
                        "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                        "container": {"image": "test"},
                    },
                ],
            },
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        # Embedding a template without container
        config_dict = {
            "template": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "_template": {
                "kind": "pipeline",
                "version": 0.6,
                "ops": [
                    {"template": {"name": "build-template"}, "name": "A"},
                    {
                        "template": {"name": "job-template"},
                        "name": "B",
                        "dependencies": ["A"],
                    },
                ],
                "templates": [
                    {"kind": "job", "name": "job-template"},
                    {
                        "kind": "job",
                        "name": "build-template",
                        "tags": ["kaniko"],
                        "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                    },
                ],
            },
        }
        with self.assertRaises(TypeError):
            OpConfig.from_dict(config_dict)

        # Embedding a correct template
        config_dict = {
            "template": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "_template": {
                "kind": "pipeline",
                "version": 0.6,
                "ops": [
                    {"template": {"name": "build-template"}, "name": "A"},
                    {
                        "template": {"name": "job-template"},
                        "name": "B",
                        "dependencies": ["A"],
                    },
                ],
                "templates": [
                    {
                        "kind": "job",
                        "name": "job-template",
                        "container": {"image": "test"},
                    },
                    {
                        "kind": "job",
                        "name": "build-template",
                        "tags": ["kaniko"],
                        "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                        "container": {"image": "test"},
                    },
                ],
            },
        }
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_op_with_embedded_non_supported_kind_template(self):
        config_dict = {
            "template": {"name": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
            "_template": {
                "kind": "foo",
                "ops": [
                    {"template": {"name": "build-template"}, "name": "A"},
                    {
                        "template": {"name": "job-template"},
                        "name": "B",
                        "dependencies": ["A"],
                    },
                ],
                "templates": [
                    {"kind": "job", "name": "job-template"},
                    {
                        "kind": "job",
                        "name": "build-template",
                        "tags": ["kaniko"],
                        "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                    },
                ],
            },
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)
