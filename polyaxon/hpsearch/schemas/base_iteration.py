from marshmallow import Schema, fields, post_dump, post_load

from schemas.base import BaseConfig


class BaseIterationSchema(Schema):
    iteration = fields.Int()
    num_suggestions = fields.Int()
    experiment_ids = fields.List(fields.Int(), allow_none=True)

    @post_load
    def make(self, data):
        return BaseIterationConfig(**data)

    @post_dump
    def unmake(self, data):
        return BaseIterationConfig.remove_reduced_attrs(data)


class BaseIterationConfig(BaseConfig):
    SCHEMA = BaseIterationSchema

    def __init__(self, iteration, num_suggestions, experiment_ids=None):
        self.iteration = iteration
        self.num_suggestions = num_suggestions
        self.experiment_ids = experiment_ids
