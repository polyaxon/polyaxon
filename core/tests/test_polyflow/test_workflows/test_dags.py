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

import pytest

from marshmallow import ValidationError
from tests.utils import BaseTestCase

from polyaxon import types
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.polyflow import V1RunKind, dags
from polyaxon.polyflow.io import V1IO
from polyaxon.polyflow.operations import V1Operation
from polyaxon.polyflow.params import V1Param, ops_params
from polyaxon.polyflow.run import V1Dag


@pytest.mark.workflow_mark
class TestWorkflowV1Dags(BaseTestCase):
    def test_wrong_pipelines_ops(self):
        config_dict = {"operations": "foo"}
        with self.assertRaises(ValidationError):
            V1Dag.from_dict(config_dict)

        config_dict = {"operations": ["foo"]}
        with self.assertRaises(ValidationError):
            V1Dag.from_dict(config_dict)

    def test_dag_ops(self):
        config_dict = {
            "kind": "dag",
            "operations": [
                {
                    "name": "A",
                    "hubRef": "action1",
                    "description": "description A",
                    "tags": ["tag11", "tag12"],
                    "params": {
                        "param1": {"value": "text"},
                        "param2": {"value": 12},
                        "param3": {"value": "https://foo.com"},
                    },
                    "termination": {"maxRetries": 2},
                    "runPatch": {
                        "kind": V1RunKind.JOB,
                        "container": {"resources": {"requests": {"cpu": 1}}},
                        "environment": {
                            "nodeSelector": {"polyaxon": "core"},
                            "serviceAccountName": "service",
                            "imagePullSecrets": ["secret1", "secret2"],
                        },
                    },
                },
                {
                    "urlRef": "https://url-to-temaplte.com",
                    "name": "B",
                    "description": "description B",
                    "tags": ["tag11", "tag12"],
                    "params": {
                        "param1": {"ref": "ops.A", "value": "outputs.x"},
                        "param2": {"value": 12},
                        "param3": {"value": "https://foo.com"},
                    },
                    "termination": {"maxRetries": 2},
                    "runPatch": {
                        "kind": V1RunKind.JOB,
                        "container": {"resources": {"requests": {"cpu": 1}}},
                        "environment": {
                            "nodeSelector": {"polyaxon": "core"},
                            "serviceAccountName": "service",
                            "imagePullSecrets": ["secret1", "secret2"],
                        },
                    },
                },
                {
                    "dagRef": "my-template",
                    "name": "C",
                    "description": "description C",
                    "tags": ["tag31", "tag32"],
                    "params": {"param2": {"value": 12.34}, "param3": {"value": False}},
                    "termination": {"maxRetries": 5},
                    "runPatch": {
                        "kind": V1RunKind.JOB,
                        "container": {"resources": {"requests": {"cpu": 1}}},
                        "environment": {
                            "nodeSelector": {"polyaxon": "core"},
                            "serviceAccountName": "service",
                            "imagePullSecrets": ["secret1", "secret2"],
                            "restartPolicy": "Never",
                        },
                    },
                },
                {
                    "pathRef": "./relative/path/to/my-template.yaml",
                    "name": "D",
                    "description": "description D",
                    "tags": ["tag31", "tag32"],
                    "dependencies": ["B", "C"],
                    "termination": {"maxRetries": 3},
                    "runPatch": {
                        "kind": V1RunKind.JOB,
                        "container": {"resources": {"requests": {"cpu": 1}}},
                        "environment": {
                            "nodeSelector": {"polyaxon": "core"},
                            "serviceAccountName": "service",
                            "imagePullSecrets": ["secret1", "secret2"],
                            "restartPolicy": "Never",
                        },
                    },
                },
            ],
        }
        config = V1Dag.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        config.process_dag()
        config.validate_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()

    def test_pipelines_components(self):
        config_dict = {
            "kind": V1RunKind.DAG,
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
                            "isOptional": True,
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
                    "termination": {"maxRetries": 2},
                    "run": {
                        "kind": V1RunKind.JOB,
                        "environment": {
                            "nodeSelector": {"polyaxon": "core"},
                            "serviceAccountName": "service",
                            "imagePullSecrets": ["secret1", "secret2"],
                            "restartPolicy": "Never",
                        },
                        "container": {
                            "resources": {"requests": {"cpu": "500m"}},
                            "image": "test",
                        },
                    },
                }
            ],
        }

        config = V1Dag.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        config.process_dag()
        config.validate_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()

    def test_dag_job_component_with_correct_params(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "name": "experiment-template",
                    "params": {"input1": {"value": 1.1}, "input2": {"value": False}},
                    "termination": {"maxRetries": 2},
                    "runPatch": {
                        "kind": V1RunKind.JOB,
                        "container": {"resources": {"requests": {"cpu": "500m"}}},
                        "environment": {
                            "nodeSelector": {"polyaxon": "core"},
                            "serviceAccountName": "service",
                            "imagePullSecrets": ["secret1", "secret2"],
                            "restartPolicy": "Never",
                        },
                    },
                    "component": {
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
                                "isOptional": True,
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
                        "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                    },
                }
            ],
        }
        config = V1Dag.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        config.process_dag()
        config.validate_dag()
        config.process_components(
            inputs=[V1IO.from_dict({"name": "input_pipe", "type": types.S3})]
        )

    def test_dag_structure(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "hubRef": "action1",
                    "name": "A",
                    "params": {
                        "param1": {"value": "text"},
                        "param2": {"value": 12},
                        "param3": {"value": "https://foo.com"},
                    },
                },
                {
                    "urlRef": "https://url-to-temaplte.com",
                    "name": "B",
                    "params": {
                        "param1": {"value": "outputs.x", "ref": "ops.A"},
                        "param2": {"value": 12},
                        "param3": {"value": "https://foo.com"},
                    },
                },
                {
                    "dagRef": "my-template",
                    "name": "C",
                    "params": {"param2": {"value": 12.34}, "param3": {"value": False}},
                },
                {
                    "pathRef": "./relative/path/to/my-template.yaml",
                    "name": "D",
                    "dependencies": ["B", "C"],
                },
            ],
        }
        config = V1Dag.from_dict(config_dict)
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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action1",
        }
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "url_ref",
            "url": "https://url-to-temaplte.com",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "my-template",
        }
        assert config.dag["C"].upstream == set()
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.definition.to_dict() == {
            "kind": "path_ref",
            "path": "./relative/path/to/my-template.yaml",
        }
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

    def test_dag_matrix_ops(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {"hubRef": "action1", "name": "A"},
                {"hubRef": "event1", "name": "B"},
                {"dagRef": "foo", "name": "C"},
                {"dagRef": "bar", "name": "D"},
            ],
        }

        config = V1Dag.from_dict(config_dict)
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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action1",
        }
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == set()

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event1",
        }
        assert config.dag["B"].upstream == set()
        assert config.dag["B"].downstream == set()

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "foo",
        }
        assert config.dag["C"].upstream == set()
        assert config.dag["C"].downstream == set()

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "bar",
        }
        assert config.dag["D"].upstream == set()
        assert config.dag["D"].downstream == set()

    def test_dag_sequential_ops(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {"hubRef": "action1", "name": "A"},
                {"hubRef": "event1", "name": "B", "dependencies": ["A"]},
                {"dagRef": "foo", "name": "C", "dependencies": ["B"]},
                {"dagRef": "bar", "name": "D", "dependencies": ["C"]},
            ],
        }

        config = V1Dag.from_dict(config_dict)
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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action1",
        }
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event1",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"C"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "foo",
        }
        assert config.dag["C"].upstream == {"B"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "bar",
        }
        assert config.dag["D"].upstream == {"C"}
        assert config.dag["D"].downstream == set()

    def test_dag_all_downstream(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "hubRef": "action1",
                    "name": "A",
                    "params": {
                        "param1": {"value": "text"},
                        "param2": {"value": 12},
                        "param3": {"value": "https://foo.com"},
                    },
                    "dependencies": ["B", "C", "D"],
                },
                {"hubRef": "event1", "name": "B"},
                {"hubRef": "event2", "name": "C"},
                {"hubRef": "event3", "name": "D"},
            ],
        }

        config = V1Dag.from_dict(config_dict)
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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action1",
        }
        assert config.dag["A"].upstream == {"B", "C", "D"}
        assert config.dag["A"].downstream == set()

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event1",
        }
        assert config.dag["B"].upstream == set()
        assert config.dag["B"].downstream == {"A"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event2",
        }
        assert config.dag["C"].upstream == set()
        assert config.dag["C"].downstream == {"A"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event3",
        }
        assert config.dag["D"].upstream == set()
        assert config.dag["D"].downstream == {"A"}

    def test_dag_acyclic_deps(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {"hubRef": "action1", "name": "A", "dependencies": ["B"]},
                {"hubRef": "event1", "name": "B", "dependencies": ["A"]},
                {"dagRef": "foo", "name": "C", "dependencies": ["A"]},
            ],
        }

        config = V1Dag.from_dict(config_dict)
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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action1",
        }
        assert config.dag["A"].upstream == {"B"}
        assert config.dag["A"].downstream == {"B", "C"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event1",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"A"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "foo",
        }
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == set()

    def test_dag_circular_deps(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {"hubRef": "action1", "name": "A", "dependencies": ["C"]},
                {"hubRef": "event1", "name": "B", "dependencies": ["A"]},
                {"dagRef": "foo", "name": "C", "dependencies": ["B"]},
            ],
        }

        config = V1Dag.from_dict(config_dict)
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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action1",
        }
        assert config.dag["A"].upstream == {"C"}
        assert config.dag["A"].downstream == {"B"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event1",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"C"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "foo",
        }
        assert config.dag["C"].upstream == {"B"}
        assert config.dag["C"].downstream == {"A"}

    def test_dag_adding_ops_one_by_one_manually(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {"hubRef": "action1", "name": "A"},
                {"hubRef": "event1", "name": "B", "dependencies": ["A"]},
                {"dagRef": "foo", "name": "C", "dependencies": ["A"]},
            ],
        }

        config = V1Dag.from_dict(config_dict)
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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action1",
        }
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event1",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == set()

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "foo",
        }
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == set()

        operation_d = V1Operation(hub_ref="action4", name="D", dependencies=["B", "C"])
        config.add_op(operation_d)

        operation_e = V1Operation(hub_ref="action4", name="E", dependencies=["A"])
        config.add_op(operation_e)

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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action1",
        }
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C", "E"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event1",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "foo",
        }
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action4",
        }
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

        assert config.dag["E"].op.name == "E"
        assert config.dag["E"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action4",
        }
        assert config.dag["E"].upstream == {"A"}
        assert config.dag["E"].downstream == set()

        # Adding the same ops should not alter the behavior
        config.add_ops([operation_d, operation_e])

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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action1",
        }
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C", "E"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event1",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "foo",
        }
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action4",
        }
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

        assert config.dag["E"].op.name == "E"
        assert config.dag["E"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action4",
        }
        assert config.dag["E"].upstream == {"A"}
        assert config.dag["E"].downstream == set()

    def test_dag_adding_ops_many_manually(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {"hubRef": "action1", "name": "A"},
                {"hubRef": "event1", "name": "B", "dependencies": ["A"]},
                {"dagRef": "foo", "name": "C", "dependencies": ["A"]},
            ],
        }

        config = V1Dag.from_dict(config_dict)
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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action1",
        }
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event1",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == set()

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "foo",
        }
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == set()

        operation_d = V1Operation(hub_ref="action4", name="D", dependencies=["B", "C"])
        operation_e = V1Operation(hub_ref="action4", name="E", dependencies=["A"])
        config.add_ops([operation_d, operation_e])

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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action1",
        }
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C", "E"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event1",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "foo",
        }
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action4",
        }
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

        assert config.dag["E"].op.name == "E"
        assert config.dag["E"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action4",
        }
        assert config.dag["E"].upstream == {"A"}
        assert config.dag["E"].downstream == set()

        # Adding the same ops should not alter the behavior
        config.add_op(operation_d)
        config.add_op(operation_e)

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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action1",
        }
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C", "E"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event1",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "foo",
        }
        assert config.dag["C"].upstream == {"A"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action4",
        }
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

        assert config.dag["E"].op.name == "E"
        assert config.dag["E"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action4",
        }
        assert config.dag["E"].upstream == {"A"}
        assert config.dag["E"].downstream == set()

    def test_dag_dependency_from_params(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "hubRef": "echo",
                    "name": "A",
                    "params": {
                        "param1": {"value": "text"},
                        "param2": {"value": 12},
                        "param3": {"value": "https://foo.com"},
                    },
                },
                {
                    "hubRef": "echo",
                    "name": "B",
                    "params": {
                        "param1": {"ref": "ops.A", "value": "outputs.x"},
                        "param2": {"value": 12},
                        "param3": {"value": "https://foo.com"},
                    },
                },
                {
                    "hubRef": "echo",
                    "name": "C",
                    "params": {
                        "param1": {"ref": "ops.A", "value": "outputs.x"},
                        "param2": {"ref": "ops.B", "value": "outputs.x"},
                    },
                },
                {"hubRef": "echo", "name": "D", "dependencies": ["B", "C"]},
            ],
        }

        config = V1Dag.from_dict(config_dict)
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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "echo",
        }
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "echo",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"C", "D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "echo",
        }
        assert config.dag["C"].upstream == {"A", "B"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "echo",
        }
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

    def test_dag_dependency_from_metainfo(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "hubRef": "echo",
                    "name": "A",
                    "params": {
                        "param1": {"value": "text"},
                        "param2": {"value": 12},
                        "param3": {"value": "https://foo.com"},
                    },
                },
                {
                    "hubRef": "echo",
                    "name": "B",
                    "params": {
                        "param1": {"value": "status", "ref": "ops.A"},
                        "param2": {"value": "project_name", "ref": "ops.A"},
                        "param3": {"value": "https://foo.com"},
                    },
                },
                {
                    "hubRef": "echo",
                    "name": "C",
                    "params": {
                        "param1": {"value": "inputs", "ref": "ops.A"},
                        "param2": {"value": "uuid", "ref": "ops.B"},
                        "param3": {"value": "outputs", "ref": "ops.B"},
                    },
                },
                {"hubRef": "echo", "name": "D", "dependencies": ["B", "C"]},
            ],
        }

        config = V1Dag.from_dict(config_dict)
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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "echo",
        }
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "echo",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"C", "D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "echo",
        }
        assert config.dag["C"].upstream == {"A", "B"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "echo",
        }
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

    def test_dag_dependency_and_params(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "hubRef": "echo",
                    "name": "A",
                    "params": {
                        "param1": {"value": "text"},
                        "param2": {"value": 12},
                        "param3": {"value": "https://foo.com"},
                    },
                },
                {
                    "hubRef": "echo",
                    "name": "B",
                    "params": {
                        "param1": {"value": "outputs.x", "ref": "ops.A"},
                        "param2": {"value": 12},
                        "param3": {"value": "https://foo.com"},
                    },
                    "dependencies": ["A"],
                },
                {
                    "hubRef": "echo",
                    "name": "C",
                    "params": {"param2": {"value": "outputs.x", "ref": "ops.B"}},
                    "dependencies": ["A"],
                },
                {"hubRef": "echo", "name": "D", "dependencies": ["B", "C"]},
            ],
        }

        config = V1Dag.from_dict(config_dict)
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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "echo",
        }
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "echo",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == {"C", "D"}

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "echo",
        }
        assert config.dag["C"].upstream == {"A", "B"}
        assert config.dag["C"].downstream == {"D"}

        assert config.dag["D"].op.name == "D"
        assert config.dag["D"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "echo",
        }
        assert config.dag["D"].upstream == {"B", "C"}
        assert config.dag["D"].downstream == set()

    def test_dag_orphan_ops(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {"hubRef": "action1", "name": "A"},
                {"hubRef": "event1", "name": "B", "dependencies": ["A"]},
                {"dagRef": "foo", "name": "C", "dependencies": ["A", "E"]},
            ],
        }

        config = V1Dag.from_dict(config_dict)
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
        assert config.dag["A"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "action1",
        }
        assert config.dag["A"].upstream == set()
        assert config.dag["A"].downstream == {"B", "C"}

        assert config.dag["B"].op.name == "B"
        assert config.dag["B"].op.definition.to_dict() == {
            "kind": "hub_ref",
            "name": "event1",
        }
        assert config.dag["B"].upstream == {"A"}
        assert config.dag["B"].downstream == set()

        assert config.dag["C"].op.name == "C"
        assert config.dag["C"].op.definition.to_dict() == {
            "kind": "dag_ref",
            "name": "foo",
        }
        assert config.dag["C"].upstream == {"A", "E"}
        assert config.dag["C"].downstream == set()

    def test_dag_with_duplicate_job_names(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {"dagRef": "build-template1", "name": "A"},
                {"dagRef": "build-template1", "name": "A"},
            ],
            "components": [
                {
                    "kind": "component",
                    "name": "build-template",
                    "description": "description build",
                    "tags": ["tag11", "tag12"],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                },
                {
                    "kind": "component",
                    "name": "job-template",
                    "description": "description build",
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                },
            ],
        }
        config = V1Dag.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()

    def test_dag_with_op_requesting_undefined_template(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {"dagRef": "build-template1", "name": "A"},
                {
                    "dagRef": "build-template1",
                    "runPatch": {
                        "kind": V1RunKind.JOB,
                        "connections": ["data2", "data2"],
                    },
                    "name": "B",
                },
            ],
            "components": [
                {
                    "kind": "component",
                    "name": "build-template2",
                    "description": "description build",
                    "tags": ["kaniko"],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                }
            ],
        }
        config = V1Dag.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        with self.assertRaises(PolyaxonSchemaError):
            config.process_components()

    def test_dag_with_template_not_defining_inputs(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "dagRef": "build-template",
                    "name": "A",
                    "runPatch": {
                        "kind": V1RunKind.JOB,
                        "connections": ["foo", "boo"],
                        "container": {"args": ["--branch=dev"]},
                    },
                },
                {"dagRef": "job-template", "name": "B", "dependencies": ["A"]},
            ],
            "components": [
                {
                    "kind": "component",
                    "name": "job-template",
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                },
                {
                    "kind": "component",
                    "name": "build-template",
                    "tags": ["kaniko"],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                },
            ],
        }
        config = V1Dag.from_dict(config_dict)
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
        assert config.dag["A"].op.has_component_reference is False
        assert config.dag["B"].op.has_component_reference is False
        config.set_op_component("A")
        assert config.dag["B"].op.has_component_reference is False
        assert config.dag["A"].op.has_component_reference is True
        assert (
            config.dag["A"].op.definition
            == config._components_by_names["build-template"]
        )
        config.set_op_component("B")
        assert config.dag["B"].op.has_component_reference is True
        assert (
            config.dag["B"].op.definition == config._components_by_names["job-template"]
        )

    def test_dag_with_template_not_defining_inputs_and_ops_with_params(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "name": "A",
                    "component": {
                        "name": "build-template",
                        "tags": ["kaniko"],
                        "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                    },
                },
                {
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {
                        "param1": {"value": "outputs.x", "ref": "ops.A"},
                        "param2": {"value": 12},
                        "param3": {"value": "https://foo.com"},
                    },
                    "component": {
                        "name": "job-template",
                        "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                    },
                },
            ],
        }
        config = V1Dag.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_pipelines_with_template_not_defining_inputs_and_ops_with_params_template(
        self,
    ):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {"dagRef": "build-template", "name": "A"},
                {
                    "dagRef": "job-template",
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {
                        "param1": {"value": "outputs.x", "ref": "ops.A"},
                        "param2": {"value": 12},
                        "param3": {"value": "https://foo.com"},
                    },
                },
            ],
            "components": [
                {
                    "kind": "component",
                    "name": "job-template",
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                },
                {
                    "kind": "component",
                    "name": "build-template",
                    "tags": ["kaniko"],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                },
            ],
        }
        config = V1Dag.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_dag_with_ops_template_required_inputs(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "name": "A",
                    "component": {
                        "name": "job-template",
                        "inputs": [
                            {
                                "name": "input1",
                                "description": "some text",
                                "type": types.FLOAT,
                            }
                        ],
                        "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                    },
                }
            ],
        }
        config = V1Dag.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_pipelines_with_ops_template_required_inputs_template(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [{"dagRef": "job-template", "name": "A"}],
            "components": [
                {
                    "kind": "component",
                    "name": "job-template",
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.FLOAT,
                        }
                    ],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                }
            ],
        }
        config = V1Dag.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_dag_with_ops_template_optional_inputs(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "name": "A",
                    "component": {
                        "name": "job-template",
                        "inputs": [
                            {
                                "name": "input1",
                                "description": "some text",
                                "type": types.FLOAT,
                                "isOptional": True,
                                "value": 12.2,
                            }
                        ],
                        "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                    },
                }
            ],
        }
        config = V1Dag.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        config.process_components()

    def test_pipelines_with_ops_template_optional_inputs_template(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [{"dagRef": "job-template", "name": "A"}],
            "components": [
                {
                    "kind": "component",
                    "name": "job-template",
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.FLOAT,
                            "isOptional": True,
                            "value": 12.2,
                        }
                    ],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                }
            ],
        }
        config = V1Dag.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        config.process_components()

    def test_dag_with_ops_template_optional_inputs_and_wrong_param(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "name": "A",
                    "params": {"input1": {"value": "foo"}},
                    "component": {
                        "name": "job-template",
                        "inputs": [
                            {
                                "name": "input1",
                                "description": "some text",
                                "type": types.FLOAT,
                                "isOptional": True,
                                "value": 12.2,
                            }
                        ],
                        "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                    },
                }
            ],
        }
        config = V1Dag.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_pipelines_with_ops_template_optional_inputs_and_wrong_param_components(
        self,
    ):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "dagRef": "job-template",
                    "name": "A",
                    "params": {"input1": {"value": "foo"}},
                }
            ],
            "components": [
                {
                    "kind": "component",
                    "name": "job-template",
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.FLOAT,
                            "isOptional": True,
                            "value": 12.2,
                        }
                    ],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                }
            ],
        }
        config = V1Dag.from_dict(config_dict)
        config_to_light = config.to_light_dict()
        assert config_to_light == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_dag_with_ops_template_validation(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "dagRef": "job-template",
                    "name": "A",
                    "params": {
                        "input1": {"value": "sdf"},
                        "input2": {"value": 12.0},
                        "input3": {"value": False},
                    },
                },
                {
                    "dagRef": "job-template",
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {
                        "input1": {"value": "ooo"},
                        "input2": {"value": 12.123},
                    },
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
                            "isOptional": True,
                            "value": True,
                        },
                    ],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                }
            ],
        }
        config = V1Dag.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        # Trying to set op template before processing components
        with self.assertRaises(PolyaxonSchemaError):
            config.set_op_component("A")
        config.process_components()
        # Trying to set op template before processing dag
        with self.assertRaises(PolyaxonSchemaError):
            config.set_op_component("A")
        config.process_dag()
        assert config.dag["A"].op.has_component_reference is False
        assert config.dag["B"].op.has_component_reference is False
        config.set_op_component("A")
        assert config.dag["B"].op.has_component_reference is False
        assert config.dag["A"].op.has_component_reference is True
        assert (
            config.dag["A"].op.definition == config._components_by_names["job-template"]
        )
        config.set_op_component("B")
        assert config.dag["B"].op.has_component_reference is True
        assert (
            config.dag["B"].op.definition == config._components_by_names["job-template"]
        )

    def test_dag_with_wrong_refs(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "dagRef": "job-template",
                    "name": "A",
                    "params": {
                        "input1": {"value": "sdf"},
                        "input2": {"value": 12.0},
                        "input3": {"value": False},
                    },
                },
                {
                    "dagRef": "job-template",
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {
                        "input1": {"value": "outputs.output1", "ref": "ops.A"},
                        "input2": {"value": 12.123},
                    },
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
                            "isOptional": True,
                            "value": True,
                        },
                    ],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                }
            ],
        }
        config = V1Dag.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_dag_with_correct_refs(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "dagRef": "job-template",
                    "name": "A",
                    "params": {
                        "input1": {"value": 2},
                        "input2": {"value": "gs://bucket/path/to/blob/"},
                        "input4": {"value": "failed"},
                        "input5": {"value": {"foo": "bar"}},
                    },
                },
                {
                    "dagRef": "job-template",
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {
                        "input1": {"value": "outputs.output1", "ref": "ops.A"},
                        "input2": {"value": "gs://bucket/path/to/blob/"},
                        "input4": {"value": "status", "ref": "ops.A"},
                        "input5": {"value": "inputs", "ref": "ops.A"},
                    },
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
                            "isOptional": True,
                            "value": True,
                        },
                        {"name": "input4", "description": "status", "type": types.STR},
                        {"name": "input5", "description": "dict", "type": types.DICT},
                    ],
                    "outputs": [
                        {
                            "name": "output1",
                            "description": "some text",
                            "type": types.INT,
                            "isOptional": True,
                            "value": 123,
                        }
                    ],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                }
            ],
        }
        config = V1Dag.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        config.process_components()

    def test_dag_with_correct_ref_and_wrong_ref_type(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "dagRef": "job-template",
                    "name": "A",
                    "params": {
                        "input1": {"value": 2},
                        "input2": {"value": "gs://bucket/path/to/blob/"},
                        "output1": {"value": 123},
                    },
                },
                {
                    "dagRef": "job-template",
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {
                        "input1": {"value": 3},
                        "input2": {"value": "outputs.output1", "ref": "ops.A"},
                        "output1": {"value": 123},
                    },
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
                            "isOptional": True,
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
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                }
            ],
        }
        config = V1Dag.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_dag_with_template_not_defining_inputs_and_ops_refs_params(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {"dagRef": "build-template", "name": "A"},
                {
                    "dagRef": "job-template",
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {"param1": {"value": "outputs.x", "ref": "ops.A"}},
                },
            ],
            "components": [
                {
                    "kind": "component",
                    "name": "job-template",
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                },
                {
                    "kind": "component",
                    "name": "build-template",
                    "tags": ["kaniko"],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                },
            ],
        }
        config = V1Dag.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_components()

    def test_dag_with_ops_and_components(self):
        config_dict = {
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "dagRef": "build-template",
                    "name": "A",
                    "description": "description A",
                    "tags": ["tag11", "tag12"],
                    "termination": {"maxRetries": 2},
                    "runPatch": {
                        "kind": V1RunKind.JOB,
                        "container": {"resources": {"requests": {"cpu": 1}}},
                        "environment": {
                            "nodeSelector": {"polyaxon": "core"},
                            "serviceAccountName": "service",
                            "imagePullSecrets": ["secret1", "secret2"],
                        },
                    },
                },
                {
                    "dagRef": "experiment-template",
                    "name": "B",
                    "description": "description B",
                    "tags": ["tag21", "tag22"],
                    "dependencies": ["A"],
                    "params": {
                        "input1": {"value": 11.1},
                        "input2": {"value": False},
                        "input3": {
                            "value": "outputs.foo",
                            "ref": "runs.64332180bfce46eba80a65caf73c5396",
                        },
                        "output1": {"value": "S3://foo.com"},
                    },
                    "termination": {"maxRetries": 3},
                    "runPatch": {
                        "kind": V1RunKind.JOB,
                        "container": {"resources": {"requests": {"cpu": 1}}},
                        "environment": {
                            "nodeSelector": {"polyaxon": "core"},
                            "serviceAccountName": "service",
                            "imagePullSecrets": ["secret1", "secret2"],
                        },
                    },
                },
                {
                    "dagRef": "group-template",
                    "name": "C",
                    "description": "description C",
                    "tags": ["tag31", "tag32"],
                    "params": {
                        "input1": {"value": "outputs.output1", "ref": "ops.B"},
                        "input2": {"value": "outputs.output2", "ref": "ops.B"},
                        "output1": {"value": "S3://foo.com"},
                    },
                    "termination": {"maxRetries": 5},
                    "runPatch": {
                        "kind": V1RunKind.JOB,
                        "container": {"resources": {"requests": {"cpu": 1}}},
                        "environment": {
                            "nodeSelector": {"polyaxon": "core"},
                            "serviceAccountName": "service",
                            "imagePullSecrets": ["secret1", "secret2"],
                        },
                    },
                },
            ],
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
                            "isOptional": True,
                            "value": True,
                        },
                        {
                            "name": "input3",
                            "description": "some text",
                            "type": types.INT,
                            "isOptional": True,
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
                            "isOptional": True,
                            "value": True,
                        },
                    ],
                    "termination": {"maxRetries": 2},
                    "run": {
                        "kind": V1RunKind.JOB,
                        "environment": {
                            "nodeSelector": {"polyaxon": "core"},
                            "serviceAccountName": "service",
                            "imagePullSecrets": ["secret1", "secret2"],
                        },
                        "container": {
                            "image": "test",
                            "resources": {"requests": {"cpu": 1}},
                        },
                    },
                },
                {
                    "kind": "component",
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
                            "isOptional": True,
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
                    "termination": {"maxRetries": 2},
                    "run": {
                        "kind": V1RunKind.JOB,
                        "environment": {
                            "nodeSelector": {"polyaxon": "core"},
                            "serviceAccountName": "service",
                            "imagePullSecrets": ["secret1", "secret2"],
                        },
                        "container": {
                            "image": "test",
                            "resources": {"requests": {"cpu": 1}},
                        },
                    },
                },
                {
                    "kind": "component",
                    "name": "build-template",
                    "description": "description build",
                    "tags": ["tag11", "tag12"],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                },
                {
                    "kind": "component",
                    "name": "build-template2",
                    "description": "description build",
                    "tags": ["tag11", "tag12", "kaniko"],
                    "termination": {"maxRetries": 2},
                    "run": {
                        "kind": V1RunKind.JOB,
                        "environment": {
                            "nodeSelector": {"polyaxon": "core"},
                            "serviceAccountName": "service",
                            "imagePullSecrets": ["secret1", "secret2"],
                        },
                        "container": {
                            "image": "test",
                            "resources": {"requests": {"cpu": 1}},
                        },
                    },
                },
                {
                    "kind": "component",
                    "name": "job-template",
                    "description": "description job",
                    "tags": ["tag11", "tag12"],
                    "inputs": [
                        {
                            "name": "input1",
                            "description": "some text",
                            "type": types.S3,
                            "isOptional": True,
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
                    "termination": {"maxRetries": 2},
                    "run": {
                        "kind": V1RunKind.JOB,
                        "environment": {
                            "nodeSelector": {"polyaxon": "core"},
                            "serviceAccountName": "service",
                            "imagePullSecrets": ["secret1", "secret2"],
                        },
                        "container": {
                            "image": "test",
                            "resources": {"requests": {"cpu": 1}},
                        },
                    },
                },
            ],
        }

        config = V1Dag.from_dict(config_dict)
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
                param=V1Param(ref="ops.B", value="outputs.output1"),
                is_flag=None,
                is_list=None,
                is_context=None,
                arg_format=None,
            )
            assert op_upstream_by_names["B"][1] == ops_params.ParamSpec(
                name="input2",
                iotype=None,
                param=V1Param(ref="ops.B", value="outputs.output2"),
                is_flag=None,
                is_list=None,
                is_context=None,
                arg_format=None,
            )

        else:
            assert op_upstream_by_names["B"][1] == ops_params.ParamSpec(
                name="input1",
                iotype=None,
                param=V1Param(ref="ops.B", value="outputs.output1"),
                is_flag=None,
                is_list=None,
                is_context=None,
                arg_format=None,
            )
            assert op_upstream_by_names["B"][0] == ops_params.ParamSpec(
                name="input2",
                iotype=None,
                param=V1Param(ref="ops.B", value="outputs.output2"),
                is_flag=None,
                is_list=None,
                is_context=None,
                arg_format=None,
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
                param=V1Param(
                    ref="runs.64332180bfce46eba80a65caf73c5396", value="outputs.foo"
                ),
                is_flag=None,
                is_list=None,
                is_context=None,
                arg_format=None,
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
            "kind": V1RunKind.DAG,
            "operations": [
                {
                    "dagRef": "A",
                    "name": "A",
                    "params": {
                        "input1": {"value": 11.1},
                        "input2": {"value": False},
                        "input3": {
                            "value": "outputs.foo",
                            "ref": "runs.64332180bfce46eba80a65caf73c5396",
                        },
                        "input4": {"value": "s3://foo"},
                    },
                },
                {
                    "dagRef": "B",
                    "name": "B",
                    "dependencies": ["A"],
                    "params": {
                        "input1": {"value": "inputs.input4", "ref": "ops.A"},
                        "input2": {"value": "outputs.output1", "ref": "ops.A"},
                        "input3": {"value": "status", "ref": "ops.A"},
                        "input4": {"value": "inputs", "ref": "ops.A"},
                    },
                },
                {
                    "dagRef": "B",
                    "name": "C",
                    "params": {
                        "input1": {"ref": "dag", "value": "inputs.input_pipe"},
                        "input2": {"ref": "ops.B", "value": "outputs.output1"},
                        "input3": {"ref": "ops.A", "value": "status"},
                        "input4": {"ref": "ops.B", "value": "inputs"},
                    },
                },
            ],
            "components": [
                {
                    "kind": "component",
                    "name": "A",
                    "inputs": [
                        {"name": "input1", "type": types.FLOAT},
                        {
                            "name": "input2",
                            "type": types.BOOL,
                            "isOptional": True,
                            "value": True,
                        },
                        {
                            "name": "input3",
                            "type": types.INT,
                            "isOptional": True,
                            "value": True,
                        },
                        {"name": "input4", "type": types.S3},
                    ],
                    "outputs": [
                        {"name": "output1", "type": types.S3},
                        {
                            "name": "output2",
                            "type": types.BOOL,
                            "isOptional": True,
                            "value": True,
                        },
                    ],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                },
                {
                    "kind": "component",
                    "name": "B",
                    "inputs": [
                        {"name": "input1", "type": types.S3},
                        {"name": "input2", "type": types.S3},
                        {"name": "input3", "type": types.STR},
                        {"name": "input4", "type": types.DICT},
                    ],
                    "outputs": [{"name": "output1", "type": types.S3}],
                    "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
                },
            ],
        }

        config = V1Dag.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        config.process_dag()
        config.validate_dag()
        config.process_components(
            inputs=[V1IO.from_dict({"name": "input_pipe", "type": types.S3})]
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
                param=V1Param(ref="ops.A", value="inputs.input4"),
                is_flag=None,
                is_list=None,
                is_context=None,
                arg_format=None,
            )
            assert op_upstream_by_names["A"][1] == ops_params.ParamSpec(
                name="input2",
                iotype=None,
                param=V1Param(ref="ops.A", value="outputs.output1"),
                is_flag=None,
                is_list=None,
                is_context=None,
                arg_format=None,
            )

        else:
            assert op_upstream_by_names["A"][1] == ops_params.ParamSpec(
                name="input1",
                iotype=None,
                param=V1Param(ref="ops.A", value="inputs.input4"),
                is_flag=None,
                is_list=None,
                is_context=None,
                arg_format=None,
            )
            assert op_upstream_by_names["A"][0] == ops_params.ParamSpec(
                name="input2",
                iotype=None,
                param=V1Param(ref="ops.A", value="outputs.output1"),
                is_flag=None,
                is_list=None,
                is_context=None,
                arg_format=None,
            )
        op_upstream_by_names = ops_params.get_upstream_op_params_by_names(
            params=config.dag["C"].op.params
        )
        assert op_upstream_by_names == {
            "A": [
                ops_params.ParamSpec(
                    name="input3",
                    iotype=None,
                    param=V1Param(ref="ops.A", value="status"),
                    is_flag=None,
                    is_list=None,
                    is_context=None,
                    arg_format=None,
                )
            ],
            "B": [
                ops_params.ParamSpec(
                    name="input2",
                    iotype=None,
                    param=V1Param(ref="ops.B", value="outputs.output1"),
                    is_flag=None,
                    is_list=None,
                    is_context=None,
                    arg_format=None,
                ),
                ops_params.ParamSpec(
                    name="input4",
                    iotype=None,
                    param=V1Param(ref="ops.B", value="inputs"),
                    is_flag=None,
                    is_list=None,
                    is_context=None,
                    arg_format=None,
                ),
            ],
        }

        # run upstreams
        run_upstream_by_names = ops_params.get_upstream_run_params_by_names(
            params=config.dag["A"].op.params
        )
        assert run_upstream_by_names["64332180bfce46eba80a65caf73c5396"] == [
            ops_params.ParamSpec(
                name="input3",
                iotype=None,
                param=V1Param(
                    ref="runs.64332180bfce46eba80a65caf73c5396", value="outputs.foo"
                ),
                is_flag=None,
                is_list=None,
                is_context=None,
                arg_format=None,
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
                param=V1Param(ref="dag", value="inputs.input_pipe"),
                is_flag=None,
                is_list=None,
                is_context=None,
                arg_format=None,
            )
        ]
