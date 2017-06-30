# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx
from polyaxon.libs.subgraph import SubGraph
from polyaxon.libs.configs import SubGraphConfig


class TestSubgraph(tf.test.TestCase):
    def test_construct(self):
        config = SubGraphConfig(name='test',
                                modules=[plx.layers.FullyConnected, plx.layers.FullyConnected],
                                kwargs=[{'num_units': 12}, {'num_units': 6}])
        modules = SubGraph.build_subgraph_modules(mode=plx.Modes.TRAIN, subgraph_config=config)
        subgraph = SubGraph(mode=plx.Modes.TRAIN, modules=modules, **config.params)

        inputs = tf.placeholder(tf.float32, [67, 89])
        outputs = subgraph(inputs)

        self.assertEqual(outputs.get_shape().as_list(), [67, 6])

        self.assertEqual(len(subgraph.modules), 2)

    def test_construct_error(self):
        with self.assertRaises(TypeError):
            config = SubGraphConfig(
                name='test', modules=[plx.layers.FullyConnected, 5], kwargs=[{'num_units': 12}, {}])
            SubGraph.build_subgraph_modules(mode=plx.Modes.TRAIN, subgraph_config=config)

        with self.assertRaises(ValueError):
            config = SubGraphConfig(
                name='test', modules=[plx.layers.FullyConnected, plx.layers.LSTM],
                kwargs=[{'num_units': 12}])
            SubGraph.build_subgraph_modules(mode=plx.Modes.TRAIN, subgraph_config=config)

    def test_modules_get_scopes_outside_subgraph(self):
        m1 = plx.layers.FullyConnected(mode=plx.Modes.TRAIN, num_units=12)
        m2 = plx.layers.Dropout(mode=plx.Modes.TRAIN, keep_prob=0.5)
        m3 = plx.layers.FullyConnected(mode=plx.Modes.TRAIN, num_units=1)

        # Build m1 and m2
        m1.build()
        m2.build()

        subgraph = SubGraph(mode=plx.Modes.TRAIN, name='test', modules=[m1, m2, m3])
        subgraph.build()

        assert subgraph.module_name == 'test'
        assert subgraph._template.variable_scope.name == 'test'
        assert m1.module_name == 'FullyConnected'
        assert m1._template.variable_scope.name == 'FullyConnected'
        assert m2.module_name == 'Dropout'
        assert m2._template.variable_scope.name == 'Dropout'
        assert m3.module_name is None
        assert m3._template is None

        # Building the modules will assign them a scope outside the subgraph scope
        m3.build()
        assert subgraph.module_name == 'test'
        assert subgraph._template.variable_scope.name == 'test'
        assert m1.module_name == 'FullyConnected'
        assert m1._template.variable_scope.name == 'FullyConnected'
        assert m2.module_name == 'Dropout'
        assert m2._template.variable_scope.name == 'Dropout'
        assert m3.module_name == 'FullyConnected_1'
        assert m3._template.variable_scope.name == 'FullyConnected_1'

    def test_modules_get_scopes_inside_subgraph(self):
        m1 = plx.layers.FullyConnected(mode=plx.Modes.TRAIN, num_units=12)
        m2 = plx.layers.Dropout(mode=plx.Modes.TRAIN, keep_prob=0.5)
        m3 = plx.layers.FullyConnected(mode=plx.Modes.TRAIN, num_units=1)

        # Build m1
        m1.build()
        subgraph = SubGraph(mode=plx.Modes.TRAIN, name='test', modules=[m1, m2, m3])

        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        subgraph(x, y, None, None)
        assert subgraph.module_name == 'test'
        assert subgraph._template.variable_scope.name == 'test'
        assert m1.module_name == 'FullyConnected'
        assert m1._template.variable_scope.name == 'FullyConnected'
        assert m2.module_name == 'Dropout'
        assert m2._template.variable_scope.name == 'test/Dropout'
        assert m3.module_name == 'FullyConnected'
        assert m3._template.variable_scope.name == 'test/FullyConnected'

    def test_mulitple_inputs(self):
        # subgraph1_config = SubGraphConfig(
        #     name='subgraph1', modules=[plx.layers.FullyConnected], kwargs=[{'num_units': 12}])
        # subgraph1 = SubGraph(
        #     mode=plx.Modes.TRAIN, name=subgraph1_config.name,
        #     modules=SubGraph.build_subgraph_modules(mode=plx.Modes.TRAIN,
        #                                             subgraph_config=subgraph1_config))
        # subgraph2_config = SubGraphConfig(
        #     name='subgraph2',
        #     modules=[plx.layers.FullyConnected, plx.layers.Dropout, plx.layers.FullyConnected],
        #     kwargs=[{'num_units': 12}, {'keep_prob': 0.8}, {'num_units': 1}])
        # subgraph2 = SubGraph(
        #     mode=plx.Modes.TRAIN, name=subgraph2_config.name,
        #     modules=SubGraph.build_subgraph_modules(mode=plx.Modes.TRAIN,
        #                                             subgraph_config=subgraph2_config))
        # graph_config = SubGraphConfig(
        #     name='test',
        #     modules=[plx.layers.Merge, plx.layers.FullyConnected],
        #     kwargs=[{'modules': [subgraph1, subgraph1], 'merge_mode': 'prod'}, {'num_units': 12}])
        # graph = SubGraph(mode=plx.Modes.TRAIN, name=graph_config.name, )


        graph_config = {
            'name': 'graph',
            'definition': [
                (
                    plx.layers.Merge,
                    {
                        'merge_mode': 'prod',
                        'modules': [
                            {
                                'name': 'subgraph1',
                                'definition': [
                                    (
                                        plx.layers.FullyConnected,
                                        {'num_units': 10, 'activation': 'tanh'}
                                    ),
                                    (
                                        plx.layers.FullyConnected,
                                        {'num_units': 2, 'activation': 'tanh'}
                                    ),
                                ]
                            },
                            {
                                'name': 'subgraph2',
                                'definition': [
                                    (
                                        plx.layers.FullyConnected,
                                        {'num_units': 10, 'activation': 'relu'}
                                    ),
                                    (
                                        plx.layers.Dropout,
                                        {'keep_prob': 0.8}
                                    ),
                                    (
                                        plx.layers.FullyConnected,
                                        {'num_units': 10, 'activation': 'relu'}
                                    ),
                                ]
                            },
                        ]
                    }
                 ),
            ]
        }

        graph_config = SubGraphConfig.read_configs(config_values=graph_config)

        graph = SubGraph(
            mode=plx.Modes.TRAIN,
            modules=SubGraph.build_subgraph_modules(mode=plx.Modes.TRAIN,
                                                    subgraph_config=graph_config),
            **graph_config.params
        )

        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        graph(x, y, None, None)

        assert graph.module_name == 'graph'
        assert len(graph.modules) == 1
        merge_module = graph.modules[0]
        assert len(merge_module.modules) == 2
        for i, module in enumerate(merge_module.modules):
            assert isinstance(module, SubGraph)
            assert module.module_name == 'subgraph{}'.format(i + 1)
            assert module._template.variable_scope.name == 'graph/Merge/subgraph{}'.format(i + 1)
