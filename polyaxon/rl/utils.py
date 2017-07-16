import tensorflow as tf

from tensorflow.python.platform import tf_logging as logging

from polyaxon.libs import getters
from polyaxon.variables import variable


def get_global_episode(graph=None):
    return get_global_counter(tf.GraphKeys.GLOBAL_EPISODE, 'global_episode:0', graph)


def get_or_create_global_episode(graph=None):
    return get_or_create_global_counter(tf.GraphKeys.GLOBAL_EPISODE, 'global_episode:0', graph)


def create_global_episode(graph=None):
    return create_global_counter(tf.GraphKeys.GLOBAL_EPISODE, 'global_episode:0', graph)


def get_global_timestep(graph=None):
    return get_global_counter(tf.GraphKeys.GLOBAL_TIMESTEP, 'global_timestep:0', graph)


def get_or_create_global_timestep(graph=None):
    return get_or_create_global_counter(tf.GraphKeys.GLOBAL_TIMESTEP, 'global_timestep:0', graph)


def create_global_timestep(graph=None):
    return create_global_counter(tf.GraphKeys.GLOBAL_TIMESTEP, 'global_timestep:0', graph)


def get_global_counter(collection, name, graph=None):
    """Get the global counter tensor.

    The global counter tensor must be an integer variable. We first try to find it
    in the collection, or by name.

    Args:
        collection: the counter's collection.
        name: the counter's name.
        graph: The graph to find the global counter in. If missing, use default graph.

    Returns:
        The global counter variable, or `None` if none was found.

    Raises:
        TypeError: If the global counter tensor has a non-integer type,
            or if it is not a `Variable`.
    """
    graph = graph or tf.get_default_graph()
    global_counter_tensors = graph.get_collection(collection)
    if len(global_counter_tensors) == 1:
        global_counter_tensor = global_counter_tensors[0]
    elif not global_counter_tensors:
        try:
            global_counter_tensor = graph.get_tensor_by_name(name)
        except KeyError:
            return None
    else:
        logging.error('Multiple tensors in `{}` collection.'.format(collection))
        return None

    assert_global_counter(global_counter_tensor)
    return global_counter_tensor


def get_or_create_global_counter(collection, name, graph=None):
    """Returns and create (if necessary) the global counter tensor.

    Args:
        collection: the counter's collection.
        name: the counter's name.
        graph: The graph in which to create the global counter tensor.
            If missing, use default graph.

    Returns:
        The global counter tensor.
    """
    graph = graph or tf.get_default_graph()
    global_counter_tensor = get_global_counter(collection, name, graph)
    if global_counter_tensor is None:
        global_counter_tensor = create_global_counter(collection, name, graph)
    return global_counter_tensor


def create_global_counter(collection, name, graph=None):
    """Create global counter tensor in graph.

    Args:
        collection: the counter's collection.
        name: the counter's name.
        graph: The graph in which to create the global counter tensor. If missing,
        use default graph.

    Returns:
        Global step tensor.

    Raises:
        ValueError: if global counter tensor is already defined.
    """
    graph = graph or tf.get_default_graph()
    if get_global_counter(collection, name, graph) is not None:
        raise ValueError("`{}` already exists.".format(collection))
    # Create in proper graph and base name_scope.
    with graph.as_default() as g, g.name_scope(None):
        return variable(
            collection,
            shape=[],
            dtype=tf.int64,
            initializer=getters.get_initializer('zeros', dtype=tf.int64),
            trainable=False,
            collections=[tf.GraphKeys.GLOBAL_VARIABLES, collection])


def assert_global_counter(global_counter_tensor):
    """Asserts `global_counter_tensor` is a scalar int `Variable` or `Tensor`.

    Args:
        global_counter_tensor: `Tensor` to test.
    """

    if not (isinstance(global_counter_tensor, tf.Variable) or
            isinstance(global_counter_tensor, tf.Tensor)):
        raise TypeError("Existing `global_counter` must be a Variable or "
                        "Tensor: {}.".format(global_counter_tensor))

    if not global_counter_tensor.dtype.base_dtype.is_integer:
        raise TypeError("Existing `global_counter` does not have "
                        "integer type: {}".format(global_counter_tensor.dtype))

    if global_counter_tensor.get_shape().ndims != 0:
        raise TypeError('Existing `global_counter` is not '
                        'scalar: {}'.format(global_counter_tensor.get_shape()))


def get_cumulative_rewards(reward, done,  discount=0.99):
    """compute cumulative rewards R(s,a) (a.k.a. G(s,a) in Sutton '16)

    `R_t = r_t + gamma*r_{t+1} + gamma^2*r_{t+2} + ...`

    The simple way to compute cumulative rewards is to iterate from last to first time tick
    and compute R_t = r_t + gamma*R_{t+1} recurrently

    Args:
        reward: `list`. A list of immediate rewards r(s,a) for the passed episodes.
        done: `list`. A list of terminal states for the passed episodes.
        discount: `float`. The discount factor.
    """
    if discount == 0:
        return reward

    cumulative_rewards = []
    cumulative_reward = 0

    for r, d in zip(reward[::-1], done[::-1]):
        if d:
            cumulative_reward = 0.0

        cumulative_reward = r + discount * cumulative_reward
        cumulative_rewards.insert(0, cumulative_reward)

    return cumulative_rewards
