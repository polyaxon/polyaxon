# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
import logging
import six

from six.moves import xrange

import numpy as np
import tensorflow as tf

import tensorflow.contrib.rnn as rnn
from tensorflow.python.ops import array_ops
from tensorflow.python.util import nest

from polyaxon.layers.core import Dropout
from polyaxon.layers.normalizations import BatchNormalization
from polyaxon.libs import getters
from polyaxon.libs.template_module import BaseLayer
from polyaxon.libs.utils import get_shape, get_variable_scope, track
from polyaxon.variables import variable


@six.add_metaclass(abc.ABCMeta)
class CoreRNN(BaseLayer):
    @property
    def w(self):
        return self._w

    @property
    def b(self):
        return self._b

    @staticmethod
    def _set_dropout(cell, mode, dropout):
        """Apply dropout to the outputs and inputs of `cell`."""
        if not dropout:
            return cell

        if type(dropout) in [tuple, list]:
            in_keep_prob, out_keep_prob = (1 - d for d in dropout)
        elif isinstance(dropout, float):
            in_keep_prob, out_keep_prob = 1 - dropout, 1 - dropout
        else:
            raise Exception('Invalid dropout type (must be a 2-D tuple of float)')
        return DropoutWrapper(mode, cell, in_keep_prob, out_keep_prob)

    @staticmethod
    def _stack_layers(cell_fn, mode, num_layers, state_is_tuple=True):
        """Stask multiple layers of the incoming cell."""
        if num_layers and num_layers > 1:
            return MultiRNNCell(mode, [cell_fn() for _ in xrange(num_layers)], state_is_tuple)

        return cell_fn()

    def _declare_dependencies(self):
        raise NotImplemented

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 3-D Tensor [samples, timesteps, input dim].
        """
        self._declare_dependencies()
        sequence_length = None
        if self.dynamic:
            sequence_length = retrieve_seq_length_op(
                incoming if isinstance(incoming, tf.Tensor) else tf.stack(incoming))

        input_shape = get_shape(incoming)

        inference = incoming
        # If a tensor given, convert it to a per timestep list
        if type(inference) not in [list, np.array]:
            ndim = len(input_shape)
            assert ndim >= 3, 'Input dim should be at least 3.'
            axes = [1, 0] + list(xrange(2, ndim))
            inference = tf.transpose(inference, (axes))
            inference = tf.unstack(value=inference)

        if self.dynamic:
            outputs, state = tf.nn.dynamic_rnn(
                cell=self._cell, inputs=inference, dtype=tf.float32,
                initial_state=self.initial_state, sequence_length=sequence_length,
                scope=self.module_name)
        else:
            outputs, state = rnn.static_rnn(
                cell=self._cell, inputs=inference, dtype=tf.float32,
                initial_state=self.initial_state, sequence_length=sequence_length,
                scope=self.module_name)

        for v in [self._cell.w, self._cell.b]:
            if hasattr(v, '__len__'):
                for var in v:
                    track(var, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
            else:
                track(v, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        track(outputs[-1], tf.GraphKeys.ACTIVATIONS, self.module_name)

        if self.dynamic:
            if self.return_seq:
                o = outputs
            else:
                outputs = tf.transpose(tf.stack(outputs), [1, 0, 2])
                o = advanced_indexing_op(outputs, sequence_length)
        else:
            o = outputs if self.return_seq else outputs[-1]

        track(o, tf.GraphKeys.LAYER_TENSOR, self.module_name)

        return (o, state) if self.return_state else o


class SimpleRNN(CoreRNN):
    """Simple RNN (Simple Recurrent Layer.)

    Output:
        if `return_seq`: 3-D Tensor [samples, timesteps, output dim].
        else: 2-D Tensor [samples, output dim].

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_units: `int`, number of units for this layer.
        activation: `str` (name) or `function` (returning a `Tensor`). Default: 'sigmoid'.
        dropout: `tuple` of `float`: (1 - input_keep_prob, 1 - output_keep_prob). The
            input and output keep probability.
        num_layers: `int` how many times to stack the cell.
        bias: `bool`. If True, a bias is used.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
        return_seq: `bool`. If True, returns the full sequence instead of
            last sequence output only.
        return_state: `bool`. If True, returns a tuple with output and
            states: (output, states).
        initial_state: `Tensor`. An initial state for the RNN.  This must be
            a tensor of appropriate type and shape [batch_size x cell.state_size].
        dynamic: `bool`. If True, dynamic computation is performed. It will not
            compute RNN steps above the sequence length. Note that because TF
            requires to feed sequences of same length, 0 is used as a mask.
            So a sequence padded with 0 at the end must be provided. When
            computation is performed, it will stop when it meets a step with
            a value of 0.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when loading a model.
        name: `str`. A name for this layer (optional).
    """
    def __init__(self, mode, num_units, activation='sigmoid', dropout=None, num_layers=1,
                 bias=True, weights_init=None, return_seq=False, return_state=False,
                 initial_state=None, dynamic=False, trainable=True,
                 restore=True, name='SimpleRNN'):
        super(SimpleRNN, self).__init__(mode, name)
        self.num_units = num_units
        self.activation = activation
        self.bias = bias
        self.weights_init = weights_init
        self.return_seq = return_seq
        self.return_state = return_state
        self.initial_state = initial_state
        self.dynamic = dynamic
        self.dropout = dropout
        self.num_layers = num_layers
        self.trainable = trainable
        self.restore = restore

    def _cell_fn(self):
        cell = BasicRNNCell(
            self.mode, num_units=self.num_units, activation=self.activation,
            bias=self.bias, weights_init=self.weights_init,
            trainable=self.trainable, restore=self.restore)
        return self._set_dropout(cell, self.mode, self.dropout)

    def _declare_dependencies(self):
        self._cell = self._stack_layers(self._cell_fn, self.mode, self.num_layers)


class LSTM(CoreRNN):
    """LSTM (Long Short Term Memory Recurrent Layer).

    Output:
        if `return_seq`: 3-D Tensor [samples, timesteps, output dim].
        else: 2-D Tensor [samples, output dim].

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_units: `int`, number of units for this layer.
        activation: `str` (name) or `function` (returning a `Tensor`). Default: 'tanh'.
        inner_activation: `str` (name) or `function` (returning a `Tensor`).
            LSTM inner activation. Default: 'sigmoid'.
        dropout: `tuple` of `float`: (1 - input_keep_prob, 1 - output_keep_prob). The
            input and output keep probability.
        num_layers: `int` how many times to stack the cell.
        bias: `bool`. If True, a bias is used.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
        forget_bias: `float`. Bias of the forget gate. Default: 1.0.
        return_seq: `bool`. If True, returns the full sequence instead of
            last sequence output only.
        return_state: `bool`. If True, returns a tuple with output and
            states: (output, states).
        initial_state: `Tensor`. An initial state for the RNN.  This must be
            a tensor of appropriate type and shape [batch_size x cell.state_size].
        dynamic: `bool`. If True, dynamic computation is performed. It will not
            compute RNN steps above the sequence length. Note that because TF
            requires to feed sequences of same length, 0 is used as a mask.
            So a sequence padded with 0 at the end must be provided. When
            computation is performed, it will stop when it meets a step with
            a value of 0.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when loading a model.
        name: `str`. A name for this layer (optional).

    References:
        Long Short Term Memory, Sepp Hochreiter & Jurgen Schmidhuber,
        Neural Computation 9(8): 1735-1780, 1997.

    Links:
        [http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf]
        (http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf)

    """
    def __init__(self, mode, num_units, activation='tanh', inner_activation='sigmoid', dropout=None,
                 num_layers=1, bias=True, weights_init=None, forget_bias=1.0, return_seq=False,
                 return_state=False, initial_state=None, dynamic=False, trainable=True,
                 restore=True, name='LSTM'):
        super(LSTM, self).__init__(mode, name)
        self.num_units = num_units
        self.activation = activation
        self.inner_activation = inner_activation
        self.bias = bias
        self.weights_init = weights_init
        self.forget_bias = forget_bias
        self.return_seq = return_seq
        self.return_state = return_state
        self.initial_state = initial_state
        self.dynamic = dynamic
        self.dropout = dropout
        self.num_layers = num_layers
        self.trainable = trainable
        self.restore = restore

    def _cell_fn(self):
        cell = BasicLSTMCell(
            self.mode, num_units=self.num_units, activation=self.activation,
            inner_activation=self.inner_activation, forget_bias=self.forget_bias,
            bias=self.bias, weights_init=self.weights_init, trainable=self.trainable,
            restore=self.restore)
        return self._set_dropout(cell, self.mode, self.dropout)

    def _declare_dependencies(self):
        self._cell = self._stack_layers(self._cell_fn, self.mode, self.num_layers)


class GRU(CoreRNN):
    """GRU (Gated Recurrent Unit Layer).

    Output:
        if `return_seq`: 3-D Tensor [samples, timesteps, output dim].
        else: 2-D Tensor [samples, output dim].

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_units: `int`, number of units for this layer.
        activation: `str` (name) or `function` (returning a `Tensor`). Default: 'tanh'.
        inner_activation: `str` (name) or `function` (returning a `Tensor`).
            GRU inner activation. Default: 'sigmoid'.
        dropout: `tuple` of `float`: (1 - input_keep_prob, 1 - output_keep_prob). The
            input and output keep probability.
        num_layers: `int` how many times to stack the cell.
        bias: `bool`. If True, a bias is used.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
        return_seq: `bool`. If True, returns the full sequence instead of
            last sequence output only.
        return_state: `bool`. If True, returns a tuple with output and
            states: (output, states).
        initial_state: `Tensor`. An initial state for the RNN.  This must be
            a tensor of appropriate type and shape [batch_size x cell.state_size].
        dynamic: `bool`. If True, dynamic computation is performed. It will not
            compute RNN steps above the sequence length. Note that because TF
            requires to feed sequences of same length, 0 is used as a mask.
            So a sequence padded with 0 at the end must be provided. When
            computation is performed, it will stop when it meets a step with
            a value of 0.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when loading a model.
        name: `str`. A name for this layer (optional).

    References:
        Learning Phrase Representations using RNN Encoder–Decoder for
        Statistical Machine Translation, K. Cho et al., 2014.

    Links:
        [http://arxiv.org/abs/1406.1078](http://arxiv.org/abs/1406.1078)

    """
    def __init__(self, mode, num_units, activation='tanh', inner_activation='sigmoid',
                 dropout=None, num_layers=1, bias=True, weights_init=None, return_seq=False,
                 return_state=False, initial_state=None, dynamic=False,
                 trainable=True, restore=True, name='GRU'):
        super(GRU, self).__init__(mode, name)
        self.num_units = num_units
        self.activation = activation
        self.inner_activation = inner_activation
        self.bias = bias
        self.weights_init = weights_init
        self.return_seq = return_seq
        self.return_state = return_state
        self.initial_state = initial_state
        self.dynamic = dynamic
        self.dropout = dropout
        self.num_layers = num_layers
        self.trainable = trainable
        self.restore = restore

    def _cell_fn(self):
        cell = GRUCell(
            self.mode, num_units=self.num_units, activation=self.activation,
            inner_activation=self.inner_activation, bias=self.bias, weights_init=self.weights_init,
            trainable=self.trainable, restore=self.restore)
        return self._set_dropout(cell, self.mode, self.dropout)

    def _declare_dependencies(self):
        self._cell = self._stack_layers(self._cell_fn, self.mode, self.num_layers)


class BidirectionalRNN(BaseLayer):
    """Bidirectional RNN.

    Build a bidirectional recurrent neural network, it requires 2 RNN Cells
    to process sequence in forward and backward order. Any RNN Cell can be
    used i.e. SimpleRNN, LSTM, GRU... with its own parameters. But the two
    cells number of units must match.

    Output:
        if `return_seq`: 3-D Tensor [samples, timesteps, output dim].
        else: 2-D Tensor Layer [samples, output dim].

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        rnncell_fw: `RNNCell`. The RNN Cell to use for foward computation.
        rnncell_bw: `RNNCell`. The RNN Cell to use for backward computation.
        return_seq: `bool`. If True, returns the full sequence instead of
            last sequence output only.
        return_states: `bool`. If True, returns a tuple with output and
            states: (output, states).
        initial_state_fw: `Tensor`. An initial state for the forward RNN.
            This must be a tensor of appropriate type and shape [batch_size
            x cell.state_size].
        initial_state_bw: `Tensor`. An initial state for the backward RNN.
            This must be a tensor of appropriate type and shape [batch_size
            x cell.state_size].
        dynamic: `bool`. If True, dynamic computation is performed. It will not
            compute RNN steps above the sequence length. Note that because TF
            requires to feed sequences of same length, 0 is used as a mask.
            So a sequence padded with 0 at the end must be provided. When
            computation is performed, it will stop when it meets a step with
            a value of 0.
        name: `str`. A name for this layer (optional).

    """
    def __init__(self, mode, rnncell_fw, rnncell_bw, return_seq=False, return_states=False,
                 initial_state_fw=None, initial_state_bw=None, dynamic=False, name='BiRNN'):
        super(BidirectionalRNN, self).__init__(mode, name)
        self.rnncell_fw = rnncell_fw
        self.rnncell_bw = rnncell_bw
        self.return_seq = return_seq
        self.return_states = return_states
        self.initial_state_fw = initial_state_fw
        self.initial_state_bw = initial_state_bw
        self.dynamic = dynamic

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            incoming: `Tensor`. 3-D Tensor Layer [samples, timesteps, input dim].
        """
        assert (self.rnncell_fw.output_size ==
                self.rnncell_bw.output_size), "RNN Cells number of units must match!"
        input_shape = get_shape(incoming)

        # TODO: DropoutWrapper

        inference = incoming
        # If a tensor given, convert it to a per timestep list
        if type(inference) not in [list, np.array]:
            ndim = len(input_shape)
            assert ndim >= 3, 'Input dim should be at least 3.'
            axes = [1, 0] + list(xrange(2, ndim))
            inference = tf.transpose(inference, (axes,))
            inference = tf.unstack(inference)

        sequence_length = None
        if self.dynamic:
            sequence_length = retrieve_seq_length_op(
                incoming if isinstance(incoming, tf.Tensor) else tf.stack(incoming))
            outputs, states_fw, states_bw = tf.nn.bidirectional_dynamic_rnn(
                cell_fw=self.rnncell_fw, cell_bw=self.rnncell_bw, inputs=inference,
                initial_state_fw=self.initial_state_fw,
                initial_state_bw=self.initial_state_bw,
                sequence_length=sequence_length,
                dtype=tf.float32)
        else:
            outputs, states_fw, states_bw = rnn.static_bidirectional_rnn(
                cell_fw=self.rnncell_fw, cell_bw=self.rnncell_bw, inputs=inference,
                initial_state_fw=self.initial_state_fw,
                initial_state_bw=self.initial_state_bw,
                dtype=tf.float32)

        for v in [self.rnncell_fw.w, self.rnncell_fw.b, self.rnncell_bw.w, self.rnncell_bw.b]:
            if hasattr(v, '__len__'):
                for var in v:
                    track(var, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
            else:
                track(v, tf.GraphKeys.LAYER_VARIABLES, self.module_name)

        tf.add_to_collection(tf.GraphKeys.ACTIVATIONS, outputs[-1])

        if self.dynamic:
            if self.return_seq:
                o = outputs
            else:
                outputs = tf.transpose(tf.stack(outputs), [1, 0, 2])
                o = advanced_indexing_op(outputs, sequence_length)
        else:
            o = outputs if self.return_seq else outputs[-1]

        track(o, tf.GraphKeys.LAYER_TENSOR, self.module_name)

        return (o, states_fw, states_bw) if self.return_states else o


@six.add_metaclass(abc.ABCMeta)
class CoreRNNCell(BaseLayer, rnn.RNNCell):
    @property
    def w(self):
        return self._w

    @property
    def b(self):
        return self._b

    def _build(self, incoming, state, *args, **kwargs):
        """Subclasses should implement their logic here."""
        raise NotImplementedError


class BasicRNNCell(CoreRNNCell):
    """The most basic RNN cell with custom params.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_units: `int`, number of units for this layer.
        activation: `str` (name) or `function` (returning a `Tensor`). Default: 'tanh'.
        bias: `bool`. If True, a bias is used.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when loading a model.
        name: `str`. A name for this layer (optional).
    """

    def __init__(self, mode, num_units, activation='tanh', bias=True, weights_init=None,
                 trainable=True, restore=True, name='BasicRNNCell'):
        super(BasicRNNCell, self).__init__(mode, name)
        self.num_units = num_units
        self.activation = activation
        self.bias = bias
        self.weights_init = weights_init
        self.trainable = trainable
        self.restore = restore

    @property
    def state_size(self):
        return self._num_units

    @property
    def output_size(self):
        return self._num_units

    def _build(self, inputs, state, *args, **kwargs):
        """Most basic RNN: output = new_state = activation(W * input + U * state + B)."""
        weights_init = getters.get_initializer(self.weights_init)
        output = getters.get_activation(self.activation)(
            _linear([inputs, state], self.num_units, True, 0.,
                    weights_init, self.trainable, self.restore))
        # Retrieve RNN Variables
        with get_variable_scope(name='Linear', reuse=True):
            self._w = tf.get_variable(name='w')
            self._b = tf.get_variable(name='b')

        return output, output


class GRUCell(CoreRNNCell):
    """Gated Recurrent Unit cell with custom params.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_units: `int`, number of units for this layer.
        activation: `str` (name) or `function` (returning a `Tensor`). Default: 'tanh'.
        inner_activation: `str` (name) or `function` (returning a `Tensor`).
            GRU inner activation. Default: 'sigmoid'.
        bias: `bool`. If True, a bias is used.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when loading a model.
        name: `str`. A name for this layer (optional).
    """

    def __init__(self, mode, num_units, activation='tanh', inner_activation='sigmoid', bias=True,
                 weights_init=None, trainable=True, restore=True, name='GRUCell'):
        super(GRUCell, self).__init__(mode, name)
        self._num_units = num_units
        self.activation = activation
        self.inner_activation = inner_activation
        self.bias = bias
        self.weights_init = weights_init
        self.trainable = trainable
        self.restore = restore

    @property
    def state_size(self):
        return self._num_units

    @property
    def output_size(self):
        return self._num_units

    def _build(self, incoming, state, *args, **kwargs):
        """Gated recurrent unit (GRU) with nunits cells."""
        with get_variable_scope('Gates'):  # Reset gate and update gate.
            weights_init = getters.get_initializer(self.weights_init)
            # We start with bias of 1.0 to not reset and not update.
            r, u = array_ops.split(
                axis=1, num_or_size_splits=2,
                value=_linear([incoming, state], 2 * self._num_units, True, 1.0,
                              weights_init, self.trainable, self.restore))
            inner_activation = getters.get_activation(self.inner_activation)
            r, u = inner_activation(r), inner_activation(u)
        with get_variable_scope('Candidate'):
            activation = getters.get_activation(self.activation)
            c = activation(
                _linear([incoming, r * state], self._num_units, True, 0.,
                        weights_init, self.trainable, self.restore))
        new_h = u * state + (1 - u) * c

        self._w, self._b = list(), list()
        # Retrieve RNN Variables
        with get_variable_scope(scope='Gates/Linear', reuse=True):
            self._w.append(x=tf.get_variable('w'))
            self._b.append(x=tf.get_variable('b'))
        with get_variable_scope(scope='Candidate/Linear', reuse=True):
            self._w.append(x=tf.get_variable('w'))
            self._b.append(x=tf.get_variable('b'))

        return new_h, new_h


class BasicLSTMCell(CoreRNNCell):
    """Basic LSTM recurrent network cell with custo\m params.

    The implementation is based on: http://arxiv.org/abs/1409.2329.

    We add forget_bias (default: 1) to the biases of the forget gate in order to
    reduce the scale of forgetting in the beginning of the training.

    It does not allow cell clipping, a projection layer, and does not
    use peep-hole connections: it is the basic baseline.

    For advanced models, please use the full LSTMCell that follows.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        num_units: `int`, number of units for this layer.
        forget_bias: `float`. Bias of the forget gate. Default: 1.0.
        state_is_tuple: If True, accepted and returned states are n-tuples, where
            `n = len(cells)`.  If False, the states are all
            concatenated along the column axis.  This latter behavior will soon be
            deprecated.
        activation: `str` (name) or `function` (returning a `Tensor`). Default: 'tanh'.
        inner_activation: `str` (name) or `function` (returning a `Tensor`).
            GRU inner activation. Default: 'sigmoid'.
        bias: `bool`. If True, a bias is used.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
        batch_norm: `bool`. If True, use batch normalization for this cell.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when loading a model.
        name: `str`. A name for this layer (optional).
    """

    def __init__(self, mode, num_units, forget_bias=1.0, state_is_tuple=True, activation='tanh',
                 inner_activation='sigmoid', bias=True, weights_init=None,
                 batch_norm=False, trainable=True, restore=True, name='BasicLSTMCell'):
        super(BasicLSTMCell, self).__init__(mode, name)
        if not state_is_tuple:
            logging.warning(
                '{}: Using a concatenated state is slower and will soon be '
                'deprecated.  Use state_is_tuple=True.'.format(self))
        self._num_units = num_units
        self._forget_bias = forget_bias
        self._state_is_tuple = state_is_tuple
        self.batch_norm = batch_norm
        self.activation = activation
        self.inner_activation = inner_activation
        self.bias = bias
        self.weights_init = getters.get_initializer(weights_init)
        self.trainable = trainable
        self.restore = restore

    def _declare_dependencies(self):
        self._batch_norm_i = BatchNormalization(self.mode, gamma=0.1, trainable=self.trainable,
                                                restore=self.restore)
        self._batch_norm_j = BatchNormalization(self.mode, gamma=0.1, trainable=self.trainable,
                                                restore=self.restore)
        self._batch_norm_f = BatchNormalization(self.mode, gamma=0.1, trainable=self.trainable,
                                                restore=self.restore)
        self._batch_norm_o = BatchNormalization(self.mode, gamma=0.1, trainable=self.trainable,
                                                restore=self.restore)
        self._batch_norm_c = None
        if self.batch_norm:
            self._batch_norm_c = BatchNormalization(self.mode, gamma=0.1, trainable=self.trainable,
                                                    restore=self.restore)

    @property
    def state_size(self):
        return (rnn.LSTMStateTuple(self._num_units, self._num_units)
                if self._state_is_tuple else 2 * self._num_units)

    @property
    def output_size(self):
        return self._num_units

    def _build(self, incoming, state, *args, **kwargs):
        """Long short-term memory cell (LSTM)."""
        self._declare_dependencies()
        activation = getters.get_activation(self.activation)
        inner_activation = getters.get_activation(self.inner_activation)
        # Parameters of gates are concatenated into one multiply for efficiency.
        if self._state_is_tuple:
            c, h = state
        else:
            c, h = array_ops.split(axis=1, num_or_size_splits=2, value=state)
        concat = _linear(
            [incoming, h], 4 * self._num_units, True, 0., self.weights_init,
            self.trainable, self.restore)

        # i = input_gate, j = new_input, f = forget_gate, o = output_gate
        i, j, f, o = array_ops.split(axis=1, num_or_size_splits=4, value=concat)

        # apply batch normalization to inner state and gates
        if self.batch_norm:
            i = self._batch_norm_i(i)
            j = self._batch_norm_j(j)
            f = self._batch_norm_f(f)
            o = self._batch_norm_o(o)

        new_c = (c * inner_activation(f + self._forget_bias) + inner_activation(i) * activation(j))

        # hidden-to-hidden batch normalizaiton
        if self.batch_norm:
            batch_norm_new_c = self._batch_norm_c(new_c)
            new_h = activation(batch_norm_new_c) * inner_activation(o)
        else:
            new_h = activation(new_c) * inner_activation(o)

        if self._state_is_tuple:
            new_state = rnn.LSTMStateTuple(new_c, new_h)
        else:
            new_state = tf.concat(values=[new_c, new_h], axis=1)

        # Retrieve RNN Variables
        with get_variable_scope(scope='Linear', reuse=True):
            self._w = tf.get_variable('w')
            self._b = tf.get_variable('b')

        return new_h, new_state


class DropoutWrapper(CoreRNNCell):
    """Operator adding dropout to inputs and outputs of the given cell.

    Creates a cell with added input and/or output dropout.

    Dropout is never used on the state.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        cell: an RNNCell, a projection to output_size is added to it.
        input_keep_prob: unit Tensor or float between 0 and 1, input keep probability;
            if it is float and 1, no input dropout will be added.
        output_keep_prob: unit Tensor or float between 0 and 1, output keep
        probability; if it is float and 1, no output dropout will be added.
        seed: (optional) integer, the randomness seed.

    Raises:
      TypeError: if cell is not an RNNCell.
      ValueError: if keep_prob is not between 0 and 1.
    """

    def __init__(self, mode, cell, input_keep_prob=1.0, output_keep_prob=1.0, seed=None,
                 name='DropoutWrapper'):
        super(DropoutWrapper, self).__init__(mode, name)
        if not isinstance(cell, CoreRNNCell):
            raise TypeError("The parameter cell is not a RNNCell.")
        if isinstance(input_keep_prob, float) and not (0.0 <= input_keep_prob <= 1.0):
            raise ValueError(
                'Parameter input_keep_prob must be between 0 and 1: {}'.format(input_keep_prob))
        if isinstance(output_keep_prob, float) and not (0.0 <= output_keep_prob <= 1.0):
            raise ValueError(
                'Parameter output_keep_prob must be between 0 and 1: {}'.format(output_keep_prob))
        self._cell = cell
        self._input_keep_prob = input_keep_prob
        self._output_keep_prob = output_keep_prob
        self._seed = seed

    def _declare_dependencies(self):
        self._inputs_dropout = None
        if not isinstance(self._input_keep_prob, float) or self._input_keep_prob < 1:
            self._inputs_dropout = Dropout(self.mode, self._input_keep_prob, seed=self._seed)
        self._outputs_dropout = None
        if not isinstance(self._input_keep_prob, float) or self._input_keep_prob < 1:
            self._outputs_dropout = Dropout(self.mode, self._output_keep_prob, seed=self._seed)

    @property
    def state_size(self):
        return self._cell.state_size

    @property
    def output_size(self):
        return self._cell.output_size

    @property
    def w(self):
        return self._cell.w

    @property
    def b(self):
        return self._cell.b

    def _build(self, incoming, state, *args, **kwargs):
        """Run the cell with the declared dropouts."""
        self._declare_dependencies()
        if self._inputs_dropout:
            incoming = self._inputs_dropout(incoming)
        output, new_state = self._cell(incoming, state)
        if self._outputs_dropout:
            output = self._outputs_dropout(output, self._output_keep_prob, seed=self._seed)
        return output, new_state


class MultiRNNCell(CoreRNNCell):
    """RNN cell composed sequentially of multiple simple cells.

    Create a RNN cell composed sequentially of a number of RNNCells.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        cells: list of RNNCells that will be composed in this order.
        state_is_tuple: If True, accepted and returned states are n-tuples, where
            `n = len(cells)`.  If False, the states are all
            concatenated along the column axis.  This latter behavior will soon be
            deprecated.

    Raises:
        ValueError: if cells is empty (not allowed), or at least one of the cells
            returns a state tuple but the flag `state_is_tuple` is `False`.
    """

    def __init__(self, mode, cells, state_is_tuple=True, name='MultiRNNCell'):
        super(MultiRNNCell, self).__init__(mode, name)
        if not cells:
            raise ValueError("Must specify at least one cell for MultiRNNCell.")
        for cell in cells:
            if not isinstance(cell, CoreRNNCell):
                raise TypeError("The parameter cells: one cell is not a RNNCell.")
        self._cells = cells
        self._state_is_tuple = state_is_tuple
        if not state_is_tuple:
            if any(nest.is_sequence(c.state_size) for c in self._cells):
                raise ValueError("Some cells return tuples of states, but the flag "
                                 "state_is_tuple is not set.  State sizes are: %s"
                                 % str([c.state_size for c in self._cells]))

    @property
    def w(self):
        return [cell.w for cell in self._cells]

    @property
    def b(self):
        return [cell.b for cell in self._cells]

    @property
    def state_size(self):
        if self._state_is_tuple:
            return tuple(cell.state_size for cell in self._cells)
        else:
            return sum([cell.state_size for cell in self._cells])

    @property
    def output_size(self):
        return self._cells[-1].output_size

    def _build(self, incoming, state, *args, **kwargs):
        """Run this multi-layer cell on inputs, starting from state."""
        cur_state_pos = 0
        cur_inp = incoming
        new_states = []
        for i, cell in enumerate(self._cells):
            with get_variable_scope("cell_{}".format(i)):
                if self._state_is_tuple:
                    if not nest.is_sequence(state):
                        raise ValueError(
                            "Expected state to be a tuple of length %d, but received: {}".format(
                                len(self.state_size), state))
                    cur_state = state[i]
                else:
                    cur_state = array_ops.slice(state, [0, cur_state_pos], [-1, cell.state_size])
                    cur_state_pos += cell.state_size
                cur_inp, new_state = cell(cur_inp, cur_state)
                new_states.append(new_state)
        new_states = (tuple(new_states) if self._state_is_tuple else
                      array_ops.concat(values=new_states, axis=1))
        return cur_inp, new_states


def _linear(args, output_size, bias, bias_start=0.0, weights_init=None,
            trainable=True, restore=True, scope=None):
    """Linear map: sum_i(args[i] * W[i]), where W[i] is a variable.

    Args:
        args: a 2D Tensor or a list of 2D, batch x n, Tensors.
        output_size: int, second dimension of W[i].
        bias: boolean, whether to add a bias term or not.
        bias_start: starting value to initialize the bias; 0 by default.
        scope: VariableScope for the created subgraph; defaults to "Linear".

    Returns:
        A 2D Tensor with shape [batch x output_size] equal to
        sum_i(args[i] * W[i]), where W[i]s are newly created matrices.

    Raises:
        ValueError: if some of the arguments has unspecified or wrong shape.
    """
    if args is None or (nest.is_sequence(args) and not args):
        raise ValueError('`args` must be specified')
    if not nest.is_sequence(args):
        args = [args]

    # Calculate the total size of arguments on dimension 1.
    total_arg_size = 0
    shapes = [a.get_shape().as_list() for a in args]
    for shape in shapes:
        if len(shape) != 2:
            raise ValueError('Linear is expecting 2D arguments: %s' % str(shapes))
        if not shape[1]:
            raise ValueError('Linear expects shape[1] of arguments: %s' % str(shapes))
        else:
            total_arg_size += shape[1]

    # Now the computation.
    with get_variable_scope(scope or 'Linear'):
        _w = variable(name='w', shape=[total_arg_size, output_size], initializer=weights_init,
                      trainable=trainable, restore=restore)
        if len(args) == 1:
            res = tf.matmul(a=args[0], b=_w)
        else:
            res = tf.matmul(a=array_ops.concat(values=args, axis=1), b=_w)
        if not bias:
            return res
        _b = variable(name='b', shape=[output_size],
                      initializer=tf.constant_initializer(bias_start),
                      trainable=trainable, restore=restore)
    return res + _b


def retrieve_seq_length_op(data):
    """An op to compute the length of a sequence. 0 are masked. """
    with tf.name_scope('GetLength'):
        used = tf.sign(x=tf.reduce_max(tf.abs(data), axis=2))
        length = tf.reduce_sum(input_tensor=used, axis=1)
        length = tf.cast(x=length, dtype=tf.int32)
    return length


def advanced_indexing_op(input, index):
    """Advanced Indexing for Sequences. """
    batch_size = get_shape(input)[0]
    max_length = int(input.get_shape()[1])
    dim_size = int(input.get_shape()[2])
    index = tf.range(0, batch_size) * max_length + (index - 1)
    flat = tf.reshape(input, [-1, dim_size])
    relevant = tf.gather(flat, index)
    return relevant
