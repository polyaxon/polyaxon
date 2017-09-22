# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from tensorflow.python.training import training

from polyaxon_schemas.optimizers import AdamConfig

from polyaxon import Modes
from polyaxon.estimators.estimator_spec import EstimatorSpec
from polyaxon.libs import getters
from polyaxon.libs.dicts import flatten_dict
from polyaxon.libs.template_module import GraphModule
from polyaxon.libs.utils import extract_batch_length, track, get_tracked, get_arguments
from polyaxon.models import summarizer


class BaseModel(GraphModule):
    """Base class for models.

    Args:
         mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
         model_type: `str`, the type of this model.
            Possible values: `Regressor`, `Classifier`, `Generator`, 'RL'
         graph_fn: Graph function. Follows the signature:
             * Args:
                 * `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
                 * `inputs`: the feature inputs.
         loss_config: An instance of `LossConfig`.
         optimizer_config: An instance of `OptimizerConfig`. Default value `Adam`.
         eval_metrics_config: a list of `MetricConfig` instances.
         summaries: `str` or `list`. The verbosity of the tensorboard visualization.
             Possible values: [
             `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
             ]
         clip_gradients: `float`. Gradients  clipping by global norm.
         clip_embed_gradients: `float`. Embedding gradients clipping to a specified value.
         name: `str`, the name of this model, everything will be encapsulated inside this scope.

    Returns:
        `EstimatorSpec`

    Raises:
            TypeError: if the mode does not correspond to the model_type.
    """

    class Types(object):
        REGRESSOR = 'Regressor'
        CLASSIFIER = 'Classifier'
        GENERATOR = 'Generator'
        RL = 'RL'

        VALUES = [REGRESSOR, CLASSIFIER, GENERATOR, RL]

    def __init__(self, mode, model_type, graph_fn, loss_config, optimizer_config=None,
                 eval_metrics_config=None, summaries='all', clip_gradients=0.5,
                 clip_embed_gradients=0.1, name="Model"):

        # Check if mode corresponds to the correct model
        if mode in [Modes.GENERATE, Modes.ENCODE] and model_type != self.Types.GENERATOR:
            raise TypeError("Current model type `{}` does not support passed mode `{}`.".format(
                model_type, mode))

        super(BaseModel, self).__init__(mode, name, self.ModuleType.MODEL)
        self.loss_config = loss_config
        self.optimizer_config = optimizer_config or AdamConfig(learning_rate=0.001)
        self.eval_metrics_config = eval_metrics_config or []
        self.model_type = model_type
        self.summaries = summarizer.SummaryOptions.validate(summaries)
        assert model_type in self.Types.VALUES, "`model_type` provided is unsupported."
        self._clip_gradients = clip_gradients
        self._clip_embed_gradients = clip_embed_gradients
        self._grads_and_vars = None
        self._total_loss = None
        self._losses = None
        self._loss = None

        self._check_subgraph_fn(function=graph_fn, function_name='graph_fn')
        self._graph_fn = graph_fn

    @staticmethod
    def _check_subgraph_fn(function, function_name):
        """Checks that the functions provided for constructing the graph has a valid signature."""
        if function is not None:
            # Check number of arguments of the given function matches requirements.
            model_fn_args = get_arguments(function)
            if 'mode' not in model_fn_args or 'features' not in model_fn_args:
                raise ValueError(
                    "Model's `{}` `{}` should have at least 2 args: "
                    "`mode`, `features`, and possibly `features`.".format(function_name, function))
        else:
            raise ValueError("`{}` must be provided to Model.".format(function_name))

    def _call_graph_fn(self, features, labels=None):
        """Calls graph function.

        Args:
            features: `Tensor` or `dict` of tensors
            labels: `Tensor` or `dict` of tensors
        """
        kwargs = {}
        if 'labels' in get_arguments(self._graph_fn):
            kwargs['labels'] = labels
        return self._graph_fn(mode=self.mode, features=features, **kwargs)

    def _clip_gradients_fn(self, grads_and_vars):
        """Clips gradients by global norm."""
        gradients, variables = zip(*grads_and_vars)
        self._grads_and_vars = grads_and_vars

        if self._clip_gradients > 0.0:
            clipped_gradients, gradients_norm = tf.clip_by_global_norm(
                t_list=gradients, clip_norm=self._clip_gradients)
            grads_and_vars = list(zip(clipped_gradients, variables))
        if self._clip_embed_gradients > 0.0:
            clipped_gradients = []
            variables = []
            for gradient, variable in grads_and_vars:
                if "embedding" in variable.name or "Embedding" in variable.name:
                    tmp = tf.clip_by_norm(t=gradient.values, clip_norm=self._clip_embed_gradients)
                    gradient = tf.IndexedSlices(tmp, gradient.indices, gradient.dense_shape)
                clipped_gradients.append(gradient)
                variables.append(variable)
            grads_and_vars = list(zip(clipped_gradients, variables))
        return grads_and_vars

    def _build_optimizer(self):
        """Creates the optimizer"""
        optimizer = getters.get_optimizer(
            self.optimizer_config.IDENTIFIER, **self.optimizer_config.to_dict())

        # TODO: use the _SyncReplicasOptimizerHook
        # # Optionally wrap with SyncReplicasOptimizer
        # if self.optimizer_config.sync_replicas > 0:
        #     optimizer = tf.train.SyncReplicasOptimizer(
        #         opt=optimizer,
        #         replicas_to_aggregate=self.optimizer_config.sync_replicas_to_aggregate,
        #         total_num_replicas=self.optimizer_config.sync_replicas)
        #     # This is really ugly, but we need to do this to make the optimizer
        #     # accessible outside of the model.
        #     configs.SYNC_REPLICAS_OPTIMIZER = optimizer

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
                summary_op += summarizer.add_image_summary(features, op_name='inputs')
            elif summary == summarizer.SummaryOptions.IMAGE_RESULT:
                summary_op += summarizer.add_image_summary(results, op_name='results')

        # no need to tf.summary.merge(summary_op), for now we merge all at hook level
        return summary_op

    def _build_loss(self, results, features, labels):
        """Creates the loss operation

        Returns:
             tuple `(losses, loss)`:
                `losses` are the per-batch losses.
                `loss` is a single scalar tensor to minimize.
        """
        losses, loss = getters.get_loss(
            self.loss_config.IDENTIFIER, results, labels, **self.loss_config.to_dict())
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
        metrics = {}
        for metric in self.eval_metrics_config:
            metrics[metric.IDENTIFIER] = getters.get_metric(
                metric.IDENTIFIER, results, labels, **metric.to_dict())
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

    def _preprocess(self, features, labels):
        """Model specific preprocessing."""
        return features, labels

    def _build_predictions(self, results, features, labels):
        """Creates the dictionary of predictions that is returned by the model."""
        predictions = flatten_dict({'results': results})
        # Add features and, if available, labels to predictions
        predictions.update(flatten_dict({'features': features}))
        if labels is not None:
            predictions.update(flatten_dict({'labels': labels}))

        if self._losses is not None:
            predictions['losses'] = self._losses

        return predictions

    def _build_extra_ops(self, results, features, labels):
        return None

    @staticmethod
    def batch_size(features, labels):
        """Returns the batch size of the current batch based on the passed features.

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
        features, labels = self._preprocess(features, labels)
        results = self._call_graph_fn(features=features, labels=labels)

        loss = None
        train_op = None
        eval_metrics = None
        if Modes.is_infer(self.mode):
            predictions = self._build_predictions(results=results, features=features, labels=labels)
            extra_ops = self._build_extra_ops(results=results, features=features, labels=labels)
        else:
            losses, loss = self._build_loss(results, features, labels)
            eval_metrics = self._build_eval_metrics(results, features, labels)

            if Modes.is_train(self.mode):
                train_op = self._build_train_op(loss)
                self._build_summary_op(results=results, features=features, labels=labels)

            predictions = self._build_predictions(results=results, features=features, labels=labels)
            extra_ops = self._build_extra_ops(results=results, features=features, labels=labels)

        track(predictions, tf.GraphKeys.PREDICTIONS)

        return EstimatorSpec(mode=self.mode,
                             predictions=predictions,
                             loss=loss,
                             extra_ops=extra_ops,
                             train_op=train_op,
                             eval_metric_ops=eval_metrics)
