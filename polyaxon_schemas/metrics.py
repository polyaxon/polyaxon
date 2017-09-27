# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, validate, post_load

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema
from polyaxon_schemas.utils import Tensor


class BaseMetricSchema(Schema):
    input_layer = Tensor(allow_none=True)
    output_layer = Tensor(allow_none=True)
    weights = fields.Float(allow_none=True)
    name = fields.Str(allow_none=True)


class BaseMetricConfig(BaseConfig):
    REDUCED_ATTRIBUTES = ['input_layer', 'output_layer', 'name']

    def __init__(self, input_layer=None, output_layer=None, weights=None, name=None):
        self.input_layer = input_layer
        self.output_layer = output_layer
        self.weights = weights
        self.name = name


class TruePositivesSchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return TruePositivesConfig(**data)


class TruePositivesConfig(BaseMetricConfig):
    IDENTIFIER = 'TruePositives'
    SCHEMA = TruePositivesSchema


class TrueNegativesSchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return TrueNegativesConfig(**data)


class TrueNegativesConfig(BaseMetricConfig):
    IDENTIFIER = 'TrueNegatives'
    SCHEMA = TrueNegativesSchema


class FalsePositivesSchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return FalsePositivesConfig(**data)


class FalsePositivesConfig(BaseMetricConfig):
    IDENTIFIER = 'FalsePositives'
    SCHEMA = FalsePositivesSchema


class FalseNegativesSchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return FalseNegativesConfig(**data)


class FalseNegativesConfig(BaseMetricConfig):
    IDENTIFIER = 'FalseNegatives'
    SCHEMA = FalseNegativesSchema


class MeanSchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MeanConfig(**data)


class MeanConfig(BaseMetricConfig):
    IDENTIFIER = 'Mean'
    SCHEMA = MeanSchema


