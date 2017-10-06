# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

import six

import tensorflow as tf

from polyaxon_schemas.initializations import InitializerSchema
from polyaxon_schemas.utils import to_camel_case

from polyaxon.libs.utils import to_list, get_shape


def get_optimizer(module, **kwargs):
    from polyaxon.optimizers import OPTIMIZERS

    if isinstance(module, six.string_types):
        return OPTIMIZERS[module](**kwargs)()

    if hasattr(module, '__call__'):
        return module()


def get_constraint(module, **kwargs):
    from polyaxon.constraints import CONSTRAINTS

    if isinstance(module, six.string_types):
        return CONSTRAINTS[module].from_config(**kwargs)

    if hasattr(module, '__call__'):
        return module()


def get_layer(module, **kwargs):
    from polyaxon.layers import LAYERS

    if isinstance(module, six.string_types):
        return LAYERS[module].from_config(**kwargs)

    if hasattr(module, '__call__'):
        return module


def get_exploration(module, **kwargs):
    from polyaxon.rl.explorations import DISCRETE_EXPLORATIONS, CONTINUOUS_EXPLORATIONS

    if isinstance(module, six.string_types):
        if kwargs.pop('is_continuous', False):
            return CONTINUOUS_EXPLORATIONS[module](**kwargs)
        else:
            return DISCRETE_EXPLORATIONS[module](**kwargs)

    if hasattr(module, '__call__'):
        return module()

    raise TypeError('Exploration `{}` is not supported.'.format(module))


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
        return INITIALIZERS[to_camel_case(module)](**kwargs)
    if isinstance(module, Mapping):
        config = InitializerSchema(strict=True).load(data=module).data
        return INITIALIZERS[config.IDENTIFIER](**config.to_dict())
    return module


def get_regularizer(module, **kwargs):
    from polyaxon.regularizations import REGULARIZERS

    if isinstance(module, six.string_types):
        return REGULARIZERS[module](**kwargs)

    return module


def get_metric(module, y_pred, y_true, **kwargs):
    from polyaxon.metrics import METRICS, ARGMAX_METRICS

    def get_labels_and_results(results, labels):
        lshape = get_shape(labels)
        if len(lshape) == 1 or (lshape and int(lshape[1]) == 1):
            return tf.argmax(results), tf.argmax(labels)
        else:
            return tf.argmax(results, 1), tf.argmax(labels, 1)

    if isinstance(module, six.string_types):
        input_layer = kwargs.pop('input_layer', None)
        output_layer = kwargs.pop('output_layer', None)
        if isinstance(y_pred, Mapping):
            if input_layer is not None:
                y_pred = y_pred[input_layer]
            elif len(y_pred) == 1:
                y_pred = list(six.itervalues(y_pred))[0]
            else:
                raise ValueError("Eval Metric input is not defined and results has multiple keys!")

        if isinstance(y_true, Mapping):
            if output_layer is not None:
                y_true = y_true[output_layer]
            elif len(y_true) == 1:
                y_true = list(six.itervalues(y_true))[0]
            else:
                raise ValueError("Eval Metric output is not defined and labels has multiple keys!")

        if module in ARGMAX_METRICS:
            y_pred, y_true = get_labels_and_results(y_pred, y_true)
        module = METRICS[module](y_pred, y_true, **kwargs)

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
        input_layer = kwargs.pop('input_layer', None)
        output_layer = kwargs.pop('output_layer', None)
        if isinstance(y_pred, Mapping):
            if input_layer is not None:
                y_pred = y_pred[input_layer]
            elif len(y_pred) == 1:
                y_pred = list(six.itervalues(y_pred))[0]
            else:
                raise ValueError("Loss input is not defined and results has multiple keys!")

        if isinstance(y_true, Mapping):
            if output_layer is not None:
                y_true = y_true[output_layer]
            elif len(y_true) == 1:
                y_true = list(six.itervalues(y_true))[0]
            else:
                raise ValueError("Loss output is not defined and labels has multiple keys!")

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


def get_memory(module, **kwargs):
    from polyaxon.rl.memories import MEMORIES

    if isinstance(module, six.string_types):
        return MEMORIES[module](**kwargs)

    if hasattr(module, '__call__'):
        return module()

    raise TypeError('Memory `{}` is not supported.'.format(module))


def get_pipeline(module, mode, **params):
    from polyaxon.processing.pipelines import PIPELINES

    feature_processors = params.pop('feature_processors', {})
    if feature_processors:
        for feature, graph_config in feature_processors.items():
            feature_processors[feature] = get_graph_fn(graph_config)

    if isinstance(module, six.string_types):
        return PIPELINES[module](mode=mode, feature_processors=feature_processors, **params)

    else:
        raise ValueError('Invalid pipeline type.')


