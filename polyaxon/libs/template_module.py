# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
from collections import OrderedDict

import six
import tensorflow as tf

from tensorflow.python.platform import tf_logging as logging

from polyaxon.libs.utils import get_tracked, get_arguments, get_function_name


@six.add_metaclass(abc.ABCMeta)
class GraphModule(object):
    """Convenience class that makes it easy to share variables.

    Each instance of this class creates its own set of variables, but
    each subsequent execution of an instance will re-use its variables.

    Graph components that define variables should inherit from this class
    and implement their logic in the `_build` method.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        name: `str`, name of this module. Used for `tf.make_template`.
        module_type: `str`, the type of the module.
    """

    class ModuleType(object):
        MODEL = 'model'
        LAYER = 'layer'
        SUBGRAPH = 'subgraph'
        IMAGE_PROCESSOR = 'image_processor'
        PIPELINE = 'pipeline'
        BRIDGE = 'bridge'
        FUNCTION = 'function'

        VALUES = [MODEL, LAYER, SUBGRAPH, IMAGE_PROCESSOR, PIPELINE, BRIDGE, FUNCTION]

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
        self._unique_name = self._template.variable_scope.name.split('/')[-1]

    def _build(self, incoming, *args, **kwargs):
        """Subclasses should implement their logic here."""
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        if not self._is_built:
            self.build(*args, **kwargs)

        return self._template(*args, **kwargs)

    def variable_scope(self, create_context=False):
        """Returns the proper variable scope for this module."""
        if not self._is_built:
            logging.info('Current Module: `{}` is called before build.'.format(self.name))
            return None

        variable_scope = self._template.variable_scope
        if create_context:
            return tf.variable_scope(variable_scope)
        return variable_scope

    def scope_name(self):
        """Returns the proper scope name for this module."""
        return self.variable_scope().name

    def get_variables(self, collection=tf.GraphKeys.TRAINABLE_VARIABLES):
        """Returns tuple of `tf.Variable`s declared inside this module.
        Note that this operates by searching this module's variable scope,
        and so does not know about any modules that were constructed elsewhere but
        used inside this module.
        Args:
          collection: Collection to restrict query to. By default this is
            `tf.Graphkeys.TRAINABLE_VARIABLES`, which doesn't include non-trainable
            variables such as moving averages.
        Returns:
          A tuple of `tf.Variable` objects.
        Raises:
          NotConnectedError: If the module is not connected to the Graph.
        """
        return get_tracked(collection=collection, scope=self.scope_name() + '/')

    def get_variables_by_names(self, collection=tf.GraphKeys.TRAINABLE_VARIABLES):
        """Returns tuple of `tf.Variable`s declared inside this module.
        Note that this operates by searching this module's variable scope,
        and so does not know about any modules that were constructed elsewhere but
        used inside this module.
        Args:
          collection: Collection to restrict query to. By default this is
            `tf.Graphkeys.TRAINABLE_VARIABLES`, which doesn't include non-trainable
            variables such as moving averages.
        Returns:
          A tuple of `tf.Variable` objects.
        Raises:
          NotConnectedError: If the module is not connected to the Graph.
        """
        variables = self.get_variables(collection=collection)
        variables_by_names = OrderedDict()
        for var in variables:
            variables_by_names[var.name.split('{}/'.format(self.module_name))[1]] = var
        return variables_by_names

    @property
    def module_name(self):
        """Returns the name of the Module."""
        return self._unique_name

    def copy_from(self, module, collection=tf.GraphKeys.TRAINABLE_VARIABLES):
        """Copies variables from another module and assigns them to current module."""
        # Check is the same class
        if not isinstance(module, self.__class__):
            raise TypeError("You can only clone instances of `{}`. "
                            "Received `{}` instead.".format(self.__class__, type(module)))

        copy_ops = []

        current_variables = self.get_variables_by_names(collection=collection)
        target_variables = module.get_variables_by_names(collection=collection)
        for name in current_variables:
            copy_op = current_variables[name].assign(target_variables[name])
            copy_ops.append(copy_op)

        return tf.group(*copy_ops,
                        name='copy_op_from_{}_to_{}'.format(self.module_name, module.module_name))


@six.add_metaclass(abc.ABCMeta)
class BaseLayer(GraphModule):
    """Convenience class to create layers. See `GraphModule`'s docstring."""

    def __init__(self, mode, name):
        super(BaseLayer, self).__init__(mode=mode, name=name, module_type=self.ModuleType.LAYER)


@six.add_metaclass(abc.ABCMeta)
class ImageProcessorModule(GraphModule):
    """Convenience class to create image processors. See `GraphModule`'s docstring."""

    def __init__(self, mode, name):
        super(ImageProcessorModule, self).__init__(
            mode=mode, name=name, module_type=self.ModuleType.IMAGE_PROCESSOR)


class FunctionModule(GraphModule):
    """Constructs a module with a given build function.
    The Module class can be used to wrap a function assembling a network into a
    module.
    For example, the following code implements a simple one-hidden-layer MLP
    model by defining a function called make_model and using a Module instance
    to wrap it.
    ```python
    >>> import polyaxon as plx

    >>> def model_fn(mode, inputs):
    >>>     x = plx.layers.FullyConnected(mode, num_units=10)(inputs)
    >>>     x = plx.layers.FullyConnected(mode, num_units=10)(x)
    >>>     return x

    >>> model = plx.libs.FunctionModule(mode=plx.Modes.TRAIN, name='simple_mlp', build_fn=model_fn)
    >>> model(data)
    ```

    Args:
        build: Callable to be invoked when connecting the module to the graph.
            The `build` function is invoked when the module is called, and its
            role is to specify how to add elements to the Graph, and how to
            compute output Tensors from input Tensors.
            The `build` function signature can include the following parameters:
                `*args` - Input Tensors.
                `**kwargs` - Additional Python parameters controlling connection.

        name: Module name. If set to `None` (the default), the name will be set to
            that of the `build` callable converted to `snake_case`. If `build` has
            no name, the name will be 'module'.
        Raises:
            TypeError: If build is not callable.
    """

    def __init__(self, mode, build_fn, name=None):
        if not callable(build_fn):
            raise TypeError("`build_fn` must be callable.")

        build_fn_args = get_arguments(build_fn)
        if 'mode' not in build_fn_args:
            raise ValueError("`build_fn` must include `mode` argument.")

        self._build_fn = build_fn
        super(FunctionModule, self).__init__(
            mode=mode,
            name=name or get_function_name(build_fn),
            module_type=self.ModuleType.IMAGE_PROCESSOR)

    def _build(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Forwards call to the passed-in build function."""
        return self._build_fn(self.mode, *args, **kwargs)
