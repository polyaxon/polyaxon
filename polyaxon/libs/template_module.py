# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc

import six
import tensorflow as tf

from tensorflow.python.platform import tf_logging as logging


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
        IMAGE_PROCESSOR = 'image_processor'

        VALUES = [MODEL, SUBGRAPH, LAYER]

    def __init__(self, mode, name, module_type=None):
        self.name = name
        self.mode = mode
        self._template = None
        self._is_built = False
        self._unique_name = None
        self._type = module_type
        # Docstrings for the class should be the docstring for the _build method
        self.__doc__ = self._build.__doc__
        # pylint: disable=E1101
        self.__call__.__func__.__doc__ = self._build.__doc__

    @property
    def type(self):
        return self._type

    def build(self, *args, **kwargs):
        """Builds the module and sets the scope.

        This function will get called automatically when the module gets called.
        """
        if self._is_built:
            logging.info('Current Module name: `{}` is already built.'.format(self.name))
            return

        self._is_built = True
        self._template = tf.make_template(self.name, self._build, create_scope_now_=True)
        self._unique_name = self._template.variable_scope.name.split("/")[-1]

    def _build(self, incoming, *args, **kwargs):
        """Subclasses should implement their logic here."""
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        if not self._is_built:
            self.build(*args, **kwargs)

        return self._template(*args, **kwargs)

    def variable_scope(self):
        """Returns the proper variable scope for this module."""
        if not self._is_built:
            logging.info('Current Module: `{}` is called before build.'.format(self.name))
            return None
        return tf.variable_scope(self._template.variable_scope)

    @property
    def module_name(self):
        """Returns the name of the Module."""
        return self._unique_name


@six.add_metaclass(abc.ABCMeta)
class BaseLayer(GraphModule):
    def __init__(self, mode, name):
        super(BaseLayer, self).__init__(mode=mode, name=name, module_type=self.ModuleType.LAYER)


@six.add_metaclass(abc.ABCMeta)
class ImageProcessorModule(GraphModule):
    def __init__(self, mode, name):
        super(ImageProcessorModule, self).__init__(
            mode=mode, name=name, module_type=self.ModuleType.IMAGE_PROCESSOR)