def get_environment(module, env_id, **kwargs):
    from polyaxon.rl.environments import ENVIRONMENTS

    if isinstance(module, six.string_types):
        return ENVIRONMENTS[module](env_id=env_id, **kwargs)

    if hasattr(module, '__call__'):
        return module()

    raise TypeError('Environment `{}` is not supported.'.format(module))


def get_graph_fn(config, graph_class=None):
    """Creates the graph operations."""
    from polyaxon.libs.graph import Graph

    if graph_class is None:
        graph_class = Graph

    def graph_fn(mode, features, labels, return_dict=True):
        graph = graph_class.from_config(mode, features, labels, config)
        inputs = []
        for i_name in graph.input_names:
            if i_name in features:
                inputs.append(features[i_name])
            elif isinstance(labels, Mapping) and i_name in labels:
                inputs.append(labels[i_name])

        outputs = to_list(graph(inputs))
        if return_dict:
            return dict(zip(graph.output_names, outputs))
        return outputs

    return graph_fn


def get_bridge_fn(config):
    """Creates a bridge function. Defaults to `NoOpBridge`

    Args:
        config: `BridgeConfig` instance.

    Returns:
        `function`.
    """
    from polyaxon.bridges import BRIDGES, NoOpBridge

    def bridge_fn(mode, features, labels, loss, encoder_fn, decoder_fn):
        if config:
            bridge = BRIDGES[config.module]
            bridge = bridge(mode=mode, state_size=config.state_size, **config.params)
            return bridge(features, labels, loss, encoder_fn, decoder_fn)

        return NoOpBridge(mode)(features, labels, loss, encoder_fn, decoder_fn)

    return bridge_fn


def get_model_fn(model_config, graph_fn=None, encoder_fn=None, decoder_fn=None, bridge_fn=None):
    from polyaxon.models import MODELS, BaseModel

    if not graph_fn:
        graph_fn = get_graph_fn(model_config.graph)

    if not bridge_fn:
        bridge_fn = get_bridge_fn(model_config.bridge)

    def model_fn(features, labels, params, mode, config):
        """Builds the model graph"""
        if model_config.module == BaseModel.Types.GENERATOR:
            model = MODELS[model_config.module](
                mode=mode,
                encoder_fn=encoder_fn,
                decoder_fn=decoder_fn,
                bridge_fn=bridge_fn,
                loss=model_config.loss,
                optimizer=model_config.optimizer,
                metrics=model_config.metrics,
                summaries=model_config.summaries,
                clip_gradients=model_config.clip_gradients,
                clip_embed_gradients=model_config.clip_embed_gradients,
                **model_config.params)
        else:
            model = MODELS[model_config.module](
                mode=mode,
                graph_fn=graph_fn,
                loss=model_config.loss,
                optimizer=model_config.optimizer,
                metrics=model_config.metrics,
                summaries=model_config.summaries,
                clip_gradients=model_config.clip_gradients,
                clip_embed_gradients=model_config.clip_embed_gradients,
                **model_config.params)
        return model(features=features, labels=labels, params=params, config=config)

    return model_fn


def get_estimator(model, run_config, module='Estimator', output_dir=None):
    from polyaxon.estimators import ESTIMATORS
    from polyaxon.models import MODELS

    def model_fn(features, labels, params, mode, config):
        return MODELS[model.IDENTIFIER].from_config(mode, model)(features=features,
                                                                 labels=labels,
                                                                 params=params,
                                                                 config=config)

    estimator = ESTIMATORS[module](
        model_fn=model_fn,
        model_dir=output_dir,
        config=run_config,)
    return estimator


def get_agent(module, model, memory, run_config, output_dir=None):
    from polyaxon.estimators import AGENTS
    from polyaxon.models import MODELS

    model_fn = MODELS[model.IDENTIFIER].from_config(model)
    memory = get_memory(memory.IDENTIFER, **memory.to_dict())

    agent = AGENTS[module](
        model_fn=model_fn,
        memory=memory,
        model_dir=output_dir,
        config=run_config)
    return agent


def get_hooks(hooks_config):
    from polyaxon.estimators.hooks import HOOKS

    hooks = []
    for hook_dict in hooks_config:
        hook_config, hook = six.iteritems(hook_dict)[0]
        if isinstance(hook, six.string_types):
            hook = HOOKS[hook](**hook_config.to_dict())
            hooks.append(hook)

    return hooks
