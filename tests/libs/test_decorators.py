# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from polyaxon.libs.decorators import tf_template


class TestTfTemplate(tf.test.TestCase):
    def test_tf_template_with_function(self):
        @tf_template("test")
        def f():
            w = tf.get_variable("w", shape=[])
            return w

        w1 = f()
        w2 = f()
        w3 = f()
        self.assertTrue(w1 is w2)
        self.assertTrue(w2 is w3)

    def test_tf_template_with_class_function(self):
        class Test(object):
            @tf_template("test")
            def f(self):
                w = tf.get_variable("w", shape=[])
                return w

        test = Test()
        w1 = test.f()
        w2 = test.f()
        w3 = test.f()
        self.assertTrue(w1 is w2)
        self.assertTrue(w2 is w3)
