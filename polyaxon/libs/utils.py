# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import contextlib
import functools
import inspect
import uuid
import six

from collections import Mapping

import numpy as np
import tensorflow as tf

from tensorflow.python.ops import math_ops, array_ops
from tensorflow.python.platform import tf_logging as logging

from polyaxon.libs import MAPPING_COLLECTION


def track(tensor, collection, module_name=None):
    """Track tensor by adding it to the collection."""
    _collection = '{}/{}'.format(collection, module_name) if module_name else collection
    if isinstance(tensor, Mapping):
        if collection not in MAPPING_COLLECTION:
            raise TypeError("The collection `{}` does not expect a map type, received {}".format(
                collection, tensor
            ))
        key_collection = _collection + '_keys'
        value_collection = _collection + '_values'
        for key, value in tensor.items():
            tf.add_to_collection(name=key_collection, value=key)
            tf.add_to_collection(name=value_collection, value=value)
    else:
        tf.add_to_collection(name=_collection, value=tensor)


def get_tracked(collection, module_name=None, scope=None):
    """Returns a list of values in the collection with the given `collection`."""
    _collection = '{}/{}'.format(collection, module_name) if module_name else collection
    if collection in MAPPING_COLLECTION:
        key_collection = _collection + '_keys'
        value_collection = _collection + '_values'
        keys = tf.get_collection(key_collection)
        values = tf.get_collection(value_collection, scope=scope)
        return dict(zip(keys, values))
    else:
        return tf.get_collection(key=_collection, scope=scope)


def get_shape(x):
    """Get the incoming data shape.

    Args:
        x: incoming data.
    Returns:
        the incoming data shape.
    """
    if isinstance(x, (tf.Tensor, tf.Variable)):
        return x.get_shape().as_list()
    elif type(x) in [np.ndarray, list, tuple]:
        return np.shape(x)
    else:
        raise Exception('Invalid incoming layer.')


def validate_dtype(x):
    if x.dtype == tf.uint8:
        logging.warn("Received an incoming tensor with dtype: `uint8`, converted it to `float32`.")
        return tf.cast(x, tf.float32)
    else:
        return x


def get_variable_scope(name=None, scope=None, values=None, reuse=None):
    if not any([name, scope]):
        raise ValueError('`name` or `scope` is required!')
    return tf.variable_scope(scope, default_name=name, values=values, reuse=reuse)


def get_name_scope(name=None, scope=None, values=None):
    if not any([name, scope]):
        raise ValueError('`name` or `scope` is required!')
    return tf.name_scope(scope, default_name=name, values=values)


def _to_tensor(x, dtype):
    x = tf.convert_to_tensor(x)
    if x.dtype != dtype:
        x = tf.cast(x, dtype)
    return x


def clip(x, min_value, max_value):
    """Element-wise value clipping."""
    if max_value is not None and max_value < min_value:
        max_value = min_value
    if max_value is None:
        max_value = np.inf
    min_value = _to_tensor(min_value, x.dtype.base_dtype)
    max_value = _to_tensor(max_value, x.dtype.base_dtype)
    return tf.clip_by_value(x, min_value, max_value)


def int_or_tuple(value):
    """Converts `value` (int or tuple) to height, width.

    This functions normalizes the input value by always returning a tuple.

    Args:
        value: A list of 2 ints, 4 ints, a single int or a tf.TensorShape.

    Returns:
        A list with 4 values.

    Raises:
        ValueError: If `value` it not well formed.
        TypeError: if the `value` type is not supported
    """
    if isinstance(value, int):
        return [1, value, value, 1]
    elif isinstance(value, (tuple, list)):
        len_value = len(value)
        if len_value == 2:
            return [1, value[0], value[1], 1]
        elif len_value == 4:
            return [value[0], value[1], value[2], value[3]]
        else:
            raise ValueError('This operation does not support {} values list.'.format(len_value))
    raise TypeError('Expected an int, a list with 2/4 ints or a TensorShape of length 2, '
                    'instead received {}'.format(value))


def int_or_tuple_3d(value):
    """Converts `value` (int or tuple) to height, width for 3d ops.

    This functions normalizes the input value by always returning a tuple.

    Args:
        value: A list of 3 ints, 5 ints, a single int or a tf.TensorShape.

    Returns:
        A list with 5 values.

    Raises:
        ValueError: If `value` it not well formed.
        TypeError: if the `value` type is not supported
    """
    if isinstance(value, int):
        return [1, value, value, value, 1]
    elif isinstance(value, (tuple, list)):
        len_value = len(value)
        if len_value == 3:
            return [1, value[0], value[1], value[2], 1]
        elif len_value == 5:
            assert value[0] == value[4] == 1, 'Must have strides[0] = strides[4] = 1'
            return [value[0], value[1], value[2], value[3], value[4]]
        else:
            raise ValueError('This operation does not support {} values list.'.format(len_value))
    raise TypeError('Expected an int, a list with 3/5 ints or a TensorShape of length 3, '
                    'instead received {}'.format(value))


