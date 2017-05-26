# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy

from collections import Mapping

import tensorflow as tf

from polyaxon.libs.template_module import GraphModule, BaseLayer


class SubGraph(GraphModule):
    """The `SubGraph` is a class that represents the flow of layers.

    Args:
        mode: `str`. Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: `str`. The name of this subgraph, used for creating the scope.
        modules: `list`.  The modules to connect inside this subgraph, e.g. layers
        kwargs: `list`. The list key word args to call each method with.
        features: `list`. The list of features keys to extract and use in this subgraph.
            If `None`, all features will be used.
    """
    def __init__(self, mode, name, modules, kwargs, features=None):
        super(SubGraph, self).__init__(mode, name, self.ModuleType.SUBGRAPH)
        if len(modules) != len(kwargs):
            raise ValueError('`Subgraph` expects `modules` and `kwargs` to have the same length.')

        wrong_modules = []
        for i, m in enumerate(modules):
            if not issubclass(m, BaseLayer):
                wrong_modules.append((i + 1, m))

        if wrong_modules:
            raise TypeError('`Subgraph` expects all modules to be subclass of `BaseLayer`, '
                             'received {}'.format(wrong_modules))

        self._modules = modules
        self._built_modules = []
        self._kwargs = kwargs
        self._features = features

    @property
    def modules(self):
        return self._built_modules

    def _get_incoming(self, incoming):
        if isinstance(incoming, Mapping):
            columns = self._features if self._features else list(incoming.keys())
            _incoming = [incoming[col] for col in columns]
            return tf.concat(values=_incoming, axis=1) if len(_incoming) > 1 else _incoming[0]
        return incoming

    def _build(self, incoming, *args, **kwargs):
        incoming = self._get_incoming(incoming)
        for i, m in enumerate(self._modules):
            kwargs = copy.copy(self._kwargs[i])
            if 'dependencies' in kwargs:
                incoming = [dependency(self.mode, **dependency)(incoming)
                            for dependency in kwargs.pop('dependencies', [])]
            built_m = m(mode=self.mode, **kwargs)
            self._built_modules.append(built_m)
            incoming = built_m(incoming)
        return incoming
