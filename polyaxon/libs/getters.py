# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from polyaxon.experiments.subgraph import SubGraph


def get_optimizer(optimizer, **kwargs):
    from polyaxon.optimizers import OPTIMIZERS

    if isinstance(optimizer, str):
        return OPTIMIZERS[optimizer](**kwargs)()

    if hasattr(optimizer, '__call__'):
        return optimizer()


def get_activation(activation, **kwargs):
    from polyaxon.activations import ACTIVATIONS

    if isinstance(activation, str):
        return ACTIVATIONS[activation](**kwargs)

    if hasattr(activation, '__call__'):
        return activation

    raise TypeError('Activation {} is unsupported.'.format(activation))


def get_initializer(initializer, **kwargs):
    from polyaxon.initializations import INITIALIZERS

    if isinstance(initializer, str):
        return INITIALIZERS[initializer](**kwargs)

    return initializer


def get_regularizer(regularizer, **kwargs):
    from polyaxon.regularizations import REGULIZERS

    if isinstance(regularizer, str):
        return REGULIZERS[regularizer](**kwargs)

    return regularizer


def get_metric(metric, incoming, outputs, **kwargs):
    from polyaxon.metrics import METRICS

    if isinstance(metric, str):
        metric = METRICS[metric](**kwargs)(incoming, outputs)
    elif hasattr(metric, '__call__'):
        try:
            metric = metric(incoming, outputs)
        except TypeError as e:
            print(e.message)
            print('Reminder: Custom metric function arguments must be '
                  'define as follow: custom_metric(y_pred, y_true).')
            exit()
    elif not isinstance(metric, tf.Tensor):
        ValueError("Invalid Metric type.")

    return metric


def get_eval_metric(metric, y_pred, y_true, **kwargs):
    from polyaxon.metrics import EVAL_METRICS

    if isinstance(metric, str):
        metric = EVAL_METRICS[metric](y_pred, y_true, **kwargs)
    elif hasattr(metric, '__call__'):
        try:
            metric = metric(y_pred, y_true)
        except TypeError as e:
            print(e.message)
            print('Reminder: Custom metric function arguments must be '
                  'define as follow: custom_metric(y_pred, y_true).')
            exit()
    elif not isinstance(metric, tf.Tensor):
        ValueError("Invalid Metric type.")

    return metric


def get_loss(loss, y_pred, y_true, **kwargs):
    from polyaxon.losses import LOSSES

    if isinstance(loss, str):
        loss = LOSSES[loss](**kwargs)(y_true, y_pred)

    elif hasattr(loss, '__call__'):
        try:
            loss = loss(y_true, y_pred)
        except Exception as e:
            print(e.message)
            print('Reminder: Custom loss function arguments must be define as '
                  'follow: custom_loss(y_pred, y_true).')
            exit()
    elif not isinstance(loss, tf.Tensor):
        raise ValueError('Invalid Loss type.')

    return loss


def get_pipeline(pipeline, **kwargs):
    from polyaxon.processing.pipelines import PIPELINES

    if isinstance(pipeline, str):
        pipeline = PIPELINES[pipeline](**kwargs)

    else:
        raise ValueError('Invalid pipeline type.')

    return pipeline


def get_graph_fn(config):
    """Creates the graph operations."""

    def graph_fn(mode, inputs):
        graph = SubGraph(mode, config.name, config.modules, config.kwargs)
        return graph(inputs)

    return graph_fn


def get_model_fn(model_config, graph_fn=None):
    from polyaxon.experiments.models import MODELS

    if not graph_fn:
        graph_fn = get_graph_fn(model_config.graph_config)

    def model_fn(features, labels, params, mode, config):
        """Builds the model graph"""
        model = MODELS[model_config.model_type](
            mode=mode,
            name=model_config.name,
            graph_fn=graph_fn,
            loss_config=model_config.loss_config,
            optimizer_config=model_config.optimizer_config,
            eval_metrics_config=model_config.eval_metrics_config,
            summaries=model_config.summaries,
            clip_gradients=model_config.clip_gradients,
            params=model_config.params)
        return model(features=features, labels=labels, params=params, config=config)

    return model_fn


def get_estimator(estimator_config, model_config, run_config):
    from polyaxon.experiments.estimator import ESTIMATORS

    model_fn = get_model_fn(model_config)

    estimator = ESTIMATORS[estimator_config.name](
        model_fn=model_fn,
        model_dir=estimator_config.output_dir,
        config=run_config,
        params=model_config.params)
    return estimator


def get_hooks(hooks_config):
    from polyaxon.experiments.hooks import HOOKS

    hooks = []
    for hook, params in hooks_config:
        if isinstance(hook, str):
            hook = HOOKS[hook](**params)
            hooks.append(hook)

    return hooks
