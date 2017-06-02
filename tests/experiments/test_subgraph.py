# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx
from polyaxon.libs.configs import SubGraphConfig


class TestSubgraph(tf.test.TestCase):
    def test_construct(self):
        config = SubGraphConfig('test',
                                modules=[plx.layers.FullyConnected, plx.layers.FullyConnected],
                                kwargs=[{'num_units': 12}, {'num_units': 6}])
        modules = plx.experiments.SubGraph.build_subgraph_modules(
            mode=plx.ModeKeys.TRAIN, subgraph_config=config)
        subgraph = plx.experiments.SubGraph(
            mode=plx.ModeKeys.TRAIN, name=config.name, modules=modules)

        inputs = tf.placeholder(tf.float32, [67, 89])
        outputs = subgraph(inputs)

        self.assertEqual(outputs.get_shape().as_list(), [67, 6])

        self.assertEqual(len(subgraph.modules), 2)

    def test_construct_error(self):
        with self.assertRaises(TypeError):
            config = SubGraphConfig('test',
                                    modules=[plx.layers.FullyConnected, 5],
                                    kwargs=[{'num_units=12'}, {}])
            plx.experiments.SubGraph.build_subgraph_modules(
                mode=plx.ModeKeys.TRAIN,
                subgraph_config=config)

        with self.assertRaises(ValueError):
            config = SubGraphConfig('test',
                                    modules=[plx.layers.FullyConnected, plx.layers.LSTM],
                                    kwargs=[{'num_units=12'}])
            plx.experiments.SubGraph.build_subgraph_modules(
                mode=plx.ModeKeys.TRAIN,
                subgraph_config=config)

    def test_modules_get_scopes_outside_subgraph(self):
        m1 = plx.layers.FullyConnected(mode=plx.ModeKeys.TRAIN, num_units=12)
        m2 = plx.layers.Dropout(mode=plx.ModeKeys.TRAIN, keep_prob=0.5)
        m3 = plx.layers.FullyConnected(mode=plx.ModeKeys.TRAIN, num_units=1)

        # Build m1 and m2
        m1.build()
        m2.build()

        subgrpah = plx.experiments.SubGraph(
            mode=plx.ModeKeys.TRAIN, name='test', modules=[m1, m2, m3])
        subgrpah.build()

        assert subgrpah.module_name == 'test'
        assert subgrpah._template.variable_scope.name == 'test'
        assert m1.module_name == 'FullyConnected'
        assert m1._template.variable_scope.name == 'FullyConnected'
        assert m2.module_name == 'Dropout'
        assert m2._template.variable_scope.name == 'Dropout'
        assert m3.module_name is None
        assert m3._template is None

        # Building the modules will assign them a scope outside the subgraph scope
        m3.build()
        assert subgrpah.module_name == 'test'
        assert subgrpah._template.variable_scope.name == 'test'
        assert m1.module_name == 'FullyConnected'
        assert m1._template.variable_scope.name == 'FullyConnected'
        assert m2.module_name == 'Dropout'
        assert m2._template.variable_scope.name == 'Dropout'
        assert m3.module_name == 'FullyConnected_1'
        assert m3._template.variable_scope.name == 'FullyConnected_1'

    def test_modules_get_scopes_inside_subgraph(self):
        m1 = plx.layers.FullyConnected(mode=plx.ModeKeys.TRAIN, num_units=12)
        m2 = plx.layers.Dropout(mode=plx.ModeKeys.TRAIN, keep_prob=0.5)
        m3 = plx.layers.FullyConnected(mode=plx.ModeKeys.TRAIN, num_units=1)

        # Build m1
        m1.build()
        subgrpah = plx.experiments.SubGraph(
            mode=plx.ModeKeys.TRAIN, name='test', modules=[m1, m2, m3])

        x = {'x': tf.placeholder(tf.float32, [2, 89])}
        y = tf.constant([[1], [1]])

        subgrpah(x, y, None, None)
        assert subgrpah.module_name == 'test'
        assert subgrpah._template.variable_scope.name == 'test'
        assert m1.module_name == 'FullyConnected'
        assert m1._template.variable_scope.name == 'FullyConnected'
        assert m2.module_name == 'Dropout'
        assert m2._template.variable_scope.name == 'test/Dropout'
        assert m3.module_name == 'FullyConnected'
        assert m3._template.variable_scope.name == 'test/FullyConnected'
