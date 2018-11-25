from marshmallow import fields, post_dump, post_load, validate

from hpsearch.schemas.base_iteration import BaseIterationSchema, BaseIterationConfig


class HyperbandIterationSchema(BaseIterationSchema):
    bracket_iteration = fields.Int()
    experiments_metrics = fields.List(fields.List(fields.Raw(), validate=validate.Length(equal=2)),
                                      allow_none=True)

    @post_load
    def make(self, data):
        return HyperbandIterationConfig(**data)

    @post_dump
    def unmake(self, data):
        return HyperbandIterationConfig.remove_reduced_attrs(data)


class HyperbandIterationConfig(BaseIterationConfig):
    SCHEMA = HyperbandIterationSchema

    def __init__(self,
                 iteration,
                 num_suggestions,
                 bracket_iteration,
                 experiment_ids=None,
                 experiments_metrics=None):
        super().__init__(iteration=iteration,
                         num_suggestions=num_suggestions,
                         experiment_ids=experiment_ids)
        self.bracket_iteration = bracket_iteration
        self.experiments_metrics = experiments_metrics
