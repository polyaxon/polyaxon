# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy

from collections import Mapping

import tensorflow as tf

from polyaxon.libs.template_module import GraphModule, BaseLayer, ImageProcessorModule

# Currently there's an issue with numpy_input_fn, it's keeps updating the Xs dictionary
FEATURE_BLACK_LIST = ['__target_key__', '__record_key__']


class SubGraph(GraphModule):
    """The `SubGraph` is a class that represents the flow of layers.

    Args:
        mode: `str`. Specifies if this training, evaluation or prediction. See `Modes`.
        name: `str`. The name of this subgraph, used for creating the scope.
        modules: `list`.  The modules to connect inside this subgraph, e.g. layers.
        features: `list`. The list of features keys to extract and use in this subgraph.
            If `None`, all features will be used.
    """
    def __init__(self, mode, modules, name='Subgraph', features=None):
        super(SubGraph, self).__init__(mode=mode, name=name, module_type=self.ModuleType.SUBGRAPH)

        wrong_modules = []
        for i, m in enumerate(modules):
            if not isinstance(m, (BaseLayer, ImageProcessorModule)):
                wrong_modules.append((i + 1, m))

        if wrong_modules:
            raise TypeError('`Subgraph` expects all modules to be subclass of `BaseLayer`, '
                            'received {}'.format(wrong_modules))

        self._modules = modules
        self._features = features

    @property
    def modules(self):
        return self._modules

    def _get_incoming(self, incoming):
        if isinstance(incoming, Mapping):
            columns = self._features if self._features else list(incoming.keys())
            _incoming = [incoming[col] for col in columns if col not in FEATURE_BLACK_LIST]
            return tf.concat(values=_incoming, axis=1) if len(_incoming) > 1 else _incoming[0]
        return incoming

    def _build(self, incoming, *args, **kwargs):
        incoming = self._get_incoming(incoming)
        for module in self._modules:
            incoming = module(incoming, *args, **kwargs)
        return incoming

    @classmethod
    def build_subgraph_modules(cls, mode, subgraph_config):
        if len(subgraph_config.modules) != len(subgraph_config.kwargs):
            raise ValueError('`Subgraph` expects `modules` and `modules_kwargs` '
                             'to have the same length.')

        built_modules = []
        for i, module in enumerate(subgraph_config.modules):
            kwargs = copy.copy(subgraph_config.kwargs[i])
            if 'modules' in kwargs:
                dependencies = []
                for dependency_config in kwargs['modules']:
                    dependency = cls(
                        mode=mode,
                        modules=cls.build_subgraph_modules(mode=mode,
                                                           subgraph_config=dependency_config),
                        features=dependency_config.features,
                        **dependency_config.params)
                    dependencies.append(dependency)

                kwargs['modules'] = dependencies

            built_module = module(mode=mode, **kwargs)
            built_modules.append(built_module)
        return built_modules
