#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import polyaxon_sdk

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon.polyflow.early_stopping import EarlyStoppingSchema
from polyaxon.polyflow.optimization import OptimizationMetricSchema
from polyaxon.polyflow.parallel.matrix import MatrixSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class AcquisitionFunctions(object):
    UCB = "ucb"
    EI = "ei"
    POI = "poi"

    UCB_VALUES = [UCB, UCB.upper(), UCB.capitalize()]
    EI_VALUES = [EI, EI.upper(), EI.capitalize()]
    POI_VALUES = [POI, POI.upper(), POI.capitalize()]

    VALUES = UCB_VALUES + EI_VALUES + POI_VALUES

    @classmethod
    def is_ucb(cls, value):
        return value in cls.UCB_VALUES

    @classmethod
    def is_ei(cls, value):
        return value in cls.EI_VALUES

    @classmethod
    def is_poi(cls, value):
        return value in cls.POI_VALUES


class GaussianProcessesKernels(object):
    RBF = "rbf"
    MATERN = "matern"

    RBF_VALUES = [RBF, RBF.upper(), RBF.capitalize()]
    MATERN_VALUES = [MATERN, MATERN.upper(), MATERN.capitalize()]

    VALUES = RBF_VALUES + MATERN_VALUES

    @classmethod
    def is_rbf(cls, value):
        return value in cls.RBF_VALUES

    @classmethod
    def is_mattern(cls, value):
        return value in cls.MATERN_VALUES


class GaussianProcessSchema(BaseCamelSchema):
    kernel = fields.Str(
        allow_none=True, validate=validate.OneOf(GaussianProcessesKernels.VALUES)
    )
    length_scale = fields.Float(allow_none=True)
    nu = fields.Float(allow_none=True)
    num_restarts_optimizer = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return GaussianProcessConfig


class GaussianProcessConfig(BaseConfig):
    SCHEMA = GaussianProcessSchema
    IDENTIFIER = "gaussian_process"

    def __init__(
        self,
        kernel=GaussianProcessesKernels.MATERN,
        length_scale=1.0,
        nu=1.5,
        num_restarts_optimizer=0,
    ):
        self.kernel = kernel
        self.length_scale = length_scale
        self.nu = nu
        self.num_restarts_optimizer = num_restarts_optimizer


def validate_utility_function(acquisition_function, kappa, eps):
    condition = AcquisitionFunctions.is_ucb(acquisition_function) and kappa is None
    if condition:
        raise ValidationError(
            "the acquisition function `ucb` requires a parameter `kappa`"
        )

    condition = (
        AcquisitionFunctions.is_ei(acquisition_function)
        or AcquisitionFunctions.is_poi(acquisition_function)
    ) and eps is None
    if condition:
        raise ValidationError(
            "the acquisition function `{}` requires a parameter `eps`".format(
                acquisition_function
            )
        )


class UtilityFunctionSchema(BaseCamelSchema):
    acquisition_function = fields.Str(
        allow_none=True, validate=validate.OneOf(AcquisitionFunctions.VALUES)
    )
    gaussian_process = fields.Nested(GaussianProcessSchema, allow_none=True)
    kappa = fields.Float(allow_none=True)
    eps = fields.Float(allow_none=True)
    num_warmup = fields.Int(allow_none=True)
    num_iterations = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return UtilityFunctionConfig

    @validates_schema
    def validate_utility_function(self, data, **kwargs):
        validate_utility_function(
            acquisition_function=data.get("acquisition_function"),
            kappa=data.get("kappa"),
            eps=data.get("eps"),
        )


class UtilityFunctionConfig(BaseConfig):
    SCHEMA = UtilityFunctionSchema
    IDENTIFIER = "utility_function"
    REDUCED_ATTRIBUTES = ["numWarmup", "numIterations"]

    def __init__(
        self,
        acquisition_function=AcquisitionFunctions.UCB,
        gaussian_process=None,
        kappa=None,
        eps=None,
        num_warmup=None,
        num_iterations=None,
    ):
        validate_utility_function(
            acquisition_function=acquisition_function, kappa=kappa, eps=eps
        )

        self.acquisition_function = acquisition_function
        self.gaussian_process = gaussian_process
        self.kappa = kappa
        self.eps = eps
        self.num_warmup = num_warmup
        self.num_iterations = num_iterations


def validate_matrix(matrix):
    if not matrix:
        return None

    for key, value in matrix.items():
        if value.is_distribution and not value.is_uniform:
            raise ValidationError(
                "`{}` defines a non uniform distribution, "
                "and it cannot be used with bayesian optimization.".format(key)
            )

    return matrix


class BayesSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("bayes"))
    utility_function = fields.Nested(UtilityFunctionSchema, allow_none=True)
    num_initial_runs = RefOrObject(fields.Int(), required=True)
    num_iterations = RefOrObject(fields.Int(), required=True)
    metric = fields.Nested(OptimizationMetricSchema, required=True)
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(MatrixSchema), required=True
    )
    seed = RefOrObject(fields.Int(allow_none=True))
    concurrency = fields.Int(allow_none=True)
    early_stopping = fields.Nested(EarlyStoppingSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return V1Bayes

    @validates_schema
    def validate_matrix(self, data, **kwargs):
        """Validates matrix data and creates the config objects"""
        validate_matrix(data.get("params"))


class V1Bayes(BaseConfig, polyaxon_sdk.V1Bayes):
    SCHEMA = BayesSchema
    IDENTIFIER = "bayes"
    REDUCED_ATTRIBUTES = ["seed", "concurrency", "earlyStopping"]
