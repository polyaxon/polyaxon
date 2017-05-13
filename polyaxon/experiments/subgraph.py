# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy

from polyaxon.libs.template_module import GraphModule


class SubGraph(GraphModule):
    """The `SubGraph` is a class that represents the flow of layers.

    Args:
        mode: `str`. Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: `str`. The name of this subgraph, used for creating the scope.
        methods: `list`.  The methods to connect inside this subgraph, e.g. layers
        kwargs: `list`. the list key word args to call each method with.
    """
    def __init__(self, mode, name, methods, kwargs):
        super(SubGraph, self).__init__(mode, name, self.ModuleType.SUBGRAPH)
        self.methods = methods
        self.kwargs = kwargs

    def _build(self, incoming, *args, **kwargs):
        for i, m in enumerate(self.methods):
            kwargs = copy.copy(self.kwargs[i])
            if 'dependencies' in kwargs:
                incoming = [dependency(self.mode, **dependency)(incoming)
                            for dependency in kwargs.pop('dependencies', [])]
            incoming = m(mode=self.mode, **kwargs)(incoming)
        return incoming
