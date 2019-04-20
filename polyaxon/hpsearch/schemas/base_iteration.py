from marshmallow import fields

from schemas import BaseConfig, BaseSchema


class BaseIterationSchema(BaseSchema):
    iteration = fields.Int()
    num_suggestions = fields.Int()
    experiment_ids = fields.List(fields.Int(), allow_none=True)

    @staticmethod
    def schema_config():
        return BaseIterationConfig


class BaseIterationConfig(BaseConfig):
    SCHEMA = BaseIterationSchema

    def __init__(self, iteration, num_suggestions, experiment_ids=None):
        self.iteration = iteration
        self.num_suggestions = num_suggestions
        self.experiment_ids = experiment_ids
