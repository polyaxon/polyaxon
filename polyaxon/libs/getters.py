# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

import tensorflow as tf


def get_optimizer(module, **kwargs):
    from polyaxon.optimizers import OPTIMIZERS

    if isinstance(module, six.string_types):
        return OPTIMIZERS[module](**kwargs)()

    if hasattr(module, '__call__'):
        return module()


def get_activation(module, **kwargs):
    from polyaxon.activations import ACTIVATIONS

    if isinstance(module, six.string_types):
        return ACTIVATIONS[module](**kwargs)

    if hasattr(module, '__call__'):
        return module

    raise TypeError('Activation `{}` is not supported.'.format(module))


def get_initializer(module, **kwargs):
    from polyaxon.initializations import INITIALIZERS

    if isinstance(module, six.string_types):
        return INITIALIZERS[module](**kwargs)

    return module


def get_regularizer(module, **kwargs):
    from polyaxon.regularizations import REGULIZERS

    if isinstance(module, six.string_types):
        return REGULIZERS[module](**kwargs)

    return module


def get_metric(module, incoming, outputs, **kwargs):
    from polyaxon.metrics import METRICS

    if isinstance(module, six.string_types):
        module = METRICS[module](**kwargs)(incoming, outputs)
    elif hasattr(module, '__call__'):
        try:
            module = module(incoming, outputs)
        except TypeError as e:
            print(e.message)
            print('Reminder: Custom metric function arguments must be '
                  'define as follow: custom_metric(y_pred, y_true).')
            exit()
    elif not isinstance(module, tf.Tensor):
        ValueError("Invalid Metric type.")

    return module


def get_eval_metric(module, y_pred, y_true, **kwargs):
    from polyaxon.metrics import EVAL_METRICS

    if isinstance(module, six.string_types):
        module = EVAL_METRICS[module](y_pred, y_true, **kwargs)
    elif hasattr(module, '__call__'):
        try:
            module = module(y_pred, y_true)
        except TypeError as e:
            print(e.message)
            print('Reminder: Custom metric function arguments must be '
                  'define as follow: custom_metric(y_pred, y_true).')
            exit()
    elif not isinstance(module, tf.Tensor):
        ValueError("Invalid Metric type.")

    return module


def get_loss(module, y_pred, y_true, **kwargs):
    from polyaxon.losses import LOSSES

    if isinstance(module, six.string_types):
        module = LOSSES[module](**kwargs)(y_true, y_pred)

    elif hasattr(module, '__call__'):
        try:
            module = module(y_true, y_pred)
        except Exception as e:
            print(e.message)
            print('Reminder: Custom loss function arguments must be define as '
                  'follow: custom_loss(y_pred, y_true).')
            exit()
    elif not isinstance(module, tf.Tensor):
        raise ValueError('Invalid Loss type.')

    return module


def get_pipeline(module, mode, shuffle, num_epochs, subgraph_configs_by_features=None, **params):
    from polyaxon.experiments.subgraph import SubGraph
    from polyaxon.processing.pipelines import PIPELINES

    subgraphs_by_features = {}
    if subgraph_configs_by_features:
        for feature, subgraph_config in subgraph_configs_by_features.items():
            modules = SubGraph.build_subgraph_modules(mode=mode, subgraph_config=subgraph_config)
            subgraph = SubGraph(mode=mode, modules=modules, **subgraph_config.params)
            subgraphs_by_features[feature] = subgraph

    if isinstance(module, six.string_types):
        return PIPELINES[module](mode=mode, shuffle=shuffle, num_epochs=num_epochs,
                                 subgraphs_by_features=subgraphs_by_features, **params)

    else:
        raise ValueError('Invalid pipeline type.')


def get_graph_fn(config, graph_class=None):
    """Creates the graph operations."""
    from polyaxon.experiments.subgraph import SubGraph

    if graph_class is None:
        graph_class = SubGraph

    def graph_fn(mode, inputs):
        modules = graph_class.build_subgraph_modules(mode, config)
        graph = graph_class(mode=mode, modules=modules, features=config.features, **config.params)
        return graph(inputs)

    return graph_fn


def get_bridge_fn(config):
    """Creates a bridge function. Defaults to `NoOpBridge`

    Args:
        config: `BridgeConfig` instance.

    Returns:
        `function`.
    """
    from polyaxon.bridges import BRIDGES, NoOpBridge

    def bridge_fn(mode, inputs, loss_config, encoder_fn, decoder_fn):
        if config:
            bridge = BRIDGES[config.module]
            bridge = bridge(mode=mode, state_size=config.state_size, **config.params)
            return bridge(inputs, loss_config, encoder_fn, decoder_fn)

        return NoOpBridge(mode)(inputs, loss_config, encoder_fn, decoder_fn)

    return bridge_fn


def get_model_fn(model_config, graph_fn=None, encoder_fn=None, decoder_fn=None, bridge_fn=None):
    from polyaxon.models import MODELS, BaseModel
    from polyaxon.encoders import ENCODERS, Encoder
    from polyaxon.decoders import DECODERS, Decoder

    if not graph_fn:
        graph_fn = get_graph_fn(model_config.graph_config)

    if not encoder_fn and model_config.encoder_config:
        encoder = ENCODERS.get(model_config.encoder_config.module, Encoder)
        encoder_fn = get_graph_fn(model_config.encoder_config, encoder)

    if not decoder_fn and model_config.decoder_config:
        decoder = DECODERS.get(model_config.encoder_config.module, Decoder)
        decoder_fn = get_graph_fn(model_config.decoder_config, decoder)

    if not bridge_fn:
        bridge_fn = get_bridge_fn(model_config.bridge_config)

    def model_fn(features, labels, params, mode, config):
        """Builds the model graph"""
        if model_config.module == BaseModel.Types.GENERATOR:
            model = MODELS[model_config.module](
                mode=mode,
                encoder_fn=encoder_fn,
                decoder_fn=decoder_fn,
                bridge_fn=bridge_fn,
                loss_config=model_config.loss_config,
                optimizer_config=model_config.optimizer_config,
                eval_metrics_config=model_config.eval_metrics_config,
                summaries=model_config.summaries,
                clip_gradients=model_config.clip_gradients,
                clip_embed_gradients=model_config.clip_embed_gradients,
                **model_config.params)
        else:
            model = MODELS[model_config.module](
                mode=mode,
                graph_fn=graph_fn,
                loss_config=model_config.loss_config,
                optimizer_config=model_config.optimizer_config,
                eval_metrics_config=model_config.eval_metrics_config,
                summaries=model_config.summaries,
                clip_gradients=model_config.clip_gradients,
                clip_embed_gradients=model_config.clip_embed_gradients,
                **model_config.params)
        return model(features=features, labels=labels, params=params, config=config)

    return model_fn


def get_estimator(estimator_config, model_config, run_config):
    from polyaxon.experiments.estimator import ESTIMATORS

    model_fn = get_model_fn(model_config)

    estimator = ESTIMATORS[estimator_config.module](
        model_fn=model_fn,
        model_dir=estimator_config.output_dir,
        config=run_config,
        params=model_config.params)
    return estimator


def get_hooks(hooks_config):
    from polyaxon.experiments.hooks import HOOKS

    hooks = []
    for hook, params in hooks_config:
        if isinstance(hook, six.string_types):
            hook = HOOKS[hook](**params)
            hooks.append(hook)

    return hooks
