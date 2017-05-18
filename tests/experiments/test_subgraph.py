# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx


class TestSubgraph(tf.test.TestCase):
    def test_construct(self):
        seq = plx.experiments.SubGraph(
            mode=plx.ModeKeys.TRAIN, name="subgraph1",
            modules=[plx.layers.FullyConnected, plx.layers.FullyConnected],
            kwargs=[{'n_units': 12}, {'n_units': 6}])

        inputs = tf.placeholder(tf.float32, [67, 89])
        outputs = seq(inputs)

        self.assertEqual(outputs.get_shape().as_list(), [67, 6])

        self.assertEqual(len(seq.modules), 2)

    def test_construct_error(self):
        with self.assertRaises(TypeError):
            plx.experiments.SubGraph(
                mode=plx.ModeKeys.TRAIN, name="subgraph1",
                modules=[plx.layers.FullyConnected, 5],
                kwargs=[{'n_units': 12}, {}])

        with self.assertRaises(ValueError):
            plx.experiments.SubGraph(
                mode=plx.ModeKeys.TRAIN, name="subgraph1",
                modules=[plx.layers.FullyConnected, plx.layers.LSTM],
                kwargs=[{'n_units': 12}])
