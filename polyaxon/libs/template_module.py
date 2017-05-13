# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc

import six
import tensorflow as tf


@six.add_metaclass(abc.ABCMeta)
class GraphModule(object):
    """Convenience class that makes it easy to share variables.

    Each instance of this class creates its own set of variables, but
    each subsequent execution of an instance will re-use its variables.

    Graph components that define variables should inherit from this class
    and implement their logic in the `_build` method.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: `str`, name of this module. Used for `tf.make_template`.
        module_type: `str`, the type of the module.
    """

    class ModuleType(object):
        MODEL = 'model'
        LAYER = 'layer'
        SUBGRAPH = 'subgraph'

        VALUES = [MODEL, SUBGRAPH, LAYER]

    def __init__(self, mode, name, module_type=None):
        self.name = name
        self.mode = mode
        self._template = tf.make_template(name, self._build, create_scope_now_=True)
        self._unique_name = self._template.variable_scope.name.split("/")[-1]
        self._type = module_type
        # Docstrings for the class should be the docstring for the _build method
        self.__doc__ = self._build.__doc__
        # pylint: disable=E1101
        self.__call__.__func__.__doc__ = self._build.__doc__

    @property
    def type(self):
        return self._type

    def _build(self, incoming, *args, **kwargs):
        """Subclasses should implement their logic here."""
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        # pylint: disable=missing-docstring
        return self._template(*args, **kwargs)

    def variable_scope(self):
        """Returns the proper variable scope for this module."""
        return tf.variable_scope(self._template.variable_scope)

    @property
    def module_name(self):
        """Returns the name of the Module."""
        return self._unique_name


@six.add_metaclass(abc.ABCMeta)
class BaseLayer(GraphModule):
    def __init__(self, mode, name):
        super(BaseLayer, self).__init__(mode, name, self.ModuleType.LAYER)
