# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

from polyaxon_schemas.models import ClassifierConfig
from tensorflow.python.ops import standard_ops

from polyaxon_schemas.losses import SigmoidCrossEntropyConfig

from polyaxon.models.base import BaseModel


class Classifier(BaseModel):
    """Regressor base model.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
            Possible values: `regressor`, `classifier`, `generator`
        graph_fn: Graph function. Follows the signature:
            * Args:
                * `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
                * `inputs`: the feature inputs.
        loss: An instance of `LossConfig`. Default value `sigmoid_cross_entropy`.
        optimizer: An instance of `OptimizerConfig`. Default value `Adam`.
        metrics: a list of `MetricConfig` instances.
        summaries: `str` or `list`. The verbosity of the tensorboard visualization.
            Possible values:
             [`all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`]
        clip_gradients: `float`. Gradients  clipping by global norm.
        clip_embed_gradients: `float`. Embedding gradients clipping to a specified value.
        one_hot_encode: `bool`. to one hot encode the outputs.
        n_classes: `int`. The number of classes used in the one hot encoding.
        name: `str`, the name of this model, everything will be encapsulated inside this scope.

    Returns:
        `EstimatorSpec`
    """
    CONFIG = ClassifierConfig

    def __init__(self,
                 mode,
                 graph_fn,
                 loss=None,
                 optimizer=None,
                 summaries='all',
                 metrics=None,
                 clip_gradients=0.5,
                 clip_embed_gradients=0.1,
                 one_hot_encode=None,
                 n_classes=None,
                 name="Classifier"):
        if one_hot_encode and (n_classes is None or not isinstance(n_classes, int)):
            raise ValueError('`n_classes` must be an integer non negative value '
                             'when `one_hot_encode` is set to `True`, '
                             'received instead: {}'.format(n_classes))

        self.one_hot_encode = one_hot_encode
        self.n_classes = n_classes
        loss = loss or SigmoidCrossEntropyConfig()
        super(Classifier, self).__init__(
            mode=mode,
            name=name,
            model_type=self.Types.CLASSIFIER,
            graph_fn=graph_fn,
            loss=loss,
            optimizer=optimizer,
            metrics=metrics,
            summaries=summaries,
            clip_gradients=clip_gradients,
            clip_embed_gradients=clip_embed_gradients)

    def _preprocess(self, features, labels):
        if isinstance(labels, Mapping):
            labels = labels['label']

        if self.one_hot_encode:
            labels = standard_ops.one_hot(indices=labels, depth=self.n_classes)
        return super(Classifier, self)._preprocess(features, labels)
