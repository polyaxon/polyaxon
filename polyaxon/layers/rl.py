import tensorflow as tf

from polyaxon.layers import FullyConnected
from polyaxon.libs.template_module import BaseLayer


class DQN(BaseLayer):
    """Reshape.

    A layer that reshape the incoming layer tensor output to the desired shape.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        new_shape: A list of `int`. The desired shape.
        name: A name for this layer (optional).
    """
    def __init__(self, mode, name='DQN'):
        super(DQN, self).__init__(mode, name)

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: A `Tensor`. The incoming tensor.
        """
        return tf.reduce_max(incoming, axis=1)


class DDQN(BaseLayer):
    """Reshape.

    A layer that reshape the incoming layer tensor output to the desired shape.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        new_shape: A list of `int`. The desired shape.
        name: A name for this layer (optional).
    """
    def __init__(self, mode, name='DDQN'):
        super(DDQN, self).__init__(mode, name)

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: A `Tensor`. The incoming tensor.
        """
        action_probability = FullyConnected(self.mode, num_units=self.num_actions)(incoming)
        return tf.argmax(action_probability, axis=1)
