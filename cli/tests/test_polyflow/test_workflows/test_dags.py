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

from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.schemas.polyflow import dags
from polyaxon.schemas.polyflow import params as ops_params
from polyaxon.schemas.polyflow.component_ref import ComponentRefConfig
from polyaxon.schemas.polyflow.io import IOConfig
from polyaxon.schemas.polyflow.op import OpConfig
from polyaxon.schemas.polyflow.run import DagConfig
from polyaxon.types import types


@pytest.mark.workflow_mark
class TestWorkflowDagConfigs(TestCase):
    def test_wrong_pipelines_ops(self):
        config_dict = {"ops": "foo"}
        with self.assertRaises(ValidationError):
            DagConfig.from_dict(config_dict)

        config_dict = {"ops": ["foo"]}
        with self.assertRaises(ValidationError):
            DagConfig.from_dict(config_dict)

    def test_dag_ops(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "name": "A",
                    "component_ref": {"hub": "action1"},
                    "description": "description A",
                    "tags": ["tag11", "tag12"],
                    "params": {
                        "param1": "text",
                        "param2": 12,
                        "param3": "https://foo.com",
                    },
                    "environment": {
                        "resources": {"requests": {"cpu": 1}},
                        "node_selector": {"polyaxon": "core"},
                        "service_account": "service",
                        "image_pull_secrets": ["secret1", "secret2"],
                    },
                    "termination": {"max_retries": 2},
                },
                {
                    "component_ref": {"url": "https://url-to-temaplte.com"},
                    "name": "B",
                    "description": "description B",
                    "tags": ["tag11", "tag12"],
                    "params": {
                        "param1": "{{ ops.A.outputs.x }}",
                        "param2": 12,
                        "param3": "https://foo.com",
                    },
                    "environment": {
                        "resources": {"requests": {"cpu": 1}},
                        "node_selector": {"polyaxon": "core"},
                        "service_account": "service",
                        "image_pull_secrets": ["secret1", "secret2"],
                    },
                    "termination": {"max_retries": 2},
                },
                {
                    "component_ref": {"name": "my-template"},
                    "name": "C",
                    "description": "description C",
                    "tags": ["tag31", "tag32"],
                    "params": {"param2": 12.34, "param3": False},
                    "environment": {
                        "resources": {"requests": {"cpu": 1}},
                        "node_selector": {"polyaxon": "core"},
                        "service_account": "service",
                        "image_pull_secrets": ["secret1", "secret2"],
                    },
                    "termination": {"max_retries": 5, "restart_policy": "never"},
                },
                {
                    "component_ref": {"path": "./relative/path/to/my-template.yaml"},
                    "name": "D",
                    "description": "description D",
                    "tags": ["tag31", "tag32"],
                    "dependencies": ["B", "C"],
                    "environment": {
                        "resources": {"requests": {"cpu": 1}},
                        "node_selector": {"polyaxon": "core"},
                        "service_account": "service",
                        "image_pull_secrets": ["secret1", "secret2"],
                    },
                    "termination": {"max_retries": 3, "restart_policy": "never"},
                },
            ],
        }
        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        config.process_dag()
        config.validate_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()

    def test_pipelines_components(self):
        config_dict = {
            "kind": "dag",
            "components": [
                {
                    "kind": "component",
                    "name": "experiment-template",
                    "description": "description experiment",
                    "tags": ["tag11", "tag12"],
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.FLOAT,
                        },
                        {
                            "name": "input2",
                            "description": "some text",
                            "type": types.BOOL,
                            "is_optional": True,
                            "value": True,
                        },
                    ],
                    "outputs": [
                        {
                            "name": "output1",
                            "description": "some text",
                            "type": types.S3,
                        }
                    ],
                    "environment": {
                        "resources": {"requests": {"cpu": "500m"}},
                        "node_selector": {"polyaxon": "core"},
                        "service_account": "service",
                        "image_pull_secrets": ["secret1", "secret2"],
                    },
                    "termination": {"max_retries": 2, "restart_policy": "never"},
                    "run": {"kind": "container", "image": "test"},
                }
            ],
        }

        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        config.process_dag()
        config.validate_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()

    def test_dag_job_component_with_correct_params(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "name": "experiment-template",
                    "params": {"input1": 1.1, "input2": False},
                    "component": {
                        "kind": "component",
                        "description": "description experiment",
                        "tags": ["tag11", "tag12"],
                        "inputs": [
                            {
                                "name": "input1",
                                "description": "some text",
                                "type": types.FLOAT,
                            },
                            {
                                "name": "input2",
                                "description": "some text",
                                "type": types.BOOL,
                                "is_optional": True,
                                "value": True,
                            },
                        ],
                        "outputs": [
                            {
                                "name": "output1",
                                "description": "some text",
                                "type": types.S3,
                            }
                        ],
                        "environment": {
                            "resources": {"requests": {"cpu": "500m"}},
                            "node_selector": {"polyaxon": "core"},
                            "service_account": "service",
                            "image_pull_secrets": ["secret1", "secret2"],
                        },
                        "termination": {"max_retries": 2, "restart_policy": "never"},
                        "run": {"kind": "container", "image": "test"},
                    },
                }
            ],
        }
        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        config.process_dag()
        config.validate_dag()
        config.process_components(
            inputs=[IOConfig.from_dict({"name": "input_pipe", "type": types.S3})]
        )

    def test_dag_structure(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"hub": "action1"},
                    "name": "A",
                    "params": {
                        "param1": "text",
                        "param2": 12,
                        "param3": "https://foo.com",
                    },
                },
                {
                    "component_ref": {"url": "https://url-to-temaplte.com"},
                    "name": "B",
                    "params": {
                        "param1": "{{ ops.A.outputs.x }}",
                        "param2": 12,
                        "param3": "https://foo.com",
                    },
                },
                {
                    "component_ref": {"name": "my-template"},
                    "name": "C",
                    "params": {"param2": 12.34, "param3": False},
                },
                {
                    "component_ref": {"path": "./relative/path/to/my-template.yaml"},
                    "name": "D",
                    "dependencies": ["B", "C"],
                },
            ],
        }
        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()

        config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {"A", "C"}
        assert dags.get_independent_ops(dag=dag) == {"A", "C"}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert dags.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert sorted_dag[0] in [["A", "C"], ["C", "A"]]
        assert sorted_dag[1] == ["B"]
        assert sorted_dag[2] == ["D"]

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "action1"}
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {
            "url": "https://url-to-temaplte.com"
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"name": "my-template"}
        assert config.dag["C"].upstream == set()
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.component_ref.to_dict() == {
            "path": "./relative/path/to/my-template.yaml"
        }
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

    def test_dag_parallel_ops(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {"component_ref": {"hub": "action1"}, "name": "A"},
                {"component_ref": {"hub": "event1"}, "name": "B"},
                {"component_ref": {"name": "foo"}, "name": "C"},
                {"component_ref": {"name": "bar"}, "name": "D"},
            ],
        }

        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {"A", "B", "C", "D"}
        assert dags.get_independent_ops(dag=dag) == {"A", "B", "C", "D"}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert dags.get_orphan_ops(dag=dag) == set([])
        assert len(config.sort_topologically(dag=dag)) == 1  # order can be any
        assert len(config.sort_topologically(dag=dag)[0]) == 4  # order can be any

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "action1"}
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == set()

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "event1"}
        assert config.dag["B"].upstream == set()
        assert config.dag["B"].downstream == set()

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"name": "foo"}
        assert config.dag["C"].upstream == set()
        assert config.dag["C"].downstream == set()

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.component_ref.to_dict() == {"name": "bar"}
        assert config.dag["D"].upstream == set()
        assert config.dag["D"].downstream == set()

    def test_dag_sequential_ops(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {"component_ref": {"hub": "action1"}, "name": "A"},
                {
                    "component_ref": {"hub": "event1"},
                    "name": "B",
                    "dependencies": ["A"],
                },
                {"component_ref": {"name": "foo"}, "name": "C", "dependencies": ["B"]},
                {"component_ref": {"name": "bar"}, "name": "D", "dependencies": ["C"]},
            ],
        }

        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()

        config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {"A"}
        assert dags.get_independent_ops(dag=dag) == {"A"}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert dags.get_orphan_ops(dag=dag) == set([])
        assert config.sort_topologically(dag=dag) == [["A"], ["B"], ["C"], ["D"]]
        assert dags.sort_topologically(dag=dag) == [["A"], ["B"], ["C"], ["D"]]

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "action1"}
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "event1"}
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"C"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"name": "foo"}
        assert config.dag["C"].upstream == {"B"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.component_ref.to_dict() == {"name": "bar"}
        assert config.dag["D"].upstream == {"C"}
        assert config.dag["D"].downstream == set()

    def test_dag_all_downstream(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"hub": "action1"},
                    "name": "A",
                    "params": {
                        "param1": "text",
                        "param2": 12,
                        "param3": "https://foo.com",
                    },
                    "dependencies": ["B", "C", "D"],
                },
                {"component_ref": {"hub": "event1"}, "name": "B"},
                {"component_ref": {"hub": "event2"}, "name": "C"},
                {"component_ref": {"hub": "event3"}, "name": "D"},
            ],
        }

        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        # No components
        config.process_components()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {"B", "C", "D"}
        assert dags.get_independent_ops(dag=dag) == {"B", "C", "D"}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert dags.get_orphan_ops(dag=dag) == set([])

        sorted_dag = config.sort_topologically(dag=dag)
        assert dags.sort_topologically(dag=dag) == sorted_dag
        # Sort is not guaranteed at stage 0
        assert len(sorted_dag[0]) == 3
        assert set(sorted_dag[0]) == {"B", "C", "D"}
        assert sorted_dag[1] == ["A"]

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "action1"}
        assert config.dag["A"].upstream == {"B", "C", "D"}
        assert config.dag["A"].downstream == set()

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "event1"}
        assert config.dag["B"].upstream == set()
        assert config.dag["B"].downstream == {"A"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"hub": "event2"}
        assert config.dag["C"].upstream == set()
        assert config.dag["C"].downstream == {"A"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.component_ref.to_dict() == {"hub": "event3"}
        assert config.dag["D"].upstream == set()
        assert config.dag["D"].downstream == {"A"}

    def test_dag_acyclic_deps(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"hub": "action1"},
                    "name": "A",
                    "dependencies": ["B"],
                },
                {
                    "component_ref": {"hub": "event1"},
                    "name": "B",
                    "dependencies": ["A"],
                },
                {"component_ref": {"name": "foo"}, "name": "C", "dependencies": ["A"]},
            ],
        }

        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()
        with self.assertRaises(PolyaxonSchemaError):
            config.validate_dag()
        dag = config.dag
        assert len(dag) == 3
        assert config.get_independent_ops(dag=dag) == set()
        assert dags.get_independent_ops(dag=dag) == set()
        assert config.get_orphan_ops(dag=dag) == set()
        assert dags.get_orphan_ops(dag=dag) == set()
        with self.assertRaises(PolyaxonSchemaError):
            config.sort_topologically(dag=dag)
        with self.assertRaises(PolyaxonSchemaError):
            dags.sort_topologically(dag=dag)

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "action1"}
        assert config.dag["A"].upstream == {"B"}
        assert config.dag["A"].downstream == {"B", "C"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "event1"}
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"A"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"name": "foo"}
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == set()

    def test_dag_circular_deps(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"hub": "action1"},
                    "name": "A",
                    "dependencies": ["C"],
                },
                {
                    "component_ref": {"hub": "event1"},
                    "name": "B",
                    "dependencies": ["A"],
                },
                {"component_ref": {"name": "foo"}, "name": "C", "dependencies": ["B"]},
            ],
        }

        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()
        with self.assertRaises(PolyaxonSchemaError):
            config.validate_dag()
        dag = config.dag
        assert len(dag) == 3
        assert config.get_independent_ops(dag=dag) == set()
        assert dags.get_independent_ops(dag=dag) == set()
        assert config.get_orphan_ops(dag=dag) == set()
        assert dags.get_orphan_ops(dag=dag) == set()
        with self.assertRaises(PolyaxonSchemaError):
            config.sort_topologically(dag=dag)
        with self.assertRaises(PolyaxonSchemaError):
            dags.sort_topologically(dag=dag)

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "action1"}
        assert config.dag["A"].upstream == {"C"}
        assert config.dag["A"].downstream == {"B"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "event1"}
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"C"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"name": "foo"}
        assert config.dag["C"].upstream == {"B"}
        assert config.dag["C"].downstream == {"A"}

    def test_dag_adding_ops_one_by_one_manually(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {"component_ref": {"hub": "action1"}, "name": "A"},
                {
                    "component_ref": {"hub": "event1"},
                    "name": "B",
                    "dependencies": ["A"],
                },
                {"component_ref": {"name": "foo"}, "name": "C", "dependencies": ["A"]},
            ],
        }

        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 3
        assert config.get_independent_ops(dag=dag) == {"A"}
        assert config.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert dags.sort_topologically(dag=dag) == sorted_dag
        assert sorted_dag[0] == ["A"]  # Only this one has consistent order
        assert sorted_dag[1] in [["B", "C"], ["C", "B"]]

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "action1"}
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "event1"}
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == set()

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"name": "foo"}
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == set()

        template4 = ComponentRefConfig.from_dict({"hub": "action4"})
        operationD = OpConfig(
            component_ref=template4, name="D", dependencies=["B", "C"]
        )
        config.add_op(operationD)

        operationE = OpConfig(component_ref=template4, name="E", dependencies=["A"])
        config.add_op(operationE)

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 5
        assert config.get_independent_ops(dag=dag) == {"A"}
        assert dags.get_independent_ops(dag=dag) == {"A"}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert dags.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert config.sort_topologically(dag=dag) == sorted_dag
        assert sorted_dag[0] == ["A"]
        # Sort is not guaranteed at stage 1
        assert len(sorted_dag[1]) == 3
        assert set(sorted_dag[1]) == {"B", "C", "E"}
        assert sorted_dag[2] == ["D"]

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "action1"}
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C", "E"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "event1"}
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"name": "foo"}
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.component_ref.to_dict() == {"hub": "action4"}
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

        assert config.dag["E"].op.name == "E"
        assert config.dag["E"].op.component_ref.to_dict() == {"hub": "action4"}
        assert config.dag["E"].upstream == {"A"}
        assert config.dag["E"].downstream == set()

        # Adding the same ops should not alter the behaviour
        config.add_ops([operationD, operationE])

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 5
        assert config.get_independent_ops(dag=dag) == {"A"}
        assert dags.get_independent_ops(dag=dag) == {"A"}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert dags.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert config.sort_topologically(dag=dag) == sorted_dag
        assert sorted_dag[0] == ["A"]
        # Sort is not guaranteed at stage 1
        assert len(sorted_dag[1]) == 3
        assert set(sorted_dag[1]) == {"B", "C", "E"}
        assert sorted_dag[2] == ["D"]

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "action1"}
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C", "E"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "event1"}
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"name": "foo"}
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.component_ref.to_dict() == {"hub": "action4"}
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

        assert config.dag["E"].op.name == "E"
        assert config.dag["E"].op.component_ref.to_dict() == {"hub": "action4"}
        assert config.dag["E"].upstream == {"A"}
        assert config.dag["E"].downstream == set()

    def test_dag_adding_ops_many_manually(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {"component_ref": {"hub": "action1"}, "name": "A"},
                {
                    "component_ref": {"hub": "event1"},
                    "name": "B",
                    "dependencies": ["A"],
                },
                {"component_ref": {"name": "foo"}, "name": "C", "dependencies": ["A"]},
            ],
        }

        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 3
        assert config.get_independent_ops(dag=dag) == {"A"}
        assert dags.get_independent_ops(dag=dag) == {"A"}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert dags.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert config.sort_topologically(dag=dag) == sorted_dag
        assert sorted_dag[0] == ["A"]  # Only this one has consistent order
        assert sorted_dag[1] in [["B", "C"], ["C", "B"]]

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "action1"}
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "event1"}
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == set()

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"name": "foo"}
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == set()

        template4 = ComponentRefConfig.from_dict({"hub": "action4"})
        operationD = OpConfig(
            component_ref=template4, name="D", dependencies=["B", "C"]
        )
        operationE = OpConfig(component_ref=template4, name="E", dependencies=["A"])
        config.add_ops([operationD, operationE])

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()
        config.validate_dag()
        assert len(config.dag) == 5
        assert config.get_independent_ops(dag=config.dag) == {"A"}
        assert dags.get_independent_ops(dag=config.dag) == {"A"}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert dags.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert config.sort_topologically(dag=dag) == sorted_dag
        assert sorted_dag[0] == ["A"]
        # Sort is not guaranteed at stage 1
        assert len(sorted_dag[1]) == 3
        assert set(sorted_dag[1]) == {"B", "C", "E"}
        assert sorted_dag[2] == ["D"]

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "action1"}
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C", "E"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "event1"}
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"name": "foo"}
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.component_ref.to_dict() == {"hub": "action4"}
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

        assert config.dag["E"].op.name == "E"
        assert config.dag["E"].op.component_ref.to_dict() == {"hub": "action4"}
        assert config.dag["E"].upstream == {"A"}
        assert config.dag["E"].downstream == set()

        # Adding the same ops should not alter the behaviour
        config.add_op(operationD)
        config.add_op(operationE)

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 5
        assert config.get_independent_ops(dag=dag) == {"A"}
        assert dags.get_independent_ops(dag=dag) == {"A"}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert dags.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert config.sort_topologically(dag=dag) == sorted_dag
        assert sorted_dag[0] == ["A"]
        # Sort is not guaranteed at stage 1
        assert len(sorted_dag[1]) == 3
        assert set(sorted_dag[1]) == {"B", "C", "E"}
        assert sorted_dag[2] == ["D"]

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "action1"}
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C", "E"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "event1"}
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"name": "foo"}
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.component_ref.to_dict() == {"hub": "action4"}
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

        assert config.dag["E"].op.name == "E"
        assert config.dag["E"].op.component_ref.to_dict() == {"hub": "action4"}
        assert config.dag["E"].upstream == {"A"}
        assert config.dag["E"].downstream == set()

    def test_dag_dependency_from_params(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"hub": "echo"},
                    "name": "A",
                    "params": {
                        "param1": "text",
                        "param2": 12,
                        "param3": "https://foo.com",
                    },
                },
                {
                    "component_ref": {"hub": "echo"},
                    "name": "B",
                    "params": {
                        "param1": "{{ ops.A.outputs.x }}",
                        "param2": 12,
                        "param3": "https://foo.com",
                    },
                },
                {
                    "component_ref": {"hub": "echo"},
                    "name": "C",
                    "params": {
                        "param1": "{{ ops.A.outputs.x }}",
                        "param2": "{{ ops.B.outputs.x }}",
                    },
                },
                {
                    "component_ref": {"hub": "echo"},
                    "name": "D",
                    "dependencies": ["B", "C"],
                },
            ],
        }

        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        # Todo must resolve the components from the hub
        config.process_components()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {"A"}
        assert dags.get_independent_ops(dag=dag) == {"A"}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert dags.get_orphan_ops(dag=dag) == set([])
        assert config.sort_topologically(dag=dag) == [["A"], ["B"], ["C"], ["D"]]
        assert dags.sort_topologically(dag=dag) == [["A"], ["B"], ["C"], ["D"]]

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "echo"}
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "echo"}
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"C", "D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"hub": "echo"}
        assert config.dag["C"].upstream == {"A", "B"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.component_ref.to_dict() == {"hub": "echo"}
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

    def test_dag_dependency_and_params(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"hub": "echo"},
                    "name": "A",
                    "params": {
                        "param1": "text",
                        "param2": 12,
                        "param3": "https://foo.com",
                    },
                },
                {
                    "component_ref": {"hub": "echo"},
                    "name": "B",
                    "params": {
                        "param1": "{{ ops.A.outputs.x }}",
                        "param2": 12,
                        "param3": "https://foo.com",
                    },
                    "dependencies": ["A"],
                },
                {
                    "component_ref": {"hub": "echo"},
                    "name": "C",
                    "params": {"param2": "{{ ops.B.outputs.x }}"},
                    "dependencies": ["A"],
                },
                {
                    "component_ref": {"hub": "echo"},
                    "name": "D",
                    "dependencies": ["B", "C"],
                },
            ],
        }

        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        # TODO resolve components from hub
        config.process_components()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {"A"}
        assert dags.get_independent_ops(dag=dag) == {"A"}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert dags.get_orphan_ops(dag=dag) == set([])
        assert config.sort_topologically(dag=dag) == [["A"], ["B"], ["C"], ["D"]]
        assert dags.sort_topologically(dag=dag) == [["A"], ["B"], ["C"], ["D"]]

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "echo"}
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "echo"}
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"C", "D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"hub": "echo"}
        assert config.dag["C"].upstream == {"A", "B"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.component_ref.to_dict() == {"hub": "echo"}
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

    def test_dag_orphan_ops(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {"component_ref": {"hub": "action1"}, "name": "A"},
                {
                    "component_ref": {"hub": "event1"},
                    "name": "B",
                    "dependencies": ["A"],
                },
                {
                    "component_ref": {"name": "foo"},
                    "name": "C",
                    "dependencies": ["A", "E"],
                },
            ],
        }

        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()
        with self.assertRaises(PolyaxonSchemaError):
            config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {"A", "E"}
        assert dags.get_independent_ops(dag=dag) == {"A", "E"}
        assert config.get_orphan_ops(dag=dag) == {"E"}
        assert dags.get_orphan_ops(dag=dag) == {"E"}
        sorted_dag = config.sort_topologically(dag=dag)
        assert config.sort_topologically(dag=dag) == sorted_dag
        assert sorted_dag[0] in [["A", "E"], ["E", "A"]]
        assert sorted_dag[1] in [["B", "C"], ["C", "B"]]

        assert config.dag["A"].op.name == "A"
        assert config.dag["A"].op.component_ref.to_dict() == {"hub": "action1"}
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.component_ref.to_dict() == {"hub": "event1"}
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == set()

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.component_ref.to_dict() == {"name": "foo"}
        assert config.dag["C"].upstream == {"A", "E"}
        assert config.dag["C"].downstream == set()

    def test_dag_with_duplicate_job_names(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {"component_ref": {"name": "build-template1"}, "name": "A"},
                {"component_ref": {"name": "build-template1"}, "name": "A"},
            ],
            "components": [
                {
                    "name": "build-template",
                    "description": "description build",
                    "tags": ["tag11", "tag12"],
                    "run": {"kind": "container", "image": "test"},
                },
                {
                    "name": "job-template",
                    "description": "description build",
                    "run": {"kind": "container", "image": "test"},
                },
            ],
        }
        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()

    def test_dag_with_op_requesting_undefined_template(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {"component_ref": {"name": "build-template1"}, "name": "A"},
                {"component_ref": {"name": "build-template1"}, "name": "B"},
            ],
            "components": [
                {
                    "kind": "component",
                    "name": "build-template2",
                    "description": "description build",
                    "tags": ["kaniko"],
                    "environment": {"registry": "A"},
                    "mounts": {"artifacts": [{"name": "data2"}]},
                    "run": {"kind": "container", "image": "test"},
                }
            ],
        }
        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()

    def test_dag_with_template_not_defining_inputs(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {"component_ref": {"name": "build-template"}, "name": "A"},
                {
                    "component_ref": {"name": "job-template"},
                    "name": "B",
                    "dependencies": ["A"],
                },
            ],
            "components": [
                {"name": "job-template", "run": {"kind": "container", "image": "test"}},
                {
                    "name": "build-template",
                    "tags": ["kaniko"],
                    "init": {"repos": [{"name": "foo", "branch": "dev"}]},
                    "run": {"kind": "container", "image": "test"},
                },
            ],
        }
        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        # Trying to set op template before processing components
        with self.assertRaises(PolyaxonSchemaError):
            config.set_op_component("A")
        config.process_components()
        # Trying to set op template before processing dag
        with self.assertRaises(PolyaxonSchemaError):
            config.set_op_component("A")
        config.process_dag()
        assert config.dag["A"].op.component is None
        assert config.dag["B"].op.component is None
        config.set_op_component("A")
        assert config.dag["B"].op.component is None
        assert config.dag["A"].op.component is not None
        assert (
            config.dag["A"].op.component
            == config._components_by_names["build-template"]
        )
        config.set_op_component("B")
        assert config.dag["B"].op.component is not None
        assert (
            config.dag["B"].op.component == config._components_by_names["job-template"]
        )

    def test_dag_with_template_not_defining_inputs_and_ops_with_params(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "name": "A",
                    "component": {
                        "kind": "component",
                        "name": "build-template",
                        "tags": ["kaniko"],
                        "run": {"kind": "container", "image": "test"},
                    },
                },
                {
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {
                        "param1": "{{ ops.A.outputs.x }}",
                        "param2": 12,
                        "param3": "https://foo.com",
                    },
                    "component": {
                        "kind": "component",
                        "name": "job-template",
                        "run": {"kind": "container", "image": "test"},
                    },
                },
            ],
        }
        config = DagConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_pipelines_with_template_not_defining_inputs_and_ops_with_params_template(
        self
    ):
        config_dict = {
            "kind": "dag",
            "ops": [
                {"component_ref": {"name": "build-template"}, "name": "A"},
                {
                    "component_ref": {"name": "job-template"},
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {
                        "param1": "{{ ops.A.outputs.x }}",
                        "param2": 12,
                        "param3": "https://foo.com",
                    },
                },
            ],
            "components": [
                {"name": "job-template", "run": {"kind": "container", "image": "test"}},
                {
                    "name": "build-template",
                    "tags": ["kaniko"],
                    "run": {"kind": "container", "image": "test"},
                },
            ],
        }
        config = DagConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_dag_with_ops_template_required_inputs(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "name": "A",
                    "component": {
                        "kind": "component",
                        "name": "job-template",
                        "inputs": [
                            {
                                "name": "input1",
                                "description": "some text",
                                "type": types.FLOAT,
                            }
                        ],
                        "run": {"kind": "container", "image": "test"},
                    },
                }
            ],
        }
        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_pipelines_with_ops_template_required_inputs_template(self):
        config_dict = {
            "kind": "dag",
            "ops": [{"component_ref": {"name": "job-template"}, "name": "A"}],
            "components": [
                {
                    "name": "job-template",
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.FLOAT,
                        }
                    ],
                    "run": {"kind": "container", "image": "test"},
                }
            ],
        }
        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_dag_with_ops_template_optional_inputs(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"name": "job-template"},
                    "name": "A",
                    "component": {
                        "name": "job-template",
                        "inputs": [
                            {
                                "name": "input1",
                                "description": "some text",
                                "type": types.FLOAT,
                                "is_optional": True,
                                "value": 12.2,
                            }
                        ],
                        "run": {"kind": "container", "image": "test"},
                    },
                }
            ],
        }
        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        config.process_components()

    def test_pipelines_with_ops_template_optional_inputs_template(self):
        config_dict = {
            "kind": "dag",
            "ops": [{"component_ref": {"name": "job-template"}, "name": "A"}],
            "components": [
                {
                    "name": "job-template",
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.FLOAT,
                            "is_optional": True,
                            "value": 12.2,
                        }
                    ],
                    "run": {"kind": "container", "image": "test"},
                }
            ],
        }
        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        config.process_components()

    def test_dag_with_ops_template_optional_inputs_and_wrong_param(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"name": "job-template"},
                    "name": "A",
                    "params": {"input1": "foo"},
                    "component": {
                        "name": "job-template",
                        "inputs": [
                            {
                                "name": "input1",
                                "description": "some text",
                                "type": types.FLOAT,
                                "is_optional": True,
                                "value": 12.2,
                            }
                        ],
                        "run": {"kind": "container", "image": "test"},
                    },
                }
            ],
        }
        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_pipelines_with_ops_template_optional_inputs_and_wrong_param_components(
        self
    ):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"name": "job-template"},
                    "name": "A",
                    "params": {"input1": "foo"},
                }
            ],
            "components": [
                {
                    "name": "job-template",
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.FLOAT,
                            "is_optional": True,
                            "value": 12.2,
                        }
                    ],
                    "run": {"kind": "container", "image": "test"},
                }
            ],
        }
        config = DagConfig.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_dag_with_ops_template_validation(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"name": "job-template"},
                    "name": "A",
                    "params": {"input1": "sdf", "input2": 12.0, "input3": False},
                },
                {
                    "component_ref": {"name": "job-template"},
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {"input1": "ooo", "input2": 12.123},
                },
            ],
            "components": [
                {
                    "kind": "component",
                    "name": "job-template",
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.STR,
                        },
                        {
                            "name": "input2",
                            "description": "some text",
                            "type": types.FLOAT,
                        },
                        {
                            "name": "input3",
                            "description": "some text",
                            "type": types.BOOL,
                            "is_optional": True,
                            "value": True,
                        },
                    ],
                    "run": {"kind": "container", "image": "test"},
                }
            ],
        }
        config = DagConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        # Trying to set op template before processing components
        with self.assertRaises(PolyaxonSchemaError):
            config.set_op_component("A")
        config.process_components()
        # Trying to set op template before processing dag
        with self.assertRaises(PolyaxonSchemaError):
            config.set_op_component("A")
        config.process_dag()
        assert config.dag["A"].op.component is None
        assert config.dag["B"].op.component is None
        config.set_op_component("A")
        assert config.dag["B"].op.component is None
        assert config.dag["A"].op.component is not None
        assert (
            config.dag["A"].op.component == config._components_by_names["job-template"]
        )
        config.set_op_component("B")
        assert config.dag["B"].op.component is not None
        assert (
            config.dag["B"].op.component == config._components_by_names["job-template"]
        )

    def test_dag_with_wrong_refs(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"name": "job-template"},
                    "name": "A",
                    "params": {"input1": "sdf", "input2": 12.0, "input3": False},
                },
                {
                    "component_ref": {"name": "job-template"},
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {
                        "input1": "{{ ops.A.outputs.output1 }}",
                        "input2": 12.123,
                    },
                },
            ],
            "components": [
                {
                    "name": "job-template",
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.STR,
                        },
                        {
                            "name": "input2",
                            "description": "some text",
                            "type": types.FLOAT,
                        },
                        {
                            "name": "input3",
                            "description": "some text",
                            "type": types.BOOL,
                            "is_optional": True,
                            "value": True,
                        },
                    ],
                    "run": {"kind": "container", "image": "test"},
                }
            ],
        }
        config = DagConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_dag_with_correct_refs(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"name": "job-template"},
                    "name": "A",
                    "params": {"input1": 2, "input2": "gs://bucket/path/to/blob/"},
                },
                {
                    "component_ref": {"name": "job-template"},
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {
                        "input1": "{{ ops.A.outputs.output1 }}",
                        "input2": "gs://bucket/path/to/blob/",
                    },
                },
            ],
            "components": [
                {
                    "name": "job-template",
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.INT,
                        },
                        {
                            "name": "input2",
                            "description": "some text",
                            "type": types.GCS,
                        },
                        {
                            "name": "input3",
                            "description": "some text",
                            "type": types.BOOL,
                            "is_optional": True,
                            "value": True,
                        },
                    ],
                    "outputs": [
                        {
                            "name": "output1",
                            "description": "some text",
                            "type": types.INT,
                            "is_optional": True,
                            "value": 123,
                        }
                    ],
                    "run": {"kind": "container", "image": "test"},
                }
            ],
        }
        config = DagConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        config.process_components()

    def test_dag_with_correct_ref_and_wrong_ref_type(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"name": "job-template"},
                    "name": "A",
                    "params": {
                        "input1": 2,
                        "input2": "gs://bucket/path/to/blob/",
                        "output1": 123,
                    },
                },
                {
                    "component_ref": {"name": "job-template"},
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {
                        "input1": 3,
                        "input2": "{{ ops.A.outputs.output1 }}",
                        "output1": 123,
                    },
                },
            ],
            "components": [
                {
                    "name": "job-template",
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.INT,
                        },
                        {
                            "name": "input2",
                            "description": "some text",
                            "type": types.GCS,
                        },
                        {
                            "name": "input3",
                            "description": "some text",
                            "type": types.BOOL,
                            "is_optional": True,
                            "value": True,
                        },
                    ],
                    "outputs": [
                        {
                            "name": "output1",
                            "description": "some text",
                            "type": types.INT,
                        }
                    ],
                    "run": {"kind": "container", "image": "test"},
                }
            ],
        }
        config = DagConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_dag_with_template_not_defining_inputs_and_ops_refs_params(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {"component_ref": {"name": "build-template"}, "name": "A"},
                {
                    "component_ref": {"name": "job-template"},
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {"param1": "{{ ops.A.outputs.x }}"},
                },
            ],
            "components": [
                {"name": "job-template", "run": {"kind": "container", "image": "test"}},
                {
                    "name": "build-template",
                    "tags": ["kaniko"],
                    "run": {"kind": "container", "image": "test"},
                },
            ],
        }
        config = DagConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_dag_with_ops_and_components(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"name": "build-template"},
                    "name": "A",
                    "description": "description A",
                    "tags": ["tag11", "tag12"],
                    "environment": {
                        "resources": {"requests": {"cpu": 1}},
                        "node_selector": {"polyaxon": "core"},
                        "service_account": "service",
                        "image_pull_secrets": ["secret1", "secret2"],
                    },
                    "termination": {"max_retries": 2},
                },
                {
                    "component_ref": {"name": "experiment-template"},
                    "name": "B",
                    "description": "description B",
                    "tags": ["tag21", "tag22"],
                    "dependencies": ["A"],
                    "params": {
                        "input1": 11.1,
                        "input2": False,
                        "input3": "{{ runs.64332180bfce46eba80a65caf73c5396.outputs.foo }}",
                        "output1": "S3://foo.com",
                    },
                    "environment": {
                        "resources": {"requests": {"cpu": 1}},
                        "node_selector": {"polyaxon": "core"},
                        "service_account": "service",
                        "image_pull_secrets": ["secret1", "secret2"],
                    },
                    "termination": {"max_retries": 3},
                },
                {
                    "component_ref": {"name": "group-template"},
                    "name": "C",
                    "description": "description C",
                    "tags": ["tag31", "tag32"],
                    "params": {
                        "input1": "{{ ops.B.outputs.output1 }}",
                        "input2": "{{ ops.B.outputs.output2 }}",
                        "output1": "S3://foo.com",
                    },
                    "environment": {
                        "resources": {"requests": {"cpu": 1}},
                        "node_selector": {"polyaxon": "core"},
                        "service_account": "service",
                        "image_pull_secrets": ["secret1", "secret2"],
                    },
                    "termination": {"max_retries": 5},
                },
            ],
            "components": [
                {
                    "name": "experiment-template",
                    "description": "description experiment",
                    "tags": ["tag11", "tag12"],
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.FLOAT,
                        },
                        {
                            "name": "input2",
                            "description": "some text",
                            "type": types.BOOL,
                            "is_optional": True,
                            "value": True,
                        },
                        {
                            "name": "input3",
                            "description": "some text",
                            "type": types.INT,
                            "is_optional": True,
                            "value": True,
                        },
                    ],
                    "outputs": [
                        {
                            "name": "output1",
                            "description": "some text",
                            "type": types.S3,
                        },
                        {
                            "name": "output2",
                            "description": "some text",
                            "type": types.BOOL,
                            "is_optional": True,
                            "value": True,
                        },
                    ],
                    "environment": {
                        "resources": {"requests": {"cpu": 1}},
                        "node_selector": {"polyaxon": "core"},
                        "service_account": "service",
                        "image_pull_secrets": ["secret1", "secret2"],
                    },
                    "termination": {"max_retries": 2},
                    "run": {"kind": "container", "image": "test"},
                },
                {
                    "name": "group-template",
                    "description": "description group",
                    "tags": ["tag11", "tag12"],
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.S3,
                        },
                        {
                            "name": "input2",
                            "description": "some text",
                            "type": types.BOOL,
                            "is_optional": True,
                            "value": True,
                        },
                    ],
                    "outputs": [
                        {
                            "name": "output1",
                            "description": "some text",
                            "type": types.S3,
                        }
                    ],
                    "environment": {
                        "resources": {"requests": {"cpu": 1}},
                        "node_selector": {"polyaxon": "core"},
                        "service_account": "service",
                        "image_pull_secrets": ["secret1", "secret2"],
                    },
                    "termination": {"max_retries": 2},
                    "run": {"kind": "container", "image": "test"},
                },
                {
                    "name": "build-template",
                    "description": "description build",
                    "tags": ["tag11", "tag12"],
                    "run": {"kind": "container", "image": "test"},
                },
                {
                    "name": "build-template2",
                    "description": "description build",
                    "tags": ["tag11", "tag12", "kaniko"],
                    "environment": {
                        "resources": {"requests": {"cpu": 1}},
                        "node_selector": {"polyaxon": "core"},
                        "service_account": "service",
                        "image_pull_secrets": ["secret1", "secret2"],
                    },
                    "termination": {"max_retries": 2},
                    "run": {"kind": "container", "image": "test"},
                },
                {
                    "name": "job-template",
                    "description": "description job",
                    "tags": ["tag11", "tag12"],
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.S3,
                            "is_optional": True,
                            "value": "s3://foo",
                        }
                    ],
                    "outputs": [
                        {
                            "name": "output1",
                            "description": "some text",
                            "type": types.S3,
                        }
                    ],
                    "environment": {
                        "resources": {"requests": {"cpu": 1}},
                        "node_selector": {"polyaxon": "core"},
                        "service_account": "service",
                        "image_pull_secrets": ["secret1", "secret2"],
                    },
                    "termination": {"max_retries": 2},
                    "run": {"kind": "container", "image": "test"},
                },
            ],
        }

        config = DagConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        config.process_dag()
        config.validate_dag()
        config.process_components()
        dag = config.dag
        assert len(dag) == 3
        assert config.get_independent_ops(dag=dag) == {"A"}
        assert dags.get_independent_ops(dag=dag) == {"A"}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert dags.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert config.sort_topologically(dag=dag) == sorted_dag
        assert sorted_dag[0] == ["A"]
        assert sorted_dag[1] == ["B"]
        assert sorted_dag[2] == ["C"]

        # op upstreams
        op_upstream_by_names = ops_params.get_upstream_op_params_by_names(
            params=config.dag["A"].op.params
        )
        assert op_upstream_by_names == {}
        op_upstream_by_names = ops_params.get_upstream_op_params_by_names(
            params=config.dag["B"].op.params
        )
        assert op_upstream_by_names == {}
        op_upstream_by_names = ops_params.get_upstream_op_params_by_names(
            params=config.dag["C"].op.params
        )
        assert len(op_upstream_by_names["B"]) == 2
        if op_upstream_by_names["B"][0].name == "input1":
            assert op_upstream_by_names["B"][0] == ops_params.ParamSpec(
                name="input1",
                iotype=None,
                value="ops.B.outputs.output1",
                entity="ops",
                entity_ref="B",
                entity_value="output1",
                is_flag=None,
            )
            assert op_upstream_by_names["B"][1] == ops_params.ParamSpec(
                name="input2",
                iotype=None,
                value="ops.B.outputs.output2",
                entity="ops",
                entity_ref="B",
                entity_value="output2",
                is_flag=None,
            )

        else:
            assert op_upstream_by_names["B"][1] == ops_params.ParamSpec(
                name="input1",
                iotype=None,
                value="ops.B.outputs.output1",
                entity="ops",
                entity_ref="B",
                entity_value="output1",
                is_flag=None,
            )
            assert op_upstream_by_names["B"][0] == ops_params.ParamSpec(
                name="input2",
                iotype=None,
                value="ops.B.outputs.output2",
                entity="ops",
                entity_ref="B",
                entity_value="output2",
                is_flag=None,
            )

        # run upstreams
        run_upstream_by_names = ops_params.get_upstream_run_params_by_names(
            params=config.dag["A"].op.params
        )
        assert run_upstream_by_names == {}
        run_upstream_by_names = ops_params.get_upstream_run_params_by_names(
            params=config.dag["B"].op.params
        )
        assert run_upstream_by_names["64332180bfce46eba80a65caf73c5396"] == [
            ops_params.ParamSpec(
                name="input3",
                iotype=None,
                value="runs.64332180bfce46eba80a65caf73c5396.outputs.foo",
                entity="runs",
                entity_ref="64332180bfce46eba80a65caf73c5396",
                entity_value="foo",
                is_flag=None,
            )
        ]
        run_upstream_by_names = ops_params.get_upstream_run_params_by_names(
            params=config.dag["C"].op.params
        )
        assert run_upstream_by_names == {}

        # pipeline upstreams
        pipeline_by_names = ops_params.get_dag_params_by_names(
            params=config.dag["A"].op.params
        )
        assert pipeline_by_names == {}
        pipeline_by_names = ops_params.get_dag_params_by_names(
            params=config.dag["B"].op.params
        )
        assert pipeline_by_names == {}
        pipeline_by_names = ops_params.get_dag_params_by_names(
            params=config.dag["C"].op.params
        )
        assert pipeline_by_names == {}

    def test_pipeline_context(self):
        config_dict = {
            "kind": "dag",
            "ops": [
                {
                    "component_ref": {"name": "A"},
                    "name": "A",
                    "params": {
                        "input1": 11.1,
                        "input2": False,
                        "input3": "{{ runs.64332180bfce46eba80a65caf73c5396.outputs.foo }}",
                        "input4": "s3://foo",
                    },
                },
                {
                    "component_ref": {"name": "B"},
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {
                        "input1": "{{ ops.A.inputs.input4 }}",
                        "input2": "{{ ops.A.outputs.output1 }}",
                    },
                },
                {
                    "component_ref": {"name": "B"},
                    "name": "C",
                    "params": {
                        "input1": "{{ dag.inputs.input_pipe }}",
                        "input2": "{{ ops.B.outputs.output1 }}",
                    },
                },
            ],
            "components": [
                {
                    "name": "A",
                    "inputs": [
                        {"name": "input1", "type": types.FLOAT},
                        {
                            "name": "input2",
                            "type": types.BOOL,
                            "is_optional": True,
                            "value": True,
                        },
                        {
                            "name": "input3",
                            "type": types.INT,
                            "is_optional": True,
                            "value": True,
                        },
                        {"name": "input4", "type": types.S3},
                    ],
                    "outputs": [
                        {"name": "output1", "type": types.S3},
                        {
                            "name": "output2",
                            "type": types.BOOL,
                            "is_optional": True,
                            "value": True,
                        },
                    ],
                    "run": {"kind": "container", "image": "test"},
                },
                {
                    "name": "B",
                    "inputs": [
                        {"name": "input1", "type": types.S3},
                        {"name": "input2", "type": types.S3},
                    ],
                    "outputs": [{"name": "output1", "type": types.S3}],
                    "run": {"kind": "container", "image": "test"},
                },
            ],
        }

        config = DagConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        config.process_dag()
        config.validate_dag()
        config.process_components(
            inputs=[IOConfig.from_dict({"name": "input_pipe", "type": types.S3})]
        )
        dag = config.dag
        assert len(dag) == 3
        assert config.get_independent_ops(dag=dag) == {"A"}
        assert dags.get_independent_ops(dag=dag) == {"A"}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert dags.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert config.sort_topologically(dag=dag) == sorted_dag
        assert sorted_dag[0] == ["A"]
        assert sorted_dag[1] == ["B"]
        assert sorted_dag[2] == ["C"]

        # op upstreams
        op_upstream_by_names = ops_params.get_upstream_op_params_by_names(
            params=config.dag["A"].op.params
        )
        assert op_upstream_by_names == {}
        op_upstream_by_names = ops_params.get_upstream_op_params_by_names(
            params=config.dag["B"].op.params
        )

        if op_upstream_by_names["A"][0].name == "input1":
            assert op_upstream_by_names["A"][0] == ops_params.ParamSpec(
                name="input1",
                iotype=None,
                value="ops.A.inputs.input4",
                entity="ops",
                entity_ref="A",
                entity_value="input4",
                is_flag=None,
            )
            assert op_upstream_by_names["A"][1] == ops_params.ParamSpec(
                name="input2",
                iotype=None,
                value="ops.A.outputs.output1",
                entity="ops",
                entity_ref="A",
                entity_value="output1",
                is_flag=None,
            )

        else:
            assert op_upstream_by_names["A"][1] == ops_params.ParamSpec(
                name="input1",
                iotype=None,
                value="ops.A.inputs.input4",
                entity="ops",
                entity_ref="A",
                entity_value="input4",
                is_flag=None,
            )
            assert op_upstream_by_names["A"][0] == ops_params.ParamSpec(
                name="input2",
                iotype=None,
                value="ops.A.outputs.output1",
                entity="ops",
                entity_ref="A",
                entity_value="output1",
                is_flag=None,
            )
        op_upstream_by_names = ops_params.get_upstream_op_params_by_names(
            params=config.dag["C"].op.params
        )
        assert op_upstream_by_names == {
            "B": [
                ops_params.ParamSpec(
                    name="input2",
                    iotype=None,
                    value="ops.B.outputs.output1",
                    entity="ops",
                    entity_ref="B",
                    entity_value="output1",
                    is_flag=None,
                )
            ]
        }

        # run upstreams
        run_upstream_by_names = ops_params.get_upstream_run_params_by_names(
            params=config.dag["A"].op.params
        )
        assert run_upstream_by_names["64332180bfce46eba80a65caf73c5396"] == [
            ops_params.ParamSpec(
                name="input3",
                iotype=None,
                value="runs.64332180bfce46eba80a65caf73c5396.outputs.foo",
                entity="runs",
                entity_ref="64332180bfce46eba80a65caf73c5396",
                entity_value="foo",
                is_flag=None,
            )
        ]
        run_upstream_by_names = ops_params.get_upstream_run_params_by_names(
            params=config.dag["B"].op.params
        )
        assert run_upstream_by_names == {}
        run_upstream_by_names = ops_params.get_upstream_run_params_by_names(
            params=config.dag["C"].op.params
        )
        assert run_upstream_by_names == {}

        # pipeline upstreams
        pipeline_by_names = ops_params.get_dag_params_by_names(
            params=config.dag["A"].op.params
        )
        assert pipeline_by_names == {}
        pipeline_by_names = ops_params.get_dag_params_by_names(
            params=config.dag["B"].op.params
        )
        assert pipeline_by_names == {}
        pipeline_by_names = ops_params.get_dag_params_by_names(
            params=config.dag["C"].op.params
        )
        assert pipeline_by_names["_"] == [
            ops_params.ParamSpec(
                name="input1",
                iotype=None,
                value="dag.inputs.input_pipe",
                entity="dag",
                entity_ref="_",
                entity_value="input_pipe",
                is_flag=None,
            )
        ]
