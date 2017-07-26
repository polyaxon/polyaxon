# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

import tensorflow as tf

from polyaxon import Modes
from polyaxon.estimators.estimator_spec import EstimatorSpec
from polyaxon.bridges import BridgeSpec
from polyaxon.libs.configs import OptimizerConfig, LossConfig
from polyaxon.libs.utils import get_tracked, get_arguments, track
from polyaxon.models.base import BaseModel


class Generator(BaseModel):
    """Generator base model.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
            Possible values: `regressor`, `classifier`, `generator`.
        encoder_fn: Encoder Graph function. Follows the signature:
            * Args:
                * `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
                * `inputs`: the feature inputs.
        decoder_fn: Decoder Graph function. Follows the signature:
            * Args:
                * `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
                * `inputs`: the feature inputs.
        bridge_fn: The bridge to use. Follows the signature:
            * Args:
                * `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
                * `inputs`: the feature inputs.
                * `encoder_fn`: the encoder function.
                * `decoder_fn` the decoder function.
        loss_config: An instance of `LossConfig`. Default value `mean_squared_error`.
        optimizer_config: An instance of `OptimizerConfig`. Default value `Adadelta`.
        summaries: `str` or `list`. The verbosity of the tensorboard visualization.
            Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
        eval_metrics_config: a list of `MetricConfig` instances.
        summaries: `str` or `list`. The verbosity of the tensorboard visualization.
            Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
        clip_gradients: `float`. Gradients  clipping by global norm.
        clip_embed_gradients: `float`. Embedding gradients clipping to a specified value.
        name: `str`, the name of this model, everything will be encapsulated inside this scope.

    Returns:
        `EstimatorSpec`
    """

    def __init__(self, mode, encoder_fn, decoder_fn, bridge_fn, loss_config=None,
                 optimizer_config=None, summaries='all', eval_metrics_config=None,
                 clip_gradients=0.5, clip_embed_gradients=0.1, name="Generator"):
        optimizer_config = optimizer_config or OptimizerConfig('adadelta', learning_rate=0.4)
        loss_config = loss_config or LossConfig(module='sigmoid_cross_entropy')
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
            clip_gradients=clip_gradients, clip_embed_gradients=clip_embed_gradients)

    @staticmethod
    def _check_bridge_fn(function):
        if function is not None:
            # Check number of arguments of the given function matches requirements.
            model_fn_args = get_arguments(function)
            if ('mode' not in model_fn_args or
                    'loss_config' not in model_fn_args or
                    'features' not in model_fn_args or
                    'labels' not in model_fn_args or
                    'encoder_fn' not in model_fn_args or
                    'encoder_fn' not in model_fn_args):
                raise ValueError(
                    "Model's `bridge` `{}` should have these args: "
                    "`mode`, `features`, `labels`, `encoder_fn`, "
                    "and `decoder_fn`.".format(function))
        else:
            raise ValueError("`bridge_fn` must be provided to Model.")

    def _build_graph_fn(self):
        """Creates a graph_fn for the auto encoder based on the encoder/decoder functions.

        Returns:
            `function` with args: `mode`, `inputs`.
        """

        def graph_fn(mode, features, labels=None):
            return self._bridge_fn(mode=mode,
                                   features=features,
                                   labels=labels,
                                   loss_config=self.loss_config,
                                   encoder_fn=self._encode_fn,
                                   decoder_fn=self._decoder_fn)

        return graph_fn

    def _build_loss(self, results, features, labels):
        """Creates the loss operation based on the bridge.

        Returns:
             tuple `(losses, loss)`:
                `losses` are the per-batch losses.
                `loss` is a single scalar tensor to minimize.
        """

        loss = results.loss
        losses = results.losses
        self._loss = loss
        self._losses = losses

        other_losses = get_tracked(tf.GraphKeys.REGULARIZATION_LOSSES)
        if other_losses:
            loss = [loss] + other_losses
            loss = tf.add_n(loss, name="TotalLoss")
            self._total_loss = loss
        return losses, loss

    def _preprocess(self, features, labels=None):
        if isinstance(features, Mapping):
            if len(features) > 1:
                raise ValueError("Autoencoder accept only one feature value, "
                                 "received a dict of `{}` instead".format(list(features.keys())))
            features = list(features.values())[0]
        return super(Generator, self)._preprocess(features, labels)

    def _build(self, features, labels=None, params=None, config=None):
        # Pre-process features and labels
        features, labels = self._preprocess(features, labels)
        results = self._call_graph_fn(features=features, labels=labels)
        if not isinstance(results, BridgeSpec):
            raise ValueError('`bridge_fn` should return a BridgeSpec.')

        loss = None
        train_op = None
        eval_metrics = None
        if Modes.is_infer(self.mode):
            predictions = self._build_predictions(
                results=results.results, features=features, labels=labels)
        else:
            losses, loss = self._build_loss(results, features, features)
            eval_metrics = self._build_eval_metrics(results.results, features, features)

            if Modes.is_train(self.mode):
                train_op = self._build_train_op(loss)
                self._build_summary_op(results=results.results, features=features, labels=labels)

            predictions = self._build_predictions(
                results=results.results, features=features, labels=labels)

        track(predictions, tf.GraphKeys.PREDICTIONS)

        return EstimatorSpec(mode=self.mode,
                             predictions=predictions,
                             loss=loss,
                             train_op=train_op,
                             eval_metric_ops=eval_metrics)
