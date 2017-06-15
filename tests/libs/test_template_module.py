# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from tensorflow.python.ops.template import Template
from tensorflow.python.platform import test

from polyaxon import Modes
from polyaxon.libs.template_module import GraphModule


class DummyModule(GraphModule):

    def _build(self, incoming, *args, **kwargs):
        pass


class TestGraphModule(test.TestCase):
    def test_build(self):
        module = DummyModule(mode=Modes.TRAIN, name='test')
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
        module = DummyModule(mode=Modes.TRAIN, name='test')
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
        module1 = DummyModule(mode=Modes.TRAIN, name='test')
        module2 = DummyModule(mode=Modes.TRAIN, name='test')

        module1.build()
        module2.build()

        assert module1.module_name == 'test'
        assert module2.module_name == 'test_1'