def validate_padding(value):
    """Validates and format padding value

    Args:
        value: `str` padding value to validate.

    Returns:
        formatted value.

    Raises:
        ValueError: if is not valid.
    """
    padding = value.upper()
    if padding not in ['SAME', 'VALID']:
        raise ValueError('Padding value `{}` is not supported, '
                         'expects `SAME`\`VALID`'.format(value))
    return padding


def validate_filter_size(filter_size, in_depth, num_filter):
    """Validates filter size for CNN operations"""
    if isinstance(filter_size, int):
        return [filter_size, filter_size, in_depth, num_filter]
    elif isinstance(filter_size, (tuple, list)):
        len_filter = len(filter_size)
        if len_filter == 2:
            return [filter_size[0], filter_size[1], in_depth, num_filter]
        else:
            raise ValueError('This operation does not support {} values list.'.format(len_filter))

    raise TypeError('Expected an int, a list with 2 ints instead received {}'.format(filter_size))


def validate_filter_size_3d(filter_size, in_depth, num_filter):
    """Validates filter size for 3d CNN operations"""
    if isinstance(filter_size, int):
        return [filter_size, filter_size, filter_size, in_depth, num_filter]
    elif isinstance(filter_size, (tuple, list)):
        len_filter = len(filter_size)
        if len_filter == 3:
            return [filter_size[0], filter_size[1], filter_size[2], in_depth, num_filter]
        else:
            raise ValueError('This operation does not support {} values list.'.format(len_filter))

    raise TypeError('Expected an int, a list with 3 ints instead received {}'.format(filter_size))


def check_restore_tensor(tensor_to_check, exclvars):
    for exclvar in exclvars:
        if isinstance(exclvar, six.string_types):
            if exclvar.split(':')[0] in tensor_to_check.name:
                return False
        elif exclvar.name.split(':')[0] in tensor_to_check.name:
            return False
    return True


def transpose_batch_time(x):
    """Transpose the batch and time dimensions of a Tensor.

    Retains as much of the static shape information as possible.

    Args:
        x: A tensor of rank 2 or higher.

    Returns:
        x transposed along the first two dimensions.

    Raises:
        ValueError: if `x` is rank 1 or lower.
    """
    x_static_shape = x.get_shape()
    if x_static_shape.ndims is not None and x_static_shape.ndims < 2:
        raise ValueError(
            "Expected input tensor %s to have rank at least 2, but saw shape: %s" %
            (x, x_static_shape))
    x_rank = array_ops.rank(x)
    x_t = array_ops.transpose(x, array_ops.concat(([1, 0], math_ops.range(2, x_rank)), axis=0))
    x_t.set_shape(tf.tensor_shape.TensorShape([
        x_static_shape[1].value, x_static_shape[0].value]).concatenate(x_static_shape[2:]))
    return x_t


def generate_model_dir():
    base_dir = '/tmp/polyaxon_logs/'
    return base_dir + uuid.uuid4().hex


def get_arguments(func):
    """Returns list of arguments this function has."""
    if hasattr(func, '__code__'):
        # Regular function.
        return inspect.getargspec(func).args
    elif hasattr(func, 'func'):
        # Partial function.
        return get_arguments(func.func)
    elif hasattr(func, '__call__'):
        # Callable object.
        return get_arguments(func.__call__)


def extract_batch_length(values):
    """Extracts batch length of values."""
    batch_length = None
    for key, value in six.iteritems(values):
        batch_length = batch_length or get_shape(value)[0]
        if value.shape[0] != batch_length:
            raise ValueError('Batch length of predictions should be same. %s has '
                             'different batch length then others.' % key)
    return batch_length


def get_tensor_batch_size(values):
    """Extracts batch size from tensor"""
    return tf.gather(params=tf.shape(input=values), indices=tf.constant([0]))


def total_tensor_depth(tensor=None, tensor_shape=None):
    """Returns the size of a tensor without the first (batch) dimension"""
    if tensor is None and tensor_shape is None:
        raise ValueError('a tensor or a tensor shape is required.')
    if tensor_shape:
        return int(np.prod(tensor_shape[1:]))
    return int(np.prod(get_shape(tensor)[1:]))


@contextlib.contextmanager
def new_attr_context(obj, attr):
    """Creates a new context in which an object's attribute can be changed.

    This creates a context in which an object's attribute can be changed.
    Once the context is exited, the attribute reverts to its original value.

    Args:
        obj: An object whose attribute to restore at the end of the context.
        attr: An attribute to remember and restore at the end of the context.

    Yields:
        Context.

    Example:
    ```python
    >>> my_obj.x = 1
    >>> with _new_attr_context(my_obj, "x"):
    >>>     my_obj.x = 2
    >>>     print(my_obj.x)
    >>> print(my_obj.x)
    ```
    """
    saved = getattr(obj, attr)
    try:
        yield
    finally:
        setattr(obj, attr, saved)


def get_function_name(func):
    """Returns a module name for a callable or `None` if no name can be found."""
    if isinstance(func, functools.partial):
        return get_function_name(func.func)

    try:
        name = func.__name__
    except AttributeError:
        return None

    return name


EPSILON = 1e-10
