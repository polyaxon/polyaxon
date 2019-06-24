# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from hestia.tz_utils import local_now
from marshmallow import ValidationError

from polyaxon_schemas.exceptions import PolyaxonSchemaError
from polyaxon_schemas.ops.io import IOTypes
from polyaxon_schemas.polyflow.ops import OpConfig
from polyaxon_schemas.polyflow.pipeline import PipelineConfig
from polyaxon_schemas.polyflow.template_ref import TemplateRefConfig


class TestPipelineConfigs(TestCase):
    def test_pipelines_base_attrs(self):
        config_dict = {'concurrency': 'foo'}
        with self.assertRaises(ValidationError):
            PipelineConfig.from_dict(config_dict)

        config_dict = {
            'concurrency': 2,
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        config.process_dag()
        config.validate_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()

        config_dict = {
            'concurrency': 2,
            'execute_at': local_now().isoformat(),
            'timeout': 1000
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        config.process_dag()
        config.validate_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()

    def test_wrong_pipelines_ops(self):
        config_dict = {'ops': 'foo'}
        with self.assertRaises(ValidationError):
            PipelineConfig.from_dict(config_dict)

        config_dict = {'ops': ['foo']}
        with self.assertRaises(ValidationError):
            PipelineConfig.from_dict(config_dict)

    def test_pipelines_ops(self):
        config_dict = {
            'ops': [
                {
                    'template': {'action': 'action1'},
                    'name': 'A',
                    'description': 'description A',
                    'tags': ['tag11', 'tag12'],
                    'params': {'param1': 'text', 'param2': 12, 'param3': 'https://foo.com'},
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                    },
                    'max_retries': 2
                },
                {
                    'template': {'url': 'https://url-to-temaplte.com'},
                    'name': 'B',
                    'description': 'description B',
                    'tags': ['tag21', 'tag22'],
                    'params': {
                        'param1': '{{ ops.A.outputs.x }}',
                        'param2': 12,
                        'param3': 'https://foo.com'
                    },
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                    },
                    'max_retries': 2
                },
                {
                    'template': {'name': 'my-template'},
                    'name': 'C',
                    'description': 'description C',
                    'tags': ['tag31', 'tag32'],
                    'params': {
                        'param2': 12.34,
                        'param3': False
                    },
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                    },
                    'max_retries': 5,
                    'retry_delay': 12,
                    'retry_exp_backoff': True,
                },
                {
                    'template': {'path': './relative/path/to/my-template.yaml'},
                    'name': 'D',
                    'description': 'description D',
                    'tags': ['tag31', 'tag32'],
                    'dependencies': ['B', 'C'],
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                        'max_restarts': 3
                    },
                    'max_retries': 3
                }
            ],
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        config.process_dag()
        config.validate_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()

    def test_pipelines_templates(self):
        config_dict = {
            'templates': [
                {
                    'kind': 'experiment',
                    'name': 'experiment-template',
                    'description': 'description experiment',
                    'tags': ['tag11', 'tag12'],
                    'inputs': [
                        {
                            'name': 'input1',
                            'description': 'some text',
                            'type': IOTypes.FLOAT,
                        },
                        {
                            'name': 'input2',
                            'description': 'some text',
                            'type': IOTypes.BOOL,
                            'is_optional': True,
                            'default': True,
                        }
                    ],
                    'outputs': [
                        {
                            'name': 'output1',
                            'description': 'some text',
                            'type': IOTypes.S3_PATH
                        }
                    ],
                    'build': {'dockerfile': 'Dockerfile'},
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                        'max_restarts': 2
                    },
                },
                {
                    'kind': 'group',
                    'name': 'group-template',
                    'description': 'description group',
                    'tags': ['tag11', 'tag12'],
                    'inputs': [
                        {
                            'name': 'input1',
                            'description': 'some text',
                            'type': IOTypes.FLOAT,
                        },
                        {
                            'name': 'input2',
                            'description': 'some text',
                            'type': IOTypes.BOOL,
                            'is_optional': True,
                            'default': True,
                        }
                    ],
                    'outputs': [
                        {
                            'name': 'output1',
                            'description': 'some text',
                            'type': IOTypes.S3_PATH
                        }
                    ],
                    'build': {'ref': '12'},
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                        'max_restarts': 2
                    },
                },
                {
                    'kind': 'build',
                    'name': 'build-template',
                    'description': 'description build',
                    'tags': ['tag11', 'tag12'],
                    'ref': '12'
                },
                {
                    'kind': 'build',
                    'name': 'build-template',
                    'description': 'description build',
                    'tags': ['tag11', 'tag12'],
                    'backend': 'kaniko',
                    'dockerfile': 'Dockerfile',
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                        'max_restarts': 2
                    },
                },
                {
                    'kind': 'job',
                    'name': 'job-template',
                    'description': 'description job',
                    'tags': ['tag11', 'tag12'],
                    'inputs': [
                        {
                            'name': 'input1',
                            'description': 'some text',
                            'type': IOTypes.S3_PATH,
                            'is_optional': True,
                            'default': 's3://foo'
                        }
                    ],
                    'build': {'ref': '12'},
                    'outputs': [
                        {
                            'name': 'output1',
                            'description': 'some text',
                            'type': IOTypes.S3_PATH
                        }
                    ],
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                        'max_restarts': 2
                    },
                },
            ],
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        config.process_dag()
        config.validate_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()

    def test_pipelines_dag(self):
        config_dict = {
            'ops': [
                {
                    'template': {'action': 'action1'},
                    'name': 'A',
                    'params': {'param1': 'text', 'param2': 12, 'param3': 'https://foo.com'},
                },
                {
                    'template': {'url': 'https://url-to-temaplte.com'},
                    'name': 'B',
                    'params': {
                        'param1': '{{ ops.A.outputs.x }}',
                        'param2': 12,
                        'param3': 'https://foo.com'
                    },
                },
                {
                    'template': {'name': 'my-template'},
                    'name': 'C',
                    'params': {
                        'param2': 12.34,
                        'param3': False
                    },
                },
                {
                    'template': {'path': './relative/path/to/my-template.yaml'},
                    'name': 'D',
                    'dependencies': ['B', 'C'],
                }
            ],
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {'A', 'C', }
        assert config.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert sorted_dag[0] in [['A', 'C'], ['C', 'A']]
        assert sorted_dag[1] == ['B']
        assert sorted_dag[2] == ['D']

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'action1'}
        assert config.dag['A'].upstream == set()
        assert config.dag['A'].downstream == {'B', }

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'url': 'https://url-to-temaplte.com'}
        assert config.dag['B'].upstream == {'A', }
        assert config.dag['B'].downstream == {'D', }

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'name': 'my-template'}
        assert config.dag['C'].upstream == set()
        assert config.dag['C'].downstream == {'D', }

        assert config.dag['D'].op.name == 'D'
        assert config.dag['D'].op.template.to_dict() == {
            'path': './relative/path/to/my-template.yaml'}
        assert config.dag['D'].upstream == {'B', 'C'}
        assert config.dag['D'].downstream == set()

    def test_pipelines_parallel_ops(self):
        config_dict = {
            'ops': [
                {
                    'template': {'action': 'action1'},
                    'name': 'A',
                },
                {
                    'template': {'event': 'event1'},
                    'name': 'B',
                },
                {
                    'template': {'name': 'foo'},
                    'name': 'C',
                },
                {
                    'template': {'name': 'bar'},
                    'name': 'D',
                }
            ],
        }

        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {'A', 'B', 'C', 'D'}
        assert config.get_orphan_ops(dag=dag) == set([])
        assert len(config.sort_topologically(dag=dag)) == 1  # order can be any
        assert len(config.sort_topologically(dag=dag)[0]) == 4  # order can be any

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'action1'}
        assert config.dag['A'].upstream == set()
        assert config.dag['A'].downstream == set()

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'event': 'event1'}
        assert config.dag['B'].upstream == set()
        assert config.dag['B'].downstream == set()

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'name': 'foo'}
        assert config.dag['C'].upstream == set()
        assert config.dag['C'].downstream == set()

        assert config.dag['D'].op.name == 'D'
        assert config.dag['D'].op.template.to_dict() == {'name': 'bar'}
        assert config.dag['D'].upstream == set()
        assert config.dag['D'].downstream == set()

    def test_pipelines_sequential_ops(self):
        config_dict = {
            'ops': [
                {
                    'template': {'action': 'action1'},
                    'name': 'A',
                },
                {
                    'template': {'event': 'event1'},
                    'name': 'B',
                    'dependencies': ['A']
                },
                {
                    'template': {'name': 'foo'},
                    'name': 'C',
                    'dependencies': ['B']
                },
                {
                    'template': {'name': 'bar'},
                    'name': 'D',
                    'dependencies': ['C']
                }
            ],
        }

        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {'A', }
        assert config.get_orphan_ops(dag=dag) == set([])
        assert config.sort_topologically(dag=dag) == [['A'], ['B'], ['C'], ['D']]

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'action1'}
        assert config.dag['A'].upstream == set()
        assert config.dag['A'].downstream == {'B', }

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'event': 'event1'}
        assert config.dag['B'].upstream == {'A', }
        assert config.dag['B'].downstream == {'C', }

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'name': 'foo'}
        assert config.dag['C'].upstream == {'B', }
        assert config.dag['C'].downstream == {'D', }

        assert config.dag['D'].op.name == 'D'
        assert config.dag['D'].op.template.to_dict() == {'name': 'bar'}
        assert config.dag['D'].upstream == {'C', }
        assert config.dag['D'].downstream == set()

    def test_pipelines_all_downstream(self):
        config_dict = {
            'ops': [
                {
                    'template': {'action': 'action1'},
                    'name': 'A',
                    'params': {'param1': 'text', 'param2': 12, 'param3': 'https://foo.com'},
                    'dependencies': ['B', 'C', 'D'],
                },
                {
                    'template': {'event': 'event1'},
                    'name': 'B',
                },
                {
                    'template': {'event': 'event2'},
                    'name': 'C',
                },
                {
                    'template': {'event': 'event3'},
                    'name': 'D',
                }
            ],
        }

        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {'B', 'C', 'D', }
        assert config.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        # Sort is not guaranteed at stage 0
        assert len(sorted_dag[0]) == 3
        assert set(sorted_dag[0]) == {'B', 'C', 'D'}
        assert sorted_dag[1] == ['A']

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'action1'}
        assert config.dag['A'].upstream == {'B', 'C', 'D'}
        assert config.dag['A'].downstream == set()

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'event': 'event1'}
        assert config.dag['B'].upstream == set()
        assert config.dag['B'].downstream == {'A', }

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'event': 'event2'}
        assert config.dag['C'].upstream == set()
        assert config.dag['C'].downstream == {'A', }

        assert config.dag['D'].op.name == 'D'
        assert config.dag['D'].op.template.to_dict() == {'event': 'event3'}
        assert config.dag['D'].upstream == set()
        assert config.dag['D'].downstream == {'A', }

    def test_pipelines_acyclic_deps(self):
        config_dict = {
            'ops': [
                {
                    'template': {'action': 'action1'},
                    'name': 'A',
                    'dependencies': ['B']
                },
                {
                    'template': {'event': 'event1'},
                    'name': 'B',
                    'dependencies': ['A']
                },
                {
                    'template': {'name': 'foo'},
                    'name': 'C',
                    'dependencies': ['A']
                }
            ],
        }

        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        with self.assertRaises(PolyaxonSchemaError):
            config.validate_dag()
        dag = config.dag
        assert len(dag) == 3
        assert config.get_independent_ops(dag=dag) == set()
        assert config.get_orphan_ops(dag=dag) == set()
        with self.assertRaises(PolyaxonSchemaError):
            config.sort_topologically(dag=dag)

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'action1'}
        assert config.dag['A'].upstream == {'B', }
        assert config.dag['A'].downstream == {'B', 'C'}

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'event': 'event1'}
        assert config.dag['B'].upstream == {'A', }
        assert config.dag['B'].downstream == {'A', }

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'name': 'foo'}
        assert config.dag['C'].upstream == {'A', }
        assert config.dag['C'].downstream == set()

    def test_pipelines_circular_deps(self):
        config_dict = {
            'ops': [
                {
                    'template': {'action': 'action1'},
                    'name': 'A',
                    'dependencies': ['C']
                },
                {
                    'template': {'event': 'event1'},
                    'name': 'B',
                    'dependencies': ['A']
                },
                {
                    'template': {'name': 'foo'},
                    'name': 'C',
                    'dependencies': ['B']
                }
            ],
        }

        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        with self.assertRaises(PolyaxonSchemaError):
            config.validate_dag()
        dag = config.dag
        assert len(dag) == 3
        assert config.get_independent_ops(dag=dag) == set()
        assert config.get_orphan_ops(dag=dag) == set()
        with self.assertRaises(PolyaxonSchemaError):
            config.sort_topologically(dag=dag)

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'action1'}
        assert config.dag['A'].upstream == {'C', }
        assert config.dag['A'].downstream == {'B', }

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'event': 'event1'}
        assert config.dag['B'].upstream == {'A', }
        assert config.dag['B'].downstream == {'C', }

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'name': 'foo'}
        assert config.dag['C'].upstream == {'B', }
        assert config.dag['C'].downstream == {'A', }

    def test_pipelines_adding_ops_one_by_one_manually(self):
        config_dict = {
            'ops': [
                {
                    'template': {'action': 'action1'},
                    'name': 'A',
                },
                {
                    'template': {'event': 'event1'},
                    'name': 'B',
                    'dependencies': ['A']
                },
                {
                    'template': {'name': 'foo'},
                    'name': 'C',
                    'dependencies': ['A']
                }
            ],
        }

        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 3
        assert config.get_independent_ops(dag=dag) == {'A', }
        assert config.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert sorted_dag[0] == ['A']  # Only this one has consistent order
        assert sorted_dag[1] in [['B', 'C'], ['C', 'B']]

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'action1'}
        assert config.dag['A'].upstream == set()
        assert config.dag['A'].downstream == {'B', 'C'}

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'event': 'event1'}
        assert config.dag['B'].upstream == {'A', }
        assert config.dag['B'].downstream == set()

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'name': 'foo'}
        assert config.dag['C'].upstream == {'A', }
        assert config.dag['C'].downstream == set()

        template4 = TemplateRefConfig.from_dict({'action': 'action4'})
        operationD = OpConfig(template=template4, name='D', dependencies=['B', 'C'])
        config.add_op(operationD)

        operationE = OpConfig(template=template4, name='E', dependencies=['A'])
        config.add_op(operationE)

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 5
        assert config.get_independent_ops(dag=dag) == {'A', }
        assert config.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert sorted_dag[0] == ['A']
        # Sort is not guaranteed at stage 1
        assert len(sorted_dag[1]) == 3
        assert set(sorted_dag[1]) == {'B', 'C', 'E'}
        assert sorted_dag[2] == ['D']

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'action1'}
        assert config.dag['A'].upstream == set()
        assert config.dag['A'].downstream == {'B', 'C', 'E'}

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'event': 'event1'}
        assert config.dag['B'].upstream == {'A', }
        assert config.dag['B'].downstream == {'D', }

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'name': 'foo'}
        assert config.dag['C'].upstream == {'A', }
        assert config.dag['C'].downstream == {'D', }

        assert config.dag['D'].op.name == 'D'
        assert config.dag['D'].op.template.to_dict() == {'action': 'action4'}
        assert config.dag['D'].upstream == {'B', 'C'}
        assert config.dag['D'].downstream == set()

        assert config.dag['E'].op.name == 'E'
        assert config.dag['E'].op.template.to_dict() == {'action': 'action4'}
        assert config.dag['E'].upstream == {'A', }
        assert config.dag['E'].downstream == set()

        # Adding the same ops should not alter the behaviour
        config.add_ops([operationD, operationE])

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 5
        assert config.get_independent_ops(dag=dag) == {'A', }
        assert config.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert sorted_dag[0] == ['A']
        # Sort is not guaranteed at stage 1
        assert len(sorted_dag[1]) == 3
        assert set(sorted_dag[1]) == {'B', 'C', 'E'}
        assert sorted_dag[2] == ['D']

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'action1'}
        assert config.dag['A'].upstream == set()
        assert config.dag['A'].downstream == {'B', 'C', 'E'}

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'event': 'event1'}
        assert config.dag['B'].upstream == {'A', }
        assert config.dag['B'].downstream == {'D', }

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'name': 'foo'}
        assert config.dag['C'].upstream == {'A', }
        assert config.dag['C'].downstream == {'D', }

        assert config.dag['D'].op.name == 'D'
        assert config.dag['D'].op.template.to_dict() == {'action': 'action4'}
        assert config.dag['D'].upstream == {'B', 'C'}
        assert config.dag['D'].downstream == set()

        assert config.dag['E'].op.name == 'E'
        assert config.dag['E'].op.template.to_dict() == {'action': 'action4'}
        assert config.dag['E'].upstream == {'A', }
        assert config.dag['E'].downstream == set()

    def test_pipelines_adding_ops_many_manually(self):
        config_dict = {
            'ops': [
                {
                    'template': {'action': 'action1'},
                    'name': 'A',
                },
                {
                    'template': {'event': 'event1'},
                    'name': 'B',
                    'dependencies': ['A']
                },
                {
                    'template': {'name': 'foo'},
                    'name': 'C',
                    'dependencies': ['A']
                }
            ],
        }

        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 3
        assert config.get_independent_ops(dag=dag) == {'A', }
        assert config.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert sorted_dag[0] == ['A']  # Only this one has consistent order
        assert sorted_dag[1] in [['B', 'C'], ['C', 'B']]

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'action1'}
        assert config.dag['A'].upstream == set()
        assert config.dag['A'].downstream == {'B', 'C'}

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'event': 'event1'}
        assert config.dag['B'].upstream == {'A', }
        assert config.dag['B'].downstream == set()

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'name': 'foo'}
        assert config.dag['C'].upstream == {'A', }
        assert config.dag['C'].downstream == set()

        template4 = TemplateRefConfig.from_dict({'action': 'action4'})
        operationD = OpConfig(template=template4, name='D', dependencies=['B', 'C'])
        operationE = OpConfig(template=template4, name='E', dependencies=['A'])
        config.add_ops([operationD, operationE])

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        config.validate_dag()
        assert len(config.dag) == 5
        assert config.get_independent_ops(dag=config.dag) == {'A', }
        assert config.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert sorted_dag[0] == ['A']
        # Sort is not guaranteed at stage 1
        assert len(sorted_dag[1]) == 3
        assert set(sorted_dag[1]) == {'B', 'C', 'E'}
        assert sorted_dag[2] == ['D']

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'action1'}
        assert config.dag['A'].upstream == set()
        assert config.dag['A'].downstream == {'B', 'C', 'E'}

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'event': 'event1'}
        assert config.dag['B'].upstream == {'A', }
        assert config.dag['B'].downstream == {'D', }

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'name': 'foo'}
        assert config.dag['C'].upstream == {'A', }
        assert config.dag['C'].downstream == {'D', }

        assert config.dag['D'].op.name == 'D'
        assert config.dag['D'].op.template.to_dict() == {'action': 'action4'}
        assert config.dag['D'].upstream == {'B', 'C'}
        assert config.dag['D'].downstream == set()

        assert config.dag['E'].op.name == 'E'
        assert config.dag['E'].op.template.to_dict() == {'action': 'action4'}
        assert config.dag['E'].upstream == {'A', }
        assert config.dag['E'].downstream == set()

        # Adding the same ops should not alter the behaviour
        config.add_op(operationD)
        config.add_op(operationE)

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 5
        assert config.get_independent_ops(dag=dag) == {'A', }
        assert config.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert sorted_dag[0] == ['A']
        # Sort is not guaranteed at stage 1
        assert len(sorted_dag[1]) == 3
        assert set(sorted_dag[1]) == {'B', 'C', 'E'}
        assert sorted_dag[2] == ['D']

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'action1'}
        assert config.dag['A'].upstream == set()
        assert config.dag['A'].downstream == {'B', 'C', 'E'}

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'event': 'event1'}
        assert config.dag['B'].upstream == {'A', }
        assert config.dag['B'].downstream == {'D', }

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'name': 'foo'}
        assert config.dag['C'].upstream == {'A', }
        assert config.dag['C'].downstream == {'D', }

        assert config.dag['D'].op.name == 'D'
        assert config.dag['D'].op.template.to_dict() == {'action': 'action4'}
        assert config.dag['D'].upstream == {'B', 'C'}
        assert config.dag['D'].downstream == set()

        assert config.dag['E'].op.name == 'E'
        assert config.dag['E'].op.template.to_dict() == {'action': 'action4'}
        assert config.dag['E'].upstream == {'A', }
        assert config.dag['E'].downstream == set()

    def test_pipelines_dependency_from_params(self):
        config_dict = {
            'ops': [
                {
                    'template': {'action': 'echo'},
                    'name': 'A',
                    'params': {'param1': 'text', 'param2': 12, 'param3': 'https://foo.com'},
                },
                {
                    'template': {'action': 'echo'},
                    'name': 'B',
                    'params': {
                        'param1': '{{ ops.A.outputs.x }}',
                        'param2': 12,
                        'param3': 'https://foo.com'
                    },
                },
                {
                    'template': {'action': 'echo'},
                    'name': 'C',
                    'params': {
                        'param1': '{{ ops.A.outputs.x }}',
                        'param2': '{{ ops.B.outputs.x }}',
                    },

                },
                {
                    'template': {'action': 'echo'},
                    'name': 'D',
                    'dependencies': ['B', 'C'],
                }
            ],
        }

        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {'A', }
        assert config.get_orphan_ops(dag=dag) == set([])
        assert config.sort_topologically(dag=dag) == [['A'], ['B'], ['C'], ['D']]

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'echo'}
        assert config.dag['A'].upstream == set()
        assert config.dag['A'].downstream == {'B', 'C'}

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'action': 'echo'}
        assert config.dag['B'].upstream == {'A', }
        assert config.dag['B'].downstream == {'C', 'D', }

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'action': 'echo'}
        assert config.dag['C'].upstream == {'A', 'B'}
        assert config.dag['C'].downstream == {'D', }

        assert config.dag['D'].op.name == 'D'
        assert config.dag['D'].op.template.to_dict() == {'action': 'echo'}
        assert config.dag['D'].upstream == {'B', 'C'}
        assert config.dag['D'].downstream == set()

    def test_pipelines_dependency_and_params(self):
        config_dict = {
            'ops': [
                {
                    'template': {'action': 'echo'},
                    'name': 'A',
                    'params': {'param1': 'text', 'param2': 12, 'param3': 'https://foo.com'},
                },
                {
                    'template': {'action': 'echo'},
                    'name': 'B',
                    'params': {
                        'param1': '{{ ops.A.outputs.x }}',
                        'param2': 12,
                        'param3': 'https://foo.com'
                    },
                    'dependencies': ['A']
                },
                {
                    'template': {'action': 'echo'},
                    'name': 'C',
                    'params': {
                        'param2': '{{ ops.B.outputs.x }}',
                    },
                    'dependencies': ['A']
                },
                {
                    'template': {'action': 'echo'},
                    'name': 'D',
                    'dependencies': ['B', 'C'],
                }
            ],
        }

        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {'A', }
        assert config.get_orphan_ops(dag=dag) == set([])
        assert config.sort_topologically(dag=dag) == [['A'], ['B'], ['C'], ['D']]

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'echo'}
        assert config.dag['A'].upstream == set()
        assert config.dag['A'].downstream == {'B', 'C'}

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'action': 'echo'}
        assert config.dag['B'].upstream == {'A', }
        assert config.dag['B'].downstream == {'C', 'D', }

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'action': 'echo'}
        assert config.dag['C'].upstream == {'A', 'B'}
        assert config.dag['C'].downstream == {'D', }

        assert config.dag['D'].op.name == 'D'
        assert config.dag['D'].op.template.to_dict() == {'action': 'echo'}
        assert config.dag['D'].upstream == {'B', 'C'}
        assert config.dag['D'].downstream == set()

    def test_pipelines_orphan_ops(self):
        config_dict = {
            'ops': [
                {
                    'template': {'action': 'action1'},
                    'name': 'A',
                },
                {
                    'template': {'event': 'event1'},
                    'name': 'B',
                    'dependencies': ['A']
                },
                {
                    'template': {'name': 'foo'},
                    'name': 'C',
                    'dependencies': ['A', 'E']
                }
            ],
        }

        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.dag == {}

        # Process the dag
        config.process_dag()
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()
        with self.assertRaises(PolyaxonSchemaError):
            config.validate_dag()
        dag = config.dag
        assert len(dag) == 4
        assert config.get_independent_ops(dag=dag) == {'A', 'E', }
        assert config.get_orphan_ops(dag=dag) == {'E', }
        sorted_dag = config.sort_topologically(dag=dag)
        assert sorted_dag[0] in [['A', 'E'], ['E', 'A']]
        assert sorted_dag[1] in [['B', 'C'], ['C', 'B']]

        assert config.dag['A'].op.name == 'A'
        assert config.dag['A'].op.template.to_dict() == {'action': 'action1'}
        assert config.dag['A'].upstream == set()
        assert config.dag['A'].downstream == {'B', 'C'}

        assert config.dag['B'].op.name == 'B'
        assert config.dag['B'].op.template.to_dict() == {'event': 'event1'}
        assert config.dag['B'].upstream == {'A', }
        assert config.dag['B'].downstream == set()

        assert config.dag['C'].op.name == 'C'
        assert config.dag['C'].op.template.to_dict() == {'name': 'foo'}
        assert config.dag['C'].upstream == {'A', 'E'}
        assert config.dag['C'].downstream == set()

    def test_pipelines_with_duplicate_template_names(self):
        config_dict = {
            'ops': [
                {
                    'template': {'action': 'action1'},
                    'name': 'A',
                },
                {
                    'template': {'action': 'action1'},
                    'name': 'B',
                }
            ],
            'templates': [
                {
                    'kind': 'build',
                    'name': 'build-template',
                    'description': 'description build',
                    'tags': ['tag11', 'tag12'],
                    'ref': '12'
                },
                {
                    'kind': 'build',
                    'name': 'build-template',
                    'description': 'description build',
                    'tags': ['tag11', 'tag12'],
                    'backend': 'kaniko',
                    'dockerfile': 'Dockerfile',
                },
            ]
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()

    def test_pipelines_with_duplicate_op_names(self):
        config_dict = {
            'ops': [
                {
                    'template': {'name': 'build-template1'},
                    'name': 'A',
                },
                {
                    'template': {'name': 'build-template1'},
                    'name': 'A',
                }
            ],
            'templates': [
                {
                    'kind': 'build',
                    'name': 'build-template1',
                    'description': 'description build',
                    'tags': ['tag11', 'tag12'],
                    'ref': '12'
                },
                {
                    'kind': 'build',
                    'name': 'build-template2',
                    'description': 'description build',
                    'tags': ['tag11', 'tag12'],
                    'backend': 'kaniko',
                    'dockerfile': 'Dockerfile',
                },
            ]
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()

    def test_pipelines_with_op_requesting_undefined_template(self):
        config_dict = {
            'ops': [
                {
                    'template': {'name': 'build-template1'},
                    'name': 'A',
                },
                {
                    'template': {'name': 'build-template1'},
                    'name': 'A',
                }
            ],
            'templates': [
                {
                    'kind': 'build',
                    'name': 'build-template2',
                    'description': 'description build',
                    'tags': ['tag11', 'tag12'],
                    'backend': 'kaniko',
                    'dockerfile': 'Dockerfile',
                },
            ]
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(PolyaxonSchemaError):
            config.process_templates()

    def test_pipelines_with_template_not_defining_inputs(self):
        config_dict = {
            'ops': [
                {
                    'template': {'name': 'build-template'},
                    'name': 'A',
                },
                {
                    'template': {'name': 'job-template'},
                    'name': 'B',
                    'dependencies': ['A']
                }
            ],
            'templates': [
                {
                    'kind': 'job',
                    'name': 'job-template',

                },
                {
                    'kind': 'build',
                    'name': 'build-template',
                    'backend': 'kaniko',
                    'dockerfile': 'Dockerfile',
                },
            ]
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        config.process_templates()

    def test_pipelines_with_template_not_defining_inputs_and_ops_with_params(self):
        config_dict = {
            'ops': [
                {
                    'template': {'name': 'build-template'},
                    'name': 'A',
                },
                {
                    'template': {'name': 'job-template'},
                    'name': 'B',
                    'dependencies': ['A'],
                    'params': {
                        'param1': '{{ ops.A.outputs.x }}',
                        'param2': 12,
                        'param3': 'https://foo.com'
                    },
                }
            ],
            'templates': [
                {
                    'kind': 'job',
                    'name': 'job-template',

                },
                {
                    'kind': 'build',
                    'name': 'build-template',
                    'backend': 'kaniko',
                    'dockerfile': 'Dockerfile',
                },
            ]
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_templates()

    def test_pipelines_with_ops_template_required_inputs(self):
        config_dict = {
            'ops': [
                {
                    'template': {'name': 'job-template'},
                    'name': 'A',
                },
            ],
            'templates': [
                {
                    'kind': 'job',
                    'name': 'job-template',
                    'inputs': [
                        {
                            'name': 'input1',
                            'description': 'some text',
                            'type': IOTypes.FLOAT,
                        },
                    ],
                },
            ]
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_templates()

    def test_pipelines_with_ops_template_optional_inputs(self):
        config_dict = {
            'ops': [
                {
                    'template': {'name': 'job-template'},
                    'name': 'A',
                },
            ],
            'templates': [
                {
                    'kind': 'job',
                    'name': 'job-template',
                    'inputs': [
                        {
                            'name': 'input1',
                            'description': 'some text',
                            'type': IOTypes.FLOAT,
                            'is_optional': True,
                            'default': 12.2
                        },
                    ],
                },
            ]
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        config.process_templates()

    def test_pipelines_with_ops_template_optional_inputs_and_wrong_param(self):
        config_dict = {
            'ops': [
                {
                    'template': {'name': 'job-template'},
                    'name': 'A',
                    'params': {
                        'input1': 'foo',
                    },
                },
            ],
            'templates': [
                {
                    'kind': 'job',
                    'name': 'job-template',
                    'inputs': [
                        {
                            'name': 'input1',
                            'description': 'some text',
                            'type': IOTypes.FLOAT,
                            'is_optional': True,
                            'default': 12.2
                        },
                    ],
                },
            ]
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_templates()

    def test_pipelines_with_ops_template_validation(self):
        config_dict = {
            'ops': [
                {
                    'template': {'name': 'job-template'},
                    'name': 'A',
                    'params': {
                        'input1': 'sdf',
                        'input2': 12.,
                        'input3': False
                    },
                },
                {
                    'template': {'name': 'job-template'},
                    'name': 'B',
                    'dependencies': ['A'],
                    'params': {
                        'input1': 'ooo',
                        'input2': 12.123,
                    },
                }
            ],
            'templates': [
                {
                    'kind': 'job',
                    'name': 'job-template',
                    'inputs': [
                        {
                            'name': 'input1',
                            'description': 'some text',
                            'type': IOTypes.STR,
                        },
                        {
                            'name': 'input2',
                            'description': 'some text',
                            'type': IOTypes.FLOAT,
                        },
                        {
                            'name': 'input3',
                            'description': 'some text',
                            'type': IOTypes.BOOL,
                            'is_optional': True,
                            'default': True,
                        }
                    ],
                },
            ]
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        config.process_templates()

    def test_pipelines_with_wrong_refs(self):
        config_dict = {
            'ops': [
                {
                    'template': {'name': 'job-template'},
                    'name': 'A',
                    'params': {
                        'input1': 'sdf',
                        'input2': 12.,
                        'input3': False
                    },
                },
                {
                    'template': {'name': 'job-template'},
                    'name': 'B',
                    'dependencies': ['A'],
                    'params': {
                        'input1': '{{ ops.A.outputs.output1 }}',
                        'input2': 12.123,
                    },
                }
            ],
            'templates': [
                {
                    'kind': 'job',
                    'name': 'job-template',
                    'inputs': [
                        {
                            'name': 'input1',
                            'description': 'some text',
                            'type': IOTypes.STR,
                        },
                        {
                            'name': 'input2',
                            'description': 'some text',
                            'type': IOTypes.FLOAT,
                        },
                        {
                            'name': 'input3',
                            'description': 'some text',
                            'type': IOTypes.BOOL,
                            'is_optional': True,
                            'default': True,
                        }
                    ],
                },
            ]
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_templates()

    def test_pipelines_with_correct_refs(self):
        config_dict = {
            'ops': [
                {
                    'template': {'name': 'job-template'},
                    'name': 'A',
                    'params': {
                        'input1': 2,
                        'input2': 'gs://bucket/path/to/blob/',
                    },
                },
                {
                    'template': {'name': 'job-template'},
                    'name': 'B',
                    'dependencies': ['A'],
                    'params': {
                        'input1': '{{ ops.A.outputs.output1 }}',
                        'input2': 'gs://bucket/path/to/blob/',
                    },
                }
            ],
            'templates': [
                {
                    'kind': 'job',
                    'name': 'job-template',
                    'inputs': [
                        {
                            'name': 'input1',
                            'description': 'some text',
                            'type': IOTypes.INT,
                        },
                        {
                            'name': 'input2',
                            'description': 'some text',
                            'type': IOTypes.GCS_PATH,
                        },
                        {
                            'name': 'input3',
                            'description': 'some text',
                            'type': IOTypes.BOOL,
                            'is_optional': True,
                            'default': True,
                        }
                    ],
                    'outputs': [
                        {
                            'name': 'output1',
                            'description': 'some text',
                            'type': IOTypes.INT,
                            'is_optional': True,
                            'default': 123
                        },
                    ]
                },
            ]
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        config.process_templates()

    def test_pipelines_with_correct_ref_and_wrong_ref_type(self):
        config_dict = {
            'ops': [
                {
                    'template': {'name': 'job-template'},
                    'name': 'A',
                    'params': {
                        'input1': 2,
                        'input2': 'gs://bucket/path/to/blob/',
                        'output1': 123
                    },
                },
                {
                    'template': {'name': 'job-template'},
                    'name': 'B',
                    'dependencies': ['A'],
                    'params': {
                        'input1': 3,
                        'input2': '{{ ops.A.outputs.output1 }}',
                        'output1': 123
                    },
                }
            ],
            'templates': [
                {
                    'kind': 'job',
                    'name': 'job-template',
                    'inputs': [
                        {
                            'name': 'input1',
                            'description': 'some text',
                            'type': IOTypes.INT,
                        },
                        {
                            'name': 'input2',
                            'description': 'some text',
                            'type': IOTypes.GCS_PATH,
                        },
                        {
                            'name': 'input3',
                            'description': 'some text',
                            'type': IOTypes.BOOL,
                            'is_optional': True,
                            'default': True,
                        }
                    ],
                    'outputs': [
                        {
                            'name': 'output1',
                            'description': 'some text',
                            'type': IOTypes.INT,
                        },
                    ]
                },
            ]
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_templates()

    def test_pipelines_with_template_not_defining_inputs_and_ops_refs_params(self):
        config_dict = {
            'ops': [
                {
                    'template': {'name': 'build-template'},
                    'name': 'A',
                },
                {
                    'template': {'name': 'job-template'},
                    'name': 'B',
                    'dependencies': ['A'],
                    'params': {
                        'param1': '{{ ops.A.outputs.x }}',
                    },
                }
            ],
            'templates': [
                {
                    'kind': 'job',
                    'name': 'job-template',

                },
                {
                    'kind': 'build',
                    'name': 'build-template',
                    'backend': 'kaniko',
                    'dockerfile': 'Dockerfile',
                },
            ]
        }
        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.process_templates()

    def test_pipelines_with_ops_and_templates(self):
        config_dict = {
            'ops': [
                {
                    'template': {'name': 'build-template'},
                    'name': 'A',
                    'description': 'description A',
                    'tags': ['tag11', 'tag12'],
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                    },
                    'max_retries': 2
                },
                {
                    'template': {'name': 'experiment-template'},
                    'name': 'B',
                    'description': 'description B',
                    'tags': ['tag21', 'tag22'],
                    'dependencies': ['A'],
                    'params': {
                        'input1': 11.1,
                        'input2': False,
                        'output1': 'S3://foo.com'
                    },
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                    },
                    'max_retries': 2
                },
                {
                    'template': {'name': 'group-template'},
                    'name': 'C',
                    'description': 'description C',
                    'tags': ['tag31', 'tag32'],
                    'params': {
                        'input1': '{{ ops.B.outputs.output1 }}',
                        'output1': 'S3://foo.com',
                    },
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                    },
                    'max_retries': 5,
                    'retry_delay': 12,
                    'retry_exp_backoff': True,
                },
            ],
            'templates': [
                {
                    'kind': 'experiment',
                    'name': 'experiment-template',
                    'description': 'description experiment',
                    'tags': ['tag11', 'tag12'],
                    'inputs': [
                        {
                            'name': 'input1',
                            'description': 'some text',
                            'type': IOTypes.FLOAT,
                        },
                        {
                            'name': 'input2',
                            'description': 'some text',
                            'type': IOTypes.BOOL,
                            'is_optional': True,
                            'default': True,
                        }
                    ],
                    'outputs': [
                        {
                            'name': 'output1',
                            'description': 'some text',
                            'type': IOTypes.S3_PATH
                        }
                    ],
                    'build': {'dockerfile': 'Dockerfile'},
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                        'max_restarts': 2
                    },
                },
                {
                    'kind': 'group',
                    'name': 'group-template',
                    'description': 'description group',
                    'tags': ['tag11', 'tag12'],
                    'inputs': [
                        {
                            'name': 'input1',
                            'description': 'some text',
                            'type': IOTypes.S3_PATH
                        },
                        {
                            'name': 'input2',
                            'description': 'some text',
                            'type': IOTypes.BOOL,
                            'is_optional': True,
                            'default': True,
                        }
                    ],
                    'outputs': [
                        {
                            'name': 'output1',
                            'description': 'some text',
                            'type': IOTypes.S3_PATH
                        }
                    ],
                    'build': {'ref': '12'},
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                        'max_restarts': 2
                    },
                },
                {
                    'kind': 'build',
                    'name': 'build-template',
                    'description': 'description build',
                    'tags': ['tag11', 'tag12'],
                    'ref': '12'
                },
                {
                    'kind': 'build',
                    'name': 'build-template2',
                    'description': 'description build',
                    'tags': ['tag11', 'tag12'],
                    'backend': 'kaniko',
                    'dockerfile': 'Dockerfile',
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                        'max_restarts': 2
                    },
                },
                {
                    'kind': 'job',
                    'name': 'job-template',
                    'description': 'description job',
                    'tags': ['tag11', 'tag12'],
                    'inputs': [
                        {
                            'name': 'input1',
                            'description': 'some text',
                            'type': IOTypes.S3_PATH,
                            'is_optional': True,
                            'default': 's3://foo'
                        }
                    ],
                    'build': {'ref': '12'},
                    'outputs': [
                        {
                            'name': 'output1',
                            'description': 'some text',
                            'type': IOTypes.S3_PATH
                        }
                    ],
                    'environment': {
                        'resources': {'cpu': {'requests': 1}},
                        'node_selector': {'polyaxon': 'core'},
                        'service_account': 'service',
                        'image_pull_secrets': ['secret1', 'secret2'],
                        'max_restarts': 2
                    },
                },
            ],
        }

        config = PipelineConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        config.process_dag()
        config.validate_dag()
        config.process_templates()
        dag = config.dag
        assert len(dag) == 3
        assert config.get_independent_ops(dag=dag) == {'A', }
        assert config.get_orphan_ops(dag=dag) == set([])
        sorted_dag = config.sort_topologically(dag=dag)
        assert sorted_dag[0] == ['A']
        assert sorted_dag[1] == ['B']
        assert sorted_dag[2] == ['C']
