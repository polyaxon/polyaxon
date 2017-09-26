# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

from polyaxon_schemas.losses import MeanSquaredErrorConfig

from polyaxon.models.base import BaseModel


class Regressor(BaseModel):
    """Regressor base model.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
            Possible values: `regressor`, `classifier`, `generator`
        graph_fn: Graph function. Follows the signature:
            * Args:
                * `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
                * `inputs`: the feature inputs.
        loss: An instance of `LossConfig`. Default value `mean_squared_error`.
        optimizer: An instance of `OptimizerConfig`. Default value `Adam`.
        metrics: a list of `MetricConfig` instances.
        summaries: `str` or `list`. The verbosity of the tensorboard visualization.
            Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
        clip_gradients: `float`. Gradients  clipping by global norm.
        clip_embed_gradients: `float`. Embedding gradients clipping to a specified value.
        name: `str`, the name of this model, everything will be encapsulated inside this scope.

    Returns:
        `EstimatorSpec`
    """

    def __init__(self,
                 mode,
                 graph_fn,
                 loss=None,
                 optimizer=None,
                 metrics=None,
                 summaries='all',
                 clip_gradients=0.5,
                 clip_embed_gradients=0.1,
                 name="Regressor"):
        loss = loss or MeanSquaredErrorConfig()
        super(Regressor, self).__init__(
            mode=mode,
            name=name,
            model_type=self.Types.REGRESSOR,
            graph_fn=graph_fn,
            loss=loss,
            optimizer=optimizer,
            metrics=metrics,
            summaries=summaries,
            clip_gradients=clip_gradients,
            clip_embed_gradients=clip_embed_gradients)

    def _preprocess(self, features, labels):
        if isinstance(labels, Mapping):
            labels = labels['labels']
        return super(Regressor, self)._preprocess(features, labels)
