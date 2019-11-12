from marshmallow import fields, validate

from polyaxon.schemas.base import BaseConfig, BaseSchema


class BaseIterationSchema(BaseSchema):
    iteration = fields.Int()
    configs = fields.List(
        fields.List(fields.Raw(), validate=validate.Length(equal=2)), allow_none=True
    )
    metrics = fields.List(
        fields.List(fields.Raw(), validate=validate.Length(equal=2)), allow_none=True
    )

    @staticmethod
    def schema_config():
        return BaseIterationConfig


class BaseIterationConfig(BaseConfig):
    SCHEMA = BaseIterationSchema

    def __init__(self, iteration, configs, metrics):
        self.iteration = iteration
        self.configs = configs
        self.metrics = metrics
