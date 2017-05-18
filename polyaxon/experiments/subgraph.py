# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy

from polyaxon.libs.template_module import GraphModule, BaseLayer


class SubGraph(GraphModule):
    """The `SubGraph` is a class that represents the flow of layers.

    Args:
        mode: `str`. Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: `str`. The name of this subgraph, used for creating the scope.
        modules: `list`.  The modules to connect inside this subgraph, e.g. layers
        kwargs: `list`. the list key word args to call each method with.
    """
    def __init__(self, mode, name, modules, kwargs):
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

    @property
    def modules(self):
        return self._built_modules

    def _build(self, incoming, *args, **kwargs):
        for i, m in enumerate(self._modules):
            kwargs = copy.copy(self._kwargs[i])
            if 'dependencies' in kwargs:
                incoming = [dependency(self.mode, **dependency)(incoming)
                            for dependency in kwargs.pop('dependencies', [])]
            built_m = m(mode=self.mode, **kwargs)
            self._built_modules.append(built_m)
            incoming = built_m(incoming)
        return incoming
