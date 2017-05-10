# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from tensorflow.python.estimator.model_fn import EstimatorSpec, ModeKeys
from tensorflow.python.framework import ops

from polyaxon.experiments import summarizer
from polyaxon.experiments.subgraph import SubGraph
from polyaxon.libs import configs, getters
from polyaxon.libs.dicts import flatten_dict
from polyaxon.libs.template_module import GraphModule
from polyaxon.libs.utils import extract_batch_length, track, get_tracked


class BaseModel(GraphModule):
    """Abstract base class for models.

      Args:
        mode: Specifies if this training, evaluation or prediction. See `ModeKeys`.
        config: An instance of `ModelConfig`.
        params: A dictionary of hyperparameter values
    """
    class Types(object):
        REGRESSOR = 'regressor'
        CLASSIFIER = 'classifier'
        GENERATOR = 'generator'

        VALUES = [REGRESSOR, CLASSIFIER, GENERATOR]

    def __init__(self, mode, config, model_type, summaries, name, params):
        super(BaseModel, self).__init__(mode, name, self.ModuleType.MODEL)
        self.config = config
        self.params = params
        self.model_type = model_type
        self.summaries = summarizer.SummaryOptions.validate(summaries)
        assert model_type in self.Types.VALUES, "`model_type` provided is unsupported."
        self._grads_and_vars = None
        self._total_loss = None
        self._loss = None

    def _clip_gradients(self, grads_and_vars):
        """Clips gradients by global norm."""
        gradients, variables = zip(*grads_and_vars)
        self._grads_and_vars = grads_and_vars

        if self.config.clip_gradients > 0.0:
            clipped_gradients, gradients_norm = tf.clip_by_global_norm(
                t_list=gradients, clip_norm=self.config.clip_gradients)
            return list(zip(clipped_gradients, variables))
        return grads_and_vars

    def _create_optimizer(self):
        """Creates the optimizer"""
        optimizer = getters.get_optimizer(
            self.config.optimizer_config.name,
            learning_rate=self.config.optimizer_config.learning_rate,
            decay_type=self.config.optimizer_config.decay_type,
            decay_steps=self.config.optimizer_config.decay_steps,
            decay_rate=self.config.optimizer_config.decay_rate,
            start_decay_at=self.config.optimizer_config.start_decay_at,
            stop_decay_at=self.config.optimizer_config.stop_decay_at,
            min_learning_rate=self.config.optimizer_config.min_learning_rate,
            staircase=self.config.optimizer_config.staircase,
            **self.config.optimizer_config.params)

        # Optionally wrap with SyncReplicasOptimizer
        if self.config.optimizer_config.sync_replicas > 0:
            optimizer = tf.train.SyncReplicasOptimizer(
                opt=optimizer,
                replicas_to_aggregate=self.config.optimizer_config.sync_replicas_to_aggregate,
                total_num_replicas=self.config.optimizer_config.sync_replicas)
            # This is really ugly, but we need to do this to make the optimizer
            # accessible outside of the model.
            configs.SYNC_REPLICAS_OPTIMIZER = optimizer

        return optimizer

    def _build_summary_op(self):
        summary_op = []
        for summary in self.summaries:
            if summary == summarizer.SummaryOptions.ACTIVATIONS:
                activations = get_tracked(tf.GraphKeys.ACTIVATIONS)
                summary_op += summarizer.add_activations_summary(activations)
            elif summary == summarizer.SummaryOptions.VARIABLES:
                variables = tf.trainable_variables()
                summary_op += summarizer.add_trainable_vars_summary(variables)
            elif summary == summarizer.SummaryOptions.GRADIENTS:
                summary_op += summarizer.add_gradients_summary(self._grads_and_vars)
            elif summary == summarizer.SummaryOptions.LOSS:
                summary_op += summarizer.add_loss_summaries(self._total_loss, self._loss)
            elif summary == summarizer.SummaryOptions.LEARNING_RATE:
                summary_op += summarizer.add_learning_rate_summaries()

        ops.add_to_collection(tf.summary.merge(summary_op), tf.GraphKeys.SUMMARY_OP)

    def _build_loss(self, results, features, labels):
        """Creates the loss operation

        Returns a tuple `(losses, loss)`:
            `losses` are the per-batch losses.
            `loss` is a single scalar tensor to minimize.
        """
        losses, loss = getters.get_loss(
            self.config.loss_config.name, results, labels, **self.config.loss_config.params)
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
        if self.model_type == self.Types.CLASSIFIER:
            results = tf.argmax(results, 1)
            labels = tf.argmax(labels, 1)

        metrics = {}
        for metric in self.config.eval_metrics_config:
            metrics[metric.name] = getters.get_eval_metric(
                metric.name, results, labels, **metric.params)
        return metrics

    def _build_subgraphs(self, features):
        """Creates the subgraph operations."""
        x = features['source_ids']
        self._graph = SubGraph(self.mode, self.config.graph_config.name,
                               self.config.graph_config.methods, self.config.graph_config.kwargs)
        return self._graph(x)

    def _build_train_op(self, loss):
        """Creates the training operation"""
        optimizer = self._create_optimizer()
        train_op = tf.contrib.layers.optimize_loss(
            loss=loss,
            global_step=tf.contrib.framework.get_global_step(),
            learning_rate=None,
            clip_gradients=self._clip_gradients,
            optimizer=optimizer,
            summaries=[])

        return train_op

    def _preprocess(self, features, labels):
        """Model specific preprocessing."""
        return features, labels

    @staticmethod
    def _build_predictions(results, features, labels, losses=None):
        """Creates the dictionary of predictions that is returned by the model."""
        predictions = {'results': results}
        # Add features and, if available, labels to predictions
        predictions.update(flatten_dict({'features': features['source_ids']}))  # TODO: source_ids ?
        if labels is not None:
            predictions.update(flatten_dict({'labels': labels}))

        if losses is not None:
            predictions['losses'] = losses  # TODO: transpose_batch_time(losses)

        return predictions

    @staticmethod
    def batch_size(features, labels):
        """Returns the batch size of the curren batch based on the passed features."""
        return extract_batch_length(features)

    def __call__(self, features, labels, params):
        """Creates the model graph. See the model_fn documentation in
        tf.contrib.learn.Estimator class for a more detailed explanation.
        """
        return self._template(features, labels, params)

    def _build(self, features, labels, params):
        """Subclasses should implement this method. See the `model_fn` documentation
        in tf.contrib.learn.Estimator class for a more detailed explanation.
        """
        # Pre-process features and labels
        features, labels = self._preprocess(features, labels)
        results = self._build_subgraphs(features)

        loss = None
        train_op = None
        eval_metrics = None
        if self.mode == ModeKeys.PREDICT:
            predictions = self._build_predictions(results=results, features=features, labels=labels)
        else:
            losses, loss = self._build_loss(results, features, labels)
            eval_metrics = self._build_eval_metrics(results, features, labels)

            if self.mode == ModeKeys.TRAIN:
                train_op = self._build_train_op(loss)
                self._build_summary_op()

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


MODELS = {
    'base_model': BaseModel
}
