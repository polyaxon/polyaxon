# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np

import collections
from tensorflow.python.estimator.inputs.queues import feeding_functions

try:
    # pylint: disable=g-import-not-at-top
    # pylint: disable=unused-import
    import pandas as pd

    HAS_PANDAS = True
except IOError:
    # Pandas writes a temporary file during import. If it fails, don't use pandas.
    HAS_PANDAS = False
except ImportError:
    HAS_PANDAS = False

# Key name to pack the target into dict of `features`. See
# `_get_unique_target_key` for details.
_TARGET_KEY = '__target_key__'


def _get_unique_target_key(features):
    """Returns a key not existed in the input dict `features`.

    Caller of `input_fn` usually provides `features` (dict of numpy arrays) and
    `target`, but the underlying feeding module expects a single dict of numpy
    arrays as input. So, the `target` needs to be packed into the `features`
    temporarily and unpacked after calling the feeding function. Toward this goal,
    this function returns a key not existed in the `features` to pack the
    `target`.
    """
    target_key = _TARGET_KEY
    while target_key in features:
        target_key += '_n'
    return target_key


def numpy_input_fn(x,
                   y=None,
                   batch_size=128,
                   num_epochs=1,
                   shuffle=None,
                   queue_capacity=1000,
                   num_threads=1):
    """This is required here, until the upgrade of tensorflow to 1.2.

    Returns input function that would feed dict of numpy arrays into the model.

    This returns a function outputting `features` and `target` based on the dict
    of numpy arrays. The dict `features` has the same keys as the `x`.

    Example:
    ```python
    age = np.arange(4) * 1.0
    height = np.arange(32, 36)
    x = {'age': age, 'height': height}
    y = np.arange(-32, -28)

    with tf.Session() as session:
        input_fn = numpy_io.numpy_input_fn(
            x, y, batch_size=2, shuffle=False, num_epochs=1)
    ```

    Args:
        x: dict of numpy array object.
        y: numpy array object. `None` if absent.
        batch_size: Integer, size of batches to return.
        num_epochs: Integer, number of epochs to iterate over data. If `None` will
            run forever.
        shuffle: Boolean, if True shuffles the queue. Avoid shuffle at prediction
            time.
        queue_capacity: Integer, size of queue to accumulate.
        num_threads: Integer, number of threads used for reading and enqueueing. In
            order to have predicted and repeatable order of reading and enqueueing,
            such as in prediction and evaluation mode, `num_threads` should be 1.

    Returns:
        Function, that has signature of ()->(dict of `features`, `target`)

    Raises:
        ValueError: if the shape of `y` mismatches the shape of values in `x` (i.e.,
            values in `x` have same shape).
        TypeError: `x` is not a dict or `shuffle` is not bool.
    """

    if not isinstance(shuffle, bool):
        raise TypeError('shuffle must be explicitly set as boolean; '
                        'got {}'.format(shuffle))

    def input_fn():
        """Numpy input function."""
        if not isinstance(x, dict):
            raise TypeError('x must be dict; got {}'.format(type(x).__name__))

        # Make a shadow copy and also ensure the order of iteration is consistent.
        ordered_dict_x = collections.OrderedDict(
            sorted(x.items(), key=lambda t: t[0]))

        unique_target_key = _get_unique_target_key(ordered_dict_x)
        if y is not None:
            ordered_dict_x[unique_target_key] = y

        if len(set(v.shape[0] for v in ordered_dict_x.values())) != 1:
            shape_dict_of_x = {k: ordered_dict_x[k].shape
                               for k in ordered_dict_x.keys()}
            shape_of_y = None if y is None else y.shape
            raise ValueError('Length of tensors in x and y is mismatched. All '
                             'elements in x and y must have the same length.\n'
                             'Shapes in x: {}\n'
                             'Shape for y: {}\n'.format(shape_dict_of_x, shape_of_y))

        queue = feeding_functions._enqueue_data(  # pylint: disable=protected-access
            ordered_dict_x,
            queue_capacity,
            shuffle=shuffle,
            num_threads=num_threads,
            enqueue_size=batch_size,
            num_epochs=num_epochs)

        features = (queue.dequeue_many(batch_size) if num_epochs is None
                    else queue.dequeue_up_to(batch_size))

        # Remove the first `Tensor` in `features`, which is the row number.
        if len(features) > 0:
            features.pop(0)

        features = dict(zip(ordered_dict_x.keys(), features))
        if y is not None:
            target = features.pop(unique_target_key)
            return features, target
        return features

    return input_fn


def pandas_input_fn(x,
                    y=None,
                    batch_size=128,
                    num_epochs=1,
                    shuffle=None,
                    queue_capacity=1000,
                    num_threads=1,
                    target_column='target'):
    """This is required here, until the upgrade of tensorflow to 1.2.

    Returns input function that would feed Pandas DataFrame into the model.

    Note: `y`'s index must match `x`'s index.

    Args:
        x: pandas `DataFrame` object.
        y: pandas `Series` object. `None` if absent.
        batch_size: int, size of batches to return.
        num_epochs: int, number of epochs to iterate over data. If not `None`,
            read attempts that would exceed this value will raise `OutOfRangeError`.
        shuffle: bool, whether to read the records in random order.
        queue_capacity: int, size of the read queue. If `None`, it will be set
            roughly to the size of `x`.
        num_threads: Integer, number of threads used for reading and enqueueing. In
            order to have predicted and repeatable order of reading and enqueueing,
            such as in prediction and evaluation mode, `num_threads` should be 1.
        target_column: str, name to give the target column `y`.

    Returns:
        Function, that has signature of ()->(dict of `features`, `target`)

    Raises:
        ValueError: if `x` already contains a column with the same name as `y`, or
            if the indexes of `x` and `y` don't match.
        TypeError: `shuffle` is not bool.
    """
    if not HAS_PANDAS:
        raise TypeError(
            'pandas_input_fn should not be called without pandas installed')

    if not isinstance(shuffle, bool):
        raise TypeError('shuffle must be explicitly set as boolean; '
                        'got {}'.format(shuffle))

    x = x.copy()
    if y is not None:
        if target_column in x:
            raise ValueError(
                'Cannot use name %s for target column: DataFrame already has a '
                'column with that name: %s' % (target_column, x.columns))
        if not np.array_equal(x.index, y.index):
            raise ValueError('Index for x and y are mismatched.\nIndex for x: %s\n'
                             'Index for y: %s\n' % (x.index, y.index))
        x[target_column] = y

    # TODO(mdan): These are memory copies. We probably don't need 4x slack space.
    # The sizes below are consistent with what I've seen elsewhere.
    if queue_capacity is None:
        if shuffle:
            queue_capacity = 4 * len(x)
        else:
            queue_capacity = len(x)
    min_after_dequeue = max(queue_capacity / 4, 1)

    def input_fn():
        """Pandas input function."""
        queue = feeding_functions._enqueue_data(  # pylint: disable=protected-access
            x,
            queue_capacity,
            shuffle=shuffle,
            min_after_dequeue=min_after_dequeue,
            num_threads=num_threads,
            enqueue_size=batch_size,
            num_epochs=num_epochs)
        if num_epochs is None:
            features = queue.dequeue_many(batch_size)
        else:
            features = queue.dequeue_up_to(batch_size)
        assert len(features) == len(x.columns) + 1, ('Features should have one '
                                                     'extra element for the index.')
        features = features[1:]
        features = dict(zip(list(x.columns), features))
        if y is not None:
            target = features.pop(target_column)
            return features, target
        return features

    return input_fn
