# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import functools

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

        with self.test_session() as sess:
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

        with self.test_session() as sess:
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

    def test_copy_from_with_no_trainable_vars(self):
        l1 = plx.layers.FullyConnected(mode=plx.Modes.TRAIN, num_units=1)
        l2 = plx.layers.FullyConnected(mode=plx.Modes.TRAIN, num_units=1, trainable=False)

        x = tf.placeholder(dtype=tf.float32, shape=[1, 1])

        lx1 = l1(x)
        lx2 = l2(x)

        init_all_op = tf.global_variables_initializer()
        copy_op = l2.copy_from(l1, tf.GraphKeys.GLOBAL_VARIABLES)
        assign_op = l1.get_variables()[0].assign_add([[1]])

        with self.test_session() as sess:
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

    def test_copy_from_works_with_control_flow(self):
        l1 = plx.layers.FullyConnected(mode=plx.Modes.TRAIN, num_units=1)
        l2 = plx.layers.FullyConnected(mode=plx.Modes.TRAIN, num_units=1, trainable=False)

        x = tf.placeholder(dtype=tf.float32, shape=[1, 1])

        lx1 = l1(x)
        lx2 = l2(x)

        init_all_op = tf.global_variables_initializer()

        def copy():
            # note that we need to put this copy_op in a function otherwise it will always
            # be evaluate no matter what the condition
            return l2.copy_from(l1, tf.GraphKeys.GLOBAL_VARIABLES)

        a = tf.placeholder(tf.int32, ())
        cond = tf.cond(tf.equal(tf.mod(a, 5), 0), copy, lambda: tf.no_op())
        assign_op = l1.get_variables()[0].assign_add([[1]])
        group_op = tf.group(*[assign_op, cond])

        with self.test_session() as sess:
            sess.run(init_all_op)

            # Check that initially they have different values
            lx1_results = lx1.eval({x: [[1]]})
            lx2_results = lx2.eval({x: [[1]]})

            assert lx1_results[0] != lx2_results[0]

            # Set condition to True 10 % 5 == 0
            sess.run(cond, feed_dict={a: 10})

            lx1_results = lx1.eval({x: [[1]]})
            lx2_results = lx2.eval({x: [[1]]})

            assert lx1_results[0] == lx2_results[0]

            # Assign and Set condition to False 2 % 5 != 0
            sess.run(group_op, feed_dict={a: 2})

            lx1_results = lx1.eval({x: [[1]]})
            lx2_results = lx2.eval({x: [[1]]})

            assert lx1_results[0] != lx2_results[0]


class TestFunctionModule(test.TestCase):
    def test_checks_function(self):
        with self.assertRaisesRegexp(TypeError, "`build_fn` must be callable."):
            plx.libs.FunctionModule(mode=plx.Modes.TRAIN, build_fn='not_a_function')

        with self.assertRaisesRegexp(ValueError, "`build_fn` must include `mode` argument."):
            plx.libs.FunctionModule(mode=plx.Modes.TRAIN, build_fn=lambda x: x)

    def test_sharing(self):
        batch_size = 3
        in_size = 4
        inputs1 = tf.placeholder(tf.float32, shape=[batch_size, in_size])
        inputs2 = tf.placeholder(tf.float32, shape=[batch_size, in_size])

        def dummy_fn(mode, inputs, output_size):
            weight_shape = [inputs.get_shape().as_list()[-1], output_size]
            weight = tf.get_variable("w", shape=weight_shape, dtype=inputs.dtype)
            return tf.matmul(inputs, weight)

        build_fn = functools.partial(dummy_fn, output_size=10)
        model = plx.libs.FunctionModule(plx.Modes.TRAIN, build_fn)
        outputs1 = model(inputs1)
        outputs2 = model(inputs2)

        self.assertEqual(model.scope_name(), "dummy_fn")

        import numpy as np
        input_data = np.random.rand(batch_size, in_size)

        with self.test_session() as sess:
            sess.run(tf.global_variables_initializer())
            outputs1, outputs2 = sess.run(
                [outputs1, outputs2], feed_dict={inputs1: input_data, inputs2: input_data})
            self.assertAllClose(outputs1, outputs2)