class MeanTensorSchema(Schema):
    tensor = Tensor()
    weights = fields.Float(allow_none=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MeanTensorConfig(**data)


class MeanTensorConfig(BaseConfig):
    IDENTIFIER = 'MeanTensor'
    SCHEMA = MeanTensorSchema
    REDUCED_ATTRIBUTES = ['name']

    def __init__(self, tensor, weights=None, name=None):
        self.tensor = tensor
        self.weights = weights
        self.name = name


class AccuracySchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AccuracyConfig(**data)


class AccuracyConfig(BaseMetricConfig):
    IDENTIFIER = 'Accuracy'
    SCHEMA = AccuracySchema


class PrecisionSchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return PrecisionConfig(**data)


class PrecisionConfig(BaseMetricConfig):
    IDENTIFIER = 'Precision'
    SCHEMA = PrecisionSchema


class RecallSchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return RecallConfig(**data)


class RecallConfig(BaseMetricConfig):
    IDENTIFIER = 'Recall'
    SCHEMA = RecallSchema


class AUCSchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AUCConfig(**data)


class AUCConfig(BaseMetricConfig):
    IDENTIFIER = 'AUC'
    SCHEMA = AUCSchema


class SpecificityAtSensitivitySchema(BaseMetricSchema):
    sensitivity = fields.Float(validate=validate.Range(min=0., max=1.))
    num_thresholds = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return SpecificityAtSensitivityConfig(**data)


class SpecificityAtSensitivityConfig(BaseMetricConfig):
    IDENTIFIER = 'SpecificityAtSensitivity'
    SCHEMA = SpecificityAtSensitivitySchema

    def __init__(self,
                 sensitivity,
                 num_thresholds=200,
                 input_layer=None,
                 output_layer=None,
                 weights=None,
                 name=None):
        self.sensitivity = sensitivity
        self.num_thresholds = num_thresholds
        super(SpecificityAtSensitivityConfig, self).__init__(
            input_layer, output_layer, weights, name)


class SensitivityAtSpecificitySchema(BaseMetricSchema):
    specificity = fields.Float(validate=validate.Range(min=0., max=1.))
    num_thresholds = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return SensitivityAtSpecificityConfig(**data)


class SensitivityAtSpecificityConfig(BaseMetricConfig):
    IDENTIFIER = 'SensitivityAtSpecificity'
    SCHEMA = SensitivityAtSpecificitySchema

    def __init__(self,
                 specificity,
                 num_thresholds=200,
                 input_layer=None,
                 output_layer=None,
                 weights=None,
                 name=None):
        self.specificity = specificity
        self.num_thresholds = num_thresholds
        super(SensitivityAtSpecificityConfig, self).__init__(
            input_layer, output_layer, weights, name)


class PrecisionAtThresholdsSchema(BaseMetricSchema):
    thresholds = fields.List(fields.Float(validate=validate.Range(min=0., max=1.)))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return PrecisionAtThresholdsConfig(**data)


class PrecisionAtThresholdsConfig(BaseMetricConfig):
    IDENTIFIER = 'PrecisionAtThresholds'
    SCHEMA = PrecisionAtThresholdsSchema

    def __init__(self,
                 thresholds,
                 input_layer=None,
                 output_layer=None,
                 weights=None,
                 name=None):
        self.thresholds = thresholds
        super(PrecisionAtThresholdsConfig, self).__init__(
            input_layer, output_layer, weights, name)


class RecallAtThresholdsSchema(BaseMetricSchema):
    thresholds = fields.List(fields.Float(validate=validate.Range(min=0., max=1.)))

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return RecallAtThresholdsConfig(**data)


class RecallAtThresholdsConfig(BaseMetricConfig):
    IDENTIFIER = 'RecallAtThresholds'
    SCHEMA = RecallAtThresholdsSchema

    def __init__(self,
                 thresholds,
                 input_layer=None,
                 output_layer=None,
                 weights=None,
                 name=None):
        self.thresholds = thresholds
        super(RecallAtThresholdsConfig, self).__init__(
            input_layer, output_layer, weights, name)


class SparseRecallAtKSchema(BaseMetricSchema):
    k = fields.Int()
    class_id = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return SparseRecallAtKConfig(**data)


class SparseRecallAtKConfig(BaseMetricConfig):
    IDENTIFIER = 'SparseRecallAtK'
    SCHEMA = SparseRecallAtKSchema

    def __init__(self,
                 k,
                 class_id,
                 input_layer=None,
                 output_layer=None,
                 weights=None,
                 name=None):
        self.k = k
        self.class_id = class_id
        super(SparseRecallAtKConfig, self).__init__(
            input_layer, output_layer, weights, name)


class SparsePrecisionAtKSchema(BaseMetricSchema):
    k = fields.Int()
    class_id = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return SparsePrecisionAtKConfig(**data)


class SparsePrecisionAtKConfig(BaseMetricConfig):
    IDENTIFIER = 'SparsePrecisionAtK'
    SCHEMA = SparsePrecisionAtKSchema

    def __init__(self,
                 k,
                 class_id,
                 input_layer=None,
                 output_layer=None,
                 weights=None,
                 name=None):
        self.k = k
        self.class_id = class_id
        super(SparsePrecisionAtKConfig, self).__init__(
            input_layer, output_layer, weights, name)


class MeanAbsoluteErrorSchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MeanAbsoluteErrorConfig(**data)


class MeanAbsoluteErrorConfig(BaseMetricConfig):
    IDENTIFIER = 'MeanAbsoluteError'
    SCHEMA = MeanAbsoluteErrorSchema


class MeanRelativeErrorSchema(BaseMetricSchema):
    normalizer = fields.Str()  # name of the normalizer tensor

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MeanRelativeErrorConfig(**data)


class MeanRelativeErrorConfig(BaseMetricConfig):
    IDENTIFIER = 'MeanRelativeError'
    SCHEMA = MeanRelativeErrorSchema

    def __init__(self,
                 normalizer,
                 input_layer=None,
                 output_layer=None,
                 weights=None,
                 name=None):
        self.normalizer = normalizer
        super(MeanRelativeErrorConfig, self).__init__(
            input_layer, output_layer, weights, name)


class MeanSquaredErrorSchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MeanSquaredErrorConfig(**data)


class MeanSquaredErrorConfig(BaseMetricConfig):
    IDENTIFIER = 'MeanSquaredError'
    SCHEMA = MeanSquaredErrorSchema


class RootMeanSquaredErrorSchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return RootMeanSquaredErrorConfig(**data)


class RootMeanSquaredErrorConfig(BaseMetricConfig):
    IDENTIFIER = 'RootMeanSquaredError'
    SCHEMA = RootMeanSquaredErrorSchema


class CovarianceSchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return CovarianceConfig(**data)


class CovarianceConfig(BaseMetricConfig):
    IDENTIFIER = 'Covariance'
    SCHEMA = CovarianceSchema


class PearsonCorrelationSchema(BaseMetricSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return PearsonCorrelationConfig(**data)


class PearsonCorrelationConfig(BaseMetricConfig):
    IDENTIFIER = 'PearsonCorrelation'
    SCHEMA = PearsonCorrelationSchema


class MeanCosineDistanceSchema(BaseMetricSchema):
    dim = fields.Int()

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MeanCosineDistanceConfig(**data)


class MeanCosineDistanceConfig(BaseMetricConfig):
    IDENTIFIER = 'MeanCosineDistance'
    SCHEMA = MeanCosineDistanceSchema

    def __init__(self,
                 dim,
                 input_layer=None,
                 output_layer=None,
                 weights=None,
                 name=None):
        self.dim = dim
        super(MeanCosineDistanceConfig, self).__init__(
            input_layer, output_layer, weights, name)


class PercentageLessSchema(BaseMetricSchema):
    tensor = fields.Str()
    threshold = fields.Float()

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return PercentageLessConfig(**data)


class PercentageLessConfig(BaseMetricConfig):
    IDENTIFIER = 'PercentageLess'
    SCHEMA = PercentageLessSchema

    def __init__(self,
                 tensor,
                 threshold,
                 input_layer=None,
                 output_layer=None,
                 weights=None,
                 name=None):
        self.tensor = tensor
        self.threshold = threshold
        super(PercentageLessConfig, self).__init__(
            input_layer, output_layer, weights, name)


class MeanIOUSchema(BaseMetricSchema):
    num_classes = fields.Int()

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MeanIOUConfig(**data)


class MeanIOUConfig(BaseMetricConfig):
    IDENTIFIER = 'MeanIOU'
    SCHEMA = MeanIOUSchema

    def __init__(self,
                 num_classes,
                 input_layer=None,
                 output_layer=None,
                 weights=None,
                 name=None):
        self.num_classes = num_classes
        super(MeanIOUConfig, self).__init__(
            input_layer, output_layer, weights, name)


class MetricSchema(BaseMultiSchema):
    __multi_schema_name__ = 'Metric'
    __configs__ = {
        TruePositivesConfig.IDENTIFIER: TruePositivesConfig,
        TrueNegativesConfig.IDENTIFIER: TrueNegativesConfig,
        FalsePositivesConfig.IDENTIFIER: FalsePositivesConfig,
        FalseNegativesConfig.IDENTIFIER: FalseNegativesConfig,
        MeanConfig.IDENTIFIER: MeanConfig,
        MeanTensorConfig.IDENTIFIER: MeanTensorConfig,
        AccuracyConfig.IDENTIFIER: AccuracyConfig,
        PrecisionConfig.IDENTIFIER: PrecisionConfig,
        RecallConfig.IDENTIFIER: RecallConfig,
        AUCConfig.IDENTIFIER: AUCConfig,
        SpecificityAtSensitivityConfig.IDENTIFIER: SpecificityAtSensitivityConfig,
        SensitivityAtSpecificityConfig.IDENTIFIER: SensitivityAtSpecificityConfig,
        PrecisionAtThresholdsConfig.IDENTIFIER: PrecisionAtThresholdsConfig,
        RecallAtThresholdsConfig.IDENTIFIER: RecallAtThresholdsConfig,
        SparseRecallAtKConfig.IDENTIFIER: SparseRecallAtKConfig,
        SparsePrecisionAtKConfig.IDENTIFIER: SparsePrecisionAtKConfig,
        MeanAbsoluteErrorConfig.IDENTIFIER: MeanAbsoluteErrorConfig,
        MeanRelativeErrorConfig.IDENTIFIER: MeanRelativeErrorConfig,
        MeanSquaredErrorConfig.IDENTIFIER: MeanSquaredErrorConfig,
        RootMeanSquaredErrorConfig.IDENTIFIER: RootMeanSquaredErrorConfig,
        CovarianceConfig.IDENTIFIER: CovarianceConfig,
        PearsonCorrelationConfig.IDENTIFIER: PearsonCorrelationConfig,
        MeanCosineDistanceConfig.IDENTIFIER: MeanCosineDistanceConfig,
        PercentageLessConfig.IDENTIFIER: PercentageLessConfig,
        MeanIOUConfig.IDENTIFIER: MeanIOUConfig,
    }
