# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

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
    def make_load(self, data):
        return BaseModelConfig(**data)


class BaseModelConfig(BaseConfig):
    SCHEMA = BaseModelSchema
    IDENTIFIER = 'Model'
    REDUCED_ATTRIBUTES = ['name', 'summaries']

    def __init__(self, graph, loss=None, optimizer=None, metrics=None, summaries=None,
                 clip_gradients=0.5, clip_embed_gradients=0., name=None):
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
    def make_load(self, data):
        return ClassifierConfig(**data)


class ClassifierConfig(BaseModelConfig):
    SCHEMA = ClassifierSchema
    IDENTIFIER = 'Classifier'

    def __init__(self, graph, one_hot_encode=None, n_classes=None, **kwargs):
        super(ClassifierConfig, self).__init__(graph, **kwargs)
        self.one_hot_encode = one_hot_encode
        self.n_classes = n_classes


class RegressorSchema(BaseModelSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return RegressorConfig(**data)


class RegressorConfig(BaseModelConfig):
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
    def make_load(self, data):
        return GeneratorConfig(**data)


class GeneratorConfig(BaseModelConfig):
    SCHEMA = GeneratorSchema
    IDENTIFIER = 'Generator'

    def __init__(self, encoder, decoder, bridge, **kwargs):
        super(GeneratorConfig, self).__init__(None, **kwargs)
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
