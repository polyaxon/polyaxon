# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from tensorflow.python.estimator.model_fn import EstimatorSpec
from tensorflow.python.training import training

from polyaxon import Modes
from polyaxon.experiments import summarizer
from polyaxon.libs import configs, getters
from polyaxon.libs.configs import OptimizerConfig
from polyaxon.libs.dicts import flatten_dict
from polyaxon.libs.template_module import GraphModule
from polyaxon.libs.utils import extract_batch_length, track, get_tracked, get_arguments, get_shape
from polyaxon.metrics import ARGMAX_METRICS


class BaseModel(GraphModule):
    """Base class for models.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        graph_fn: Graph function. Follows the signature:
            * Args:
                * `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
                * `inputs`: the feature inputs.
        loss_config: An instance of `LossConfig`.
        optimizer_config: An instance of `OptimizerConfig`. Default value `Adam`.
        model_type: `str`, the type of this model.
            Possible values: `regressor`, `classifier`, `generator`
        summaries: `str` or `list`. The verbosity of the tensorboard visualization.
            Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
        name: `str`, the name of this model, everything will be encapsulated inside this scope.

    Returns:
        `EstimatorSpec`
    """
    class Types(object):
        REGRESSOR = 'Regressor'
        CLASSIFIER = 'Classifier'
        GENERATOR = 'Generator'

        VALUES = [REGRESSOR, CLASSIFIER, GENERATOR]

    def __init__(self, mode, model_type, graph_fn, loss_config, optimizer_config=None,
                 eval_metrics_config=None, summaries='all', clip_gradients=0.5, name="Model"):
        super(BaseModel, self).__init__(mode, name, self.ModuleType.MODEL)
        self.loss_config = loss_config
        self.optimizer_config = optimizer_config or OptimizerConfig('adam', learning_rate=0.001)
        self.eval_metrics_config = eval_metrics_config or []
        self.model_type = model_type
        self.summaries = summarizer.SummaryOptions.validate(summaries)
        assert model_type in self.Types.VALUES, "`model_type` provided is unsupported."
        self._clip_gradients = clip_gradients
        self._grads_and_vars = None
        self._total_loss = None
        self._loss = None

        self._check_subgraph_fn(function=graph_fn, function_name='graph_fn')
        self._graph_fn = graph_fn

    @staticmethod
    def _check_subgraph_fn(function, function_name):
        if function is not None:
            # Check number of arguments of the given function matches requirements.
            model_fn_args = get_arguments(function)
            if 'mode' not in model_fn_args or 'inputs' not in model_fn_args:
                raise ValueError("Model's `{}` `{}` should have 2 args: "
                                 "`mode` and `inputs`.".format(function_name, function))
        else:
            raise ValueError("`{}` must be provided to Model.".format(function_name))

    def _call_graph_fn(self, mode, inputs):
        """Calls model function with support of 2, 3 or 4 arguments.

        Args:
            mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
            inputs: `Tensor` or `dict` of tensors

        Raises:
            TypeError: if the mode does not correspond to the model_type.
        """
        if mode in [Modes.GENERATE, Modes.ENCODE] and self.model_type != self.Types.GENERATOR:
            raise TypeError("Current model type `{}` does not support passed mode `{}`.".format(
                self.model_type, mode))
        return self._graph_fn(mode=mode, inputs=inputs)

    def _clip_gradients_fn(self, grads_and_vars):
        """Clips gradients by global norm."""
        gradients, variables = zip(*grads_and_vars)
        self._grads_and_vars = grads_and_vars

        if self._clip_gradients > 0.0:
            clipped_gradients, gradients_norm = tf.clip_by_global_norm(
                t_list=gradients, clip_norm=self._clip_gradients)
            return list(zip(clipped_gradients, variables))
        return grads_and_vars

    def _build_optimizer(self):
        """Creates the optimizer"""
        optimizer = getters.get_optimizer(
            self.optimizer_config.module,
            learning_rate=self.optimizer_config.learning_rate,
            decay_type=self.optimizer_config.decay_type,
            decay_steps=self.optimizer_config.decay_steps,
            decay_rate=self.optimizer_config.decay_rate,
            start_decay_at=self.optimizer_config.start_decay_at,
            stop_decay_at=self.optimizer_config.stop_decay_at,
            min_learning_rate=self.optimizer_config.min_learning_rate,
            staircase=self.optimizer_config.staircase,
            **self.optimizer_config.params)

        # Optionally wrap with SyncReplicasOptimizer
        if self.optimizer_config.sync_replicas > 0:
            optimizer = tf.train.SyncReplicasOptimizer(
                opt=optimizer,
                replicas_to_aggregate=self.optimizer_config.sync_replicas_to_aggregate,
                total_num_replicas=self.optimizer_config.sync_replicas)
            # This is really ugly, but we need to do this to make the optimizer
            # accessible outside of the model.
            configs.SYNC_REPLICAS_OPTIMIZER = optimizer

        return optimizer

    def _build_summary_op(self, results=None, features=None, labels=None):
        """Builds summaries for this model.

        The summaries are one value (or more) of:
            * (`ACTIVATIONS`, `VARIABLES`, `GRADIENTS`, `LOSS`, `LEARNING_RATE`)
        """
        summary_op = []
        for summary in self.summaries:
            if summary == summarizer.SummaryOptions.ACTIVATIONS:
                activations = get_tracked(tf.GraphKeys.ACTIVATIONS)
                summary_op += summarizer.add_activations_summary(activations)
            elif summary == summarizer.SummaryOptions.VARIABLES:
                variables = tf.trainable_variables()
                summary_op += summarizer.add_trainable_vars_summary(variables)
            elif summary == summarizer.SummaryOptions.GRADIENTS and self._clip_gradients > 0.0:
                summary_op += summarizer.add_gradients_summary(self._grads_and_vars)
            elif summary == summarizer.SummaryOptions.LOSS:
                summary_op += summarizer.add_loss_summaries(self._total_loss, self._loss)
            elif summary == summarizer.SummaryOptions.LEARNING_RATE:
                summary_op += summarizer.add_learning_rate_summaries()
            elif summary == summarizer.SummaryOptions.IMAGE_INPUT:
                summary_op += summarizer.add_image_summary(tf.reshape(features, [-1, 28, 28, 1]),
                                                           op_name='inputs')
            elif summary == summarizer.SummaryOptions.IMAGE_RESULT:
                summary_op += summarizer.add_image_summary(tf.reshape(results, [-1, 28, 28, 1]),
                                                           op_name='results')

        if summary_op:
            tf.summary.merge(summary_op)

    def _build_loss(self, results, features, labels):
        """Creates the loss operation

        Returns:
             tuple `(losses, loss)`:
                `losses` are the per-batch losses.
                `loss` is a single scalar tensor to minimize.
        """
        losses, loss = getters.get_loss(
            self.loss_config.module, results, labels, **self.loss_config.params)
        self._loss = loss
        self._losses = losses

        other_losses = get_tracked(tf.GraphKeys.REGULARIZATION_LOSSES)
        if other_losses:
            loss = [loss] + other_losses
            loss = tf.add_n(loss, name="TotalLoss")
            self._total_loss = loss
        return losses, loss

    def _build_eval_metrics(self, results, features, labels):
        """Creates the loss operation

        Returns a tuple `(losses, loss)`:
            `losses` are the per-batch losses.
            `loss` is a single scalar tensor to minimize.
        """
        lshape = get_shape(labels)

        def get_labels_and_results(results, labels):
            if len(lshape) == 1 or (len(lshape) and int(lshape[1]) == 1):
                return tf.argmax(results), tf.argmax(labels)
            else:
                return tf.argmax(results, 1), tf.argmax(labels, 1)

        metrics = {}
        for metric in self.eval_metrics_config:
            _results, _labels = results, labels
            if self.model_type == self.Types.CLASSIFIER and metric.module in ARGMAX_METRICS:
                _results, _labels = get_labels_and_results(results, labels)
            metrics[metric.module] = getters.get_eval_metric(
                metric.module, _results, _labels, **metric.params)
        return metrics

    def _build_train_op(self, loss):
        """Creates the training operation"""
        optimizer = self._build_optimizer()
        train_op = tf.contrib.layers.optimize_loss(
            loss=loss,
            global_step=training.get_or_create_global_step(),
            learning_rate=None,
            clip_gradients=self._clip_gradients_fn,
            optimizer=optimizer,
            summaries=[])

        return train_op

    def _preprocess(self, mode, features, labels):
        """Model specific preprocessing."""
        return features, labels

    @staticmethod
    def _build_predictions(results, features, labels, losses=None):
        """Creates the dictionary of predictions that is returned by the model."""
        predictions = flatten_dict({'results': results})
        # Add features and, if available, labels to predictions
        predictions.update(flatten_dict({'features': features}))  # TODO: source_ids ?
        if labels is not None:
            predictions.update(flatten_dict({'labels': labels}))

        if losses is not None:
            predictions['losses'] = losses  # TODO: transpose_batch_time(losses)

        return predictions

    @staticmethod
    def batch_size(features, labels):
        """Returns the batch size of the curren batch based on the passed features.

        Args:
            features: The features.
            labels: The labels
        """
        return extract_batch_length(features)

    def __call__(self, features, labels, params=None, config=None):
        """Calls the built mode."""
        return super(BaseModel, self).__call__(features, labels, params, config)

    def _build(self, features, labels, params=None, config=None):
        """Build the different operation of the model."""
        # Pre-process features and labels
        features, labels = self._preprocess(self.mode, features, labels)
        results = self._call_graph_fn(mode=self.mode, inputs=features)

        loss = None
        train_op = None
        eval_metrics = None
        if Modes.is_infer(self.mode):
            predictions = self._build_predictions(results=results, features=features, labels=labels)
        else:
            losses, loss = self._build_loss(results, features, labels)
            eval_metrics = self._build_eval_metrics(results, features, labels)

            if Modes.is_train(self.mode):
                train_op = self._build_train_op(loss)
                self._build_summary_op(results=results, features=features, labels=labels)

            predictions = self._build_predictions(results=results, features=features,
                                                  labels=labels, losses=losses)

        # We add 'useful' tensors to the graph collection so that we
        # can easly find them in our hooks/monitors.
        track(predictions, tf.GraphKeys.PREDICTIONS)

        return EstimatorSpec(mode=self.mode,
                             predictions=predictions,
                             loss=loss,
                             train_op=train_op,
                             eval_metric_ops=eval_metrics)
