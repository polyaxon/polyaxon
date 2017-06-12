# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

import tensorflow as tf

from tensorflow.python.estimator.model_fn import EstimatorSpec

from polyaxon import ModeKeys
from polyaxon.libs import getters
from polyaxon.libs.configs import OptimizerConfig, LossConfig
from polyaxon.libs.dicts import flatten_dict
from polyaxon.libs.utils import get_tracked, get_arguments, track
from polyaxon.models.base import BaseModel
from polyaxon.models.bridges import BridgeSpec, NoOpBridge


class Generator(BaseModel):
    """Generator base model.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
        encoder_fn: Encoder Graph function. Follows the signature:
            * Args:
                * `mode`: Specifies if this training, evaluation or prediction. See `ModeKeys`.
                * `inputs`: the feature inputs.
        decoder_fn: Decoder Graph function. Follows the signature:
            * Args:
                * `mode`: Specifies if this training, evaluation or prediction. See `ModeKeys`.
                * `inputs`: the feature inputs.
        bridge_fn: The bridge to use. Follows the signature:
            * Args:
                * `mode`: Specifies if this training, evaluation or prediction. See `ModeKeys`.
                * `inputs`: the feature inputs.
                * `encoder_fn`: the encoder function.
                * `decoder_fn` the decoder function.
        loss_config: An instance of `LossConfig`. Default value `mean_squared_error`.
        optimizer_config: An instance of `OptimizerConfig`. Default value `Adadelta`.
        summaries: `str` or `list`. The verbosity of the tensorboard visualization.
            Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
        name: `str`, the name of this model, everything will be encapsulated inside this scope.

    Returns:
        `EstimatorSpec`
    """

    def __init__(self, mode, encoder_fn, decoder_fn, bridge_fn, loss_config=None,
                 optimizer_config=None, summaries='all', eval_metrics_config=None,
                 clip_gradients=0.5, name="Generator"):
        optimizer_config = optimizer_config or OptimizerConfig('adadelta', learning_rate=0.4)
        loss_config = loss_config or LossConfig(module='mean_squared_error')
        self._check_subgraph_fn(function=encoder_fn, function_name='encoder_fn')
        self._check_subgraph_fn(function=decoder_fn, function_name='decoder_fn')
        self._check_bridge_fn(function=bridge_fn)
        self._encode_fn = encoder_fn
        self._decoder_fn = decoder_fn
        self._bridge_fn = bridge_fn

        graph_fn = self._build_graph_fn()

        super(Generator, self).__init__(
            mode=mode, name=name, model_type=self.Types.GENERATOR, graph_fn=graph_fn,
            loss_config=loss_config, optimizer_config=optimizer_config,
            eval_metrics_config=eval_metrics_config, summaries=summaries,
            clip_gradients=clip_gradients)

    @staticmethod
    def _check_bridge_fn(function):
        if function is not None:
            # Check number of arguments of the given function matches requirements.
            model_fn_args = get_arguments(function)
            if ('mode' not in model_fn_args or
                    'inputs' not in model_fn_args or
                    'encoder_fn' not in model_fn_args or
                    'encoder_fn' not in model_fn_args):
                raise ValueError(
                    "Model's `bridge` `{}` should have 4 args: "
                    "`mode`, `inputs`, `encoder_fn`, and `decoder_fn`.".format(function))
        else:
            raise ValueError("`bridge_fn` must be provided to Model.")

    def _build_graph_fn(self):
        """Creates a graph_fn for the auto encoder based on the encoder/decoder functions.

        Returns:
            `function` with args: `mode`, `inputs`.
        """

        def graph_fn(mode, inputs):
            return self._bridge_fn(
                mode=mode, inputs=inputs, encoder_fn=self._encode_fn, decoder_fn=self._decoder_fn)

        return graph_fn

    def _build_loss(self, results, features, labels):
        """Creates the loss operation

        Returns:
             tuple `(losses, loss)`:
                `losses` are the per-batch losses.
                `loss` is a single scalar tensor to minimize.
        """
        losses, loss = getters.get_loss(
            self.loss_config.module, results.results, labels, **self.loss_config.params)
        if results.loss:
            loss += results.loss
        if results.losses:
            losses += results.losses
        self._loss = loss
        self._losses = losses

        other_losses = get_tracked(tf.GraphKeys.REGULARIZATION_LOSSES)
        if other_losses:
            loss = [loss] + other_losses
            loss = tf.add_n(loss, name="TotalLoss")
            self._total_loss = loss
        return losses, loss

    def _preprocess(self, mode, features, labels=None):
        if isinstance(features, Mapping):
            if len(features) > 1:
                raise ValueError("Autoencoder accept only one feature value, "
                                 "received a dict of `{}` instead".format(list(features.keys())))
            features = list(features.values())[0]
        return super(Generator, self)._preprocess(mode, features, features)

    def _build(self, features, labels=None, params=None, config=None):
        # Pre-process features and labels
        features, labels = self._preprocess(self.mode, features, labels)
        results = self._graph_fn(mode=self.mode, inputs=features)
        if not isinstance(results, BridgeSpec):
            raise ValueError('`bridge_fn` should return an BridgeSpec.')
        predictions_results = {
            'results': results.results,
            'encoded': results.encoded,
            'generated': results.generated
        }

        loss = None
        train_op = None
        eval_metrics = None
        if self.mode == ModeKeys.PREDICT:
            predictions = self._build_predictions(
                results=predictions_results, features=features, labels=labels)
        else:
            losses, loss = self._build_loss(results, features, labels)
            eval_metrics = self._build_eval_metrics(results.results, features, labels)

            if self.mode == ModeKeys.TRAIN:
                train_op = self._build_train_op(loss)
                self._build_summary_op(results=results.results, generated=results.generated,
                                       features=features, labels=labels)

            predictions = self._build_predictions(results=predictions_results, features=features,
                                                  labels=labels, losses=losses)

        # We add 'useful' tensors to the graph collection so that we
        # can easly find them in our hooks/monitors.
        track(predictions, tf.GraphKeys.PREDICTIONS)

        return EstimatorSpec(mode=self.mode,
                             predictions=predictions,
                             loss=loss,
                             train_op=train_op,
                             eval_metric_ops=eval_metrics)
