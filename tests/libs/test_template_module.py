# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx

from tensorflow.python.ops.template import Template
from tensorflow.python.platform import test


class DummyModule(plx.libs.GraphModule):

    def _build(self, incoming, *args, **kwargs):
        pass


class TestGraphModule(test.TestCase):
    def test_build(self):
        module = DummyModule(mode=plx.Modes.TRAIN, name='test')
        assert module._template is None
        assert module._is_built is False
        assert module.module_name is None
        assert module.variable_scope() is None

        module.build()

        assert isinstance(module._template, Template)
        assert module._is_built is True
        assert module._unique_name == 'test'
        assert module._template.variable_scope.name == 'test'
        assert module.variable_scope() is not None

    def test_build_with_calling_the_module(self):
        module = DummyModule(mode=plx.Modes.TRAIN, name='test')
        assert module._template is None
        assert module._is_built is False
        assert module.module_name is None
        assert module.variable_scope() is None

        module(1)

        assert isinstance(module._template, Template)
        assert module._is_built is True
        assert module._unique_name == 'test'
        assert module._template.variable_scope.name == 'test'
        assert module.variable_scope() is not None

    def test_unique_name(self):
        module1 = DummyModule(mode=plx.Modes.TRAIN, name='test')
        module2 = DummyModule(mode=plx.Modes.TRAIN, name='test')

        module1.build()
        module2.build()

        assert module1.module_name == 'test'
        assert module2.module_name == 'test_1'

    def test_variable_sharing(self):
        l = plx.layers.FullyConnected(mode=plx.Modes.TRAIN, num_units=1)
        x = tf.placeholder(dtype=tf.float32, shape=[1, 1])
        y = tf.placeholder(dtype=tf.float32, shape=[2, 1])

        lx = l(x)
        ly = l(y)

        init_all_op = tf.global_variables_initializer()
        assign_op = l.get_variables()[0].assign_add([[1]])

        with tf.Session('') as sess:
            sess.run(init_all_op)
            lx_results = lx.eval({x: [[1]]})
            ly_results = ly.eval({y: [[1], [1]]})
            assert len(lx_results) == 1
            assert len(ly_results) == 2

            assert lx_results[0] == ly_results[0][0]
            assert lx_results[0] == ly_results[1][0]

            sess.run(assign_op)
            lx_results_assign = lx.eval({x: [[1]]})
            ly_results_assign = ly.eval({y: [[1], [1]]})

            assert len(lx_results_assign) == 1
            assert len(ly_results_assign) == 2

            assert lx_results_assign[0] != lx_results[0][0]
            assert lx_results_assign[0] != ly_results[1][0]

            assert lx_results_assign[0] == ly_results_assign[0][0]
            assert lx_results_assign[0] == ly_results_assign[1][0]

    def test_copy_from(self):
        l1 = plx.layers.FullyConnected(mode=plx.Modes.TRAIN, num_units=1)
        l2 = plx.layers.FullyConnected(mode=plx.Modes.TRAIN, num_units=1)

        x = tf.placeholder(dtype=tf.float32, shape=[1, 1])

        lx1 = l1(x)
        lx2 = l2(x)

        init_all_op = tf.global_variables_initializer()
        copy_op = l2.copy_from(l1)
        assign_op = l1.get_variables()[0].assign_add([[1]])

        with tf.Session('') as sess:
            sess.run(init_all_op)

            # Check that initially they have different values
            lx1_results = lx1.eval({x: [[1]]})
            lx2_results = lx2.eval({x: [[1]]})

            assert lx1_results[0] != lx2_results[0]

            # Copying the variables should make the layers evaluate to the same value
            sess.run(copy_op)

            lx1_results = lx1.eval({x: [[1]]})
            lx2_results = lx2.eval({x: [[1]]})

            assert lx1_results[0] == lx2_results[0]

            # Changing a layer does not affect the other layer
            sess.run(assign_op)

            lx1_results = lx1.eval({x: [[1]]})
            lx2_results = lx2.eval({x: [[1]]})

            assert lx1_results[0] != lx2_results[0]
