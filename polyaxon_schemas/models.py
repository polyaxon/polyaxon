# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema
from polyaxon_schemas.bridges import BridgeSchema
from polyaxon_schemas.graph import GraphSchema
from polyaxon_schemas.losses import LossSchema
from polyaxon_schemas.metrics import MetricSchema
from polyaxon_schemas.optimizers import OptimizerSchema
from polyaxon_schemas.utils import ObjectOrListObject


class BaseModelSchema(Schema):
    graph = fields.Nested(GraphSchema)
    loss = fields.Nested(LossSchema, allow_none=True)
    optimizer = fields.Nested(OptimizerSchema, allow_none=True)
    metrics = fields.Nested(MetricSchema, many=True, allow_none=True)
    summaries = ObjectOrListObject(fields.Str, allow_none=True)
    clip_gradients = fields.Float(allow_none=True)
    clip_embed_gradients = fields.Float(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return BaseModelConfig(**data)

    @post_dump
    def unmake(self, data):
        return BaseModelConfig.remove_reduced_attrs(data)


class BaseModelConfig(BaseConfig):
    SCHEMA = BaseModelSchema
    IDENTIFIER = 'Model'
    REDUCED_ATTRIBUTES = ['name', 'summaries']

    def __init__(self,
                 graph,
                 loss=None,
                 optimizer=None,
                 metrics=None,
                 summaries=None,
                 clip_gradients=0.5,
                 clip_embed_gradients=0.,
                 name=None):
        self.graph = graph
        self.loss = loss
        self.optimizer = optimizer
        self.metrics = metrics
        self.summaries = summaries
        self.clip_gradients = clip_gradients
        self.clip_embed_gradients = clip_embed_gradients
        self.name = name


class ClassifierSchema(BaseModelSchema):
    one_hot_encode = fields.Bool(allow_none=True)
    n_classes = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ClassifierConfig(**data)

    @post_dump
    def unmake(self, data):
        return ClassifierConfig.remove_reduced_attrs(data)


class ClassifierConfig(BaseModelConfig):
    """Classifier base model.

    Args(programmatic):
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        graph_fn: Graph function. Follows the signature:
            * Args:
                * `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
                * `inputs`: the feature inputs.

    Args(polyaxonfile):
        graph: Graph definition. see [Graph]()

    Args(shared):
        loss: An instance of `LossConfig`. Default value `SigmoidCrossEntropyConfig`.
        optimizer: An instance of `OptimizerConfig`.
            Default value `AdamConfig(learning_rate=0.001)`.
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

    Programmatic usage:

    ```python
    def graph_fn(mode, features):
        x = plx.layers.Conv2D(filters=32, kernel_size=5)(features['image'])
        x = plx.layers.MaxPooling2D(pool_size=2)(x)
        x = plx.layers.Conv2D(filters=64, kernel_size=5)(x)
        x = plx.layers.MaxPooling2D(pool_size=2)(x)
        x = plx.layers.Flatten()(x)
        x = plx.layers.Dense(units=10)(x)
        return x

    model = plx.models.Classifier(
        mode=mode,
        graph_fn=graph_fn,
        loss=SigmoidCrossEntropyConfig(),
        optimizer=AdamConfig(
            learning_rate=0.007, decay_type='exponential_decay', decay_rate=0.1),
        metrics=[AccuracyConfig(), PrecisionConfig()],
        summaries='all',
        one_hot_encode=True,
        n_classes=10)
    ```

    Polyaxonfile usage:

    ```yaml
    model:
      classifier:
        loss: SigmoidCrossEntropy
        optimizer:
          Adam:
            learning_rate: 0.007
            decay_type: exponential_decay
            decay_rate: 0.2
        metrics:
          - Accuracy
          - Precision
        one_hot_encode: true
        n_classes: 10
        graph:
          input_layers: image
          layers:
            - Conv2D:
                filters: 32
                kernel_size: 5
                strides: 1
            - MaxPooling2D:
                pool_size: 2
            - Conv2D:
                filters: 64
                kernel_size: 5
            - MaxPooling2D:
                pool_size: 2
            - Flatten:
            - Dense:
                units: 1024
                activation: tanh
            - Dense:
               units: 10
    ```

    or use model_type to reduce the nesting level

    ```yaml
    model:
      model_type: classifier
      loss: SigmoidCrossEntropy
      optimizer:
        Adam:
          learning_rate: 0.007
          decay_type: exponential_decay
          decay_rate: 0.2
      metrics:
        - Accuracy
        - Precision
      one_hot_encode: true
      n_classes: 10
      graph:
        input_layers: image
        layers:
          - Conv2D:
              filters: 32
              kernel_size: 5
              strides: 1
          - MaxPooling2D:
              pool_size: 2
          - Conv2D:
              filters: 64
              kernel_size: 5
          - MaxPooling2D:
              pool_size: 2
          - Flatten:
          - Dense:
              units: 1024
              activation: tanh
          - Dense:
             units: 10
    ```
    """
    SCHEMA = ClassifierSchema
    IDENTIFIER = 'Classifier'

    def __init__(self,
                 graph,
                 loss=None,
                 optimizer=None,
                 metrics=None,
                 summaries=None,
                 clip_gradients=0.5,
                 clip_embed_gradients=0.,
                 one_hot_encode=None,
                 n_classes=None,
                 name=None,):
        super(ClassifierConfig, self).__init__(
            graph=graph,
            loss=loss,
            optimizer=optimizer,
            metrics=metrics,
            summaries=summaries,
            clip_gradients=clip_gradients,
            clip_embed_gradients=clip_embed_gradients,
            name=name)
        self.one_hot_encode = one_hot_encode
        self.n_classes = n_classes


class RegressorSchema(BaseModelSchema):
    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return RegressorConfig(**data)

    @post_dump
    def unmake(self, data):
        return RegressorConfig.remove_reduced_attrs(data)


class RegressorConfig(BaseModelConfig):
    """Regressor base model.

    Args(programmatic):
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        graph_fn: Graph function. Follows the signature:
            * Args:
                * `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
                * `inputs`: the feature inputs.

    Args(polyaxonfile):
        graph: Graph definition. see [Graph]()

    Args(both):
        loss: An instance of `LossConfig`. Default value `MeanSquaredErrorConfig`.
        optimizer: An instance of `OptimizerConfig`.
            Default value `AdamConfig(learning_rate=0.001)`.
        metrics: a list of `MetricConfig` instances.
        summaries: `str` or `list`. The verbosity of the tensorboard visualization.
            Possible values:
             [`all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`]
        clip_gradients: `float`. Gradients  clipping by global norm.
        clip_embed_gradients: `float`. Embedding gradients clipping to a specified value.
        name: `str`, the name of this model, everything will be encapsulated inside this scope.

    Returns:
        `EstimatorSpec`

    Programmatic usage:

    ```python
    def graph_fn(mode, features):
        x = features['x']
        x = plx.layers.LSTM(units=10)(x)
        return plx.layers.Dense(units=1)(x)

    model = plx.models.Regressor(
        mode=mode,
        graph_fn=graph_fn,
        loss=MeanSquaredErrorConfig(),
        optimizer=AdagradConfig(learning_rate=0.1),
        metrics=[
            RootMeanSquaredErrorConfig(),
            MeanAbsoluteErrorConfig()])
    ```

    Polyaxonfile usage:

    ```yaml
    model:
      regressor:
        loss: MeanSquaredError
        optimizer:
          Adagrad:
            learning_rate: 0.1
        metrics:
          - RootMeanSquaredError
          - MeanAbsoluteError
        graph:
          input_layers: x
          layers:
            - LSTM:
                units: 19
            - Dense:
                units: 1
    ```

    or use model_type to reduce the nesting level

    ```yaml
    model:
      model_type: regressor:
      loss: MeanSquaredError
      optimizer:
        Adagrad:
          learning_rate: 0.1
      metrics:
        - RootMeanSquaredError
        - MeanAbsoluteError
      graph:
        input_layers: x
        layers:
          - LSTM:
              units: 19
          - Dense:
              units: 1
    ```
    """
    SCHEMA = RegressorSchema
    IDENTIFIER = 'Regressor'


class GeneratorSchema(BaseModelSchema):
    encoder = fields.Nested(GraphSchema)
    decoder = fields.Nested(GraphSchema)
    bridge = fields.Nested(BridgeSchema)

    class Meta:
        ordered = True
        exclude = ('graph',)

    @post_load
    def make(self, data):
        return GeneratorConfig(**data)

    @post_dump
    def unmake(self, data):
        return GeneratorConfig.remove_reduced_attrs(data)


class GeneratorConfig(BaseModelConfig):
    """Generator base model.

    Args(programmatic):
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
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
    Args(polyaxonfile):
        encoder: Graph definition. see [Graph]()
        decoder: Graph definition. see [Graph]()
        bridge: Graph definition. see [Graph]()

    Args(shared):
        loss: An instance of `LossConfig`. Default value `SigmoidCrossEntropyConfig`.
        optimizer: An instance of `OptimizerConfig`.
            Default value `AdadeltaConfig(learning_rate=0.4)`.
        summaries: `str` or `list`. The verbosity of the tensorboard visualization.
            Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
        metrics: a list of `MetricConfig` instances.
        summaries: `str` or `list`. The verbosity of the tensorboard visualization.
            Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
        clip_gradients: `float`. Gradients  clipping by global norm.
        clip_embed_gradients: `float`. Embedding gradients clipping to a specified value.
        name: `str`, the name of this model, everything will be encapsulated inside this scope.

    Returns:
        `EstimatorSpec`

    Programmatic usage:

    ```python
    def encoder_fn(mode, features):
    x = plx.layers.Dense(units=128)(features)
    x = plx.layers.Dense(units=256)(x)
    return x


    def decoder_fn(mode, features):
        x = plx.layers.Dense(units=256)(features)
        return plx.layers.Dense(units=784)(x)


    def bridge_fn(mode, features, labels, loss, encoder_fn, decoder_fn):
        return plx.bridges.NoOpBridge(mode)(features, labels, loss, encoder_fn, decoder_fn)

    model = plx.models.Generator(
        mode=mode,
        encoder_fn=encoder_fn,
        decoder_fn=decoder_fn,
        bridge_fn=bridge_fn,
        loss=MeanSquaredErrorConfig(),
        optimizer=AdadeltaConfig(learning_rate=0.9),
        summaries=['loss'])
    ```

    Polyaxonfile usage:

    ```yaml
    model:
      generator:
        loss:
          MeanSquaredError:
        optimizer:
          Adam:
            learning_rate: 0.9
        metrics:
          - Accuracy
        bridge: NoOpBridge
        encoder:
          input_layers: image
          layers:
            - Dense:
                units: 128
            - Dense:
                units: 256
                name: encoded
        decoder:
          input_layers: encoded
          layers:
            - Dense:
                units: 256
            - Dense:
                units: 784
    ```

    or use model_type to reduce the nesting level

    ```yaml
    model:
      model_type: generator:
      loss:
        MeanSquaredError:
      optimizer:
        Adam:
          learning_rate: 0.9
      metrics:
        - Accuracy
      bridge: NoOpBridge
      encoder:
        input_layers: image
        layers:
          - Dense:
              units: 128
          - Dense:
              units: 256
              name: encoded
      decoder:
        input_layers: encoded
        layers:
          - Dense:
              units: 256
          - Dense:
              units: 784
    ```
    """
    SCHEMA = GeneratorSchema
    IDENTIFIER = 'Generator'

    def __init__(self,
                 encoder,
                 decoder,
                 bridge,
                 loss=None,
                 optimizer=None,
                 metrics=None,
                 summaries=None,
                 clip_gradients=0.5,
                 clip_embed_gradients=0.,
                 name=None,):
        super(GeneratorConfig, self).__init__(
            graph=None,
            loss=loss,
            optimizer=optimizer,
            metrics=metrics,
            summaries=summaries,
            clip_gradients=clip_gradients,
            clip_embed_gradients=clip_embed_gradients,
            name=name)

        self.encoder = encoder
        self.decoder = decoder
        self.bridge = bridge


class ModelSchema(BaseMultiSchema):
    __multi_schema_name__ = 'model'
    __configs__ = {
        BaseModelConfig.IDENTIFIER: BaseModelConfig,
        ClassifierConfig.IDENTIFIER: ClassifierConfig,
        RegressorConfig.IDENTIFIER: RegressorConfig,
        GeneratorConfig.IDENTIFIER: GeneratorConfig,
    }
    __support_snake_case__ = True


class ModelConfig(BaseConfig):
    SCHEMA = ModelSchema
    IDENTIFIER = 'model'
