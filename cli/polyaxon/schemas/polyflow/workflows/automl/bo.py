#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

import six

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.polyflow.workflows.matrix import MatrixSchema
from polyaxon.schemas.polyflow.workflows.metrics import SearchMetricSchema


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


class GaussianProcessSchema(BaseSchema):
    kernel = fields.Str(
        allow_none=True, validate=validate.OneOf(GaussianProcessesKernels.VALUES)
    )
    length_scale = fields.Float(allow_none=True)
    nu = fields.Float(allow_none=True)
    n_restarts_optimizer = fields.Int(allow_none=True)

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
        n_restarts_optimizer=0,
    ):
        self.kernel = kernel
        self.length_scale = length_scale
        self.nu = nu
        self.n_restarts_optimizer = n_restarts_optimizer


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


class UtilityFunctionSchema(BaseSchema):
    acquisition_function = fields.Str(
        allow_none=True, validate=validate.OneOf(AcquisitionFunctions.VALUES)
    )
    gaussian_process = fields.Nested(GaussianProcessSchema, allow_none=True)
    kappa = fields.Float(allow_none=True)
    eps = fields.Float(allow_none=True)
    n_warmup = fields.Int(allow_none=True)
    n_iter = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return UtilityFunctionConfig

    @validates_schema
    def validate_utility_function(self, data):
        validate_utility_function(
            acquisition_function=data.get("acquisition_function"),
            kappa=data.get("kappa"),
            eps=data.get("eps"),
        )


class UtilityFunctionConfig(BaseConfig):
    SCHEMA = UtilityFunctionSchema
    IDENTIFIER = "utility_function"
    REDUCED_ATTRIBUTES = ["n_warmup", "n_iter"]

    def __init__(
        self,
        acquisition_function=AcquisitionFunctions.UCB,
        gaussian_process=None,
        kappa=None,
        eps=None,
        n_warmup=None,
        n_iter=None,
    ):
        validate_utility_function(
            acquisition_function=acquisition_function, kappa=kappa, eps=eps
        )

        self.acquisition_function = acquisition_function
        self.gaussian_process = gaussian_process
        self.kappa = kappa
        self.eps = eps
        self.n_warmup = n_warmup
        self.n_iter = n_iter


def validate_matrix(matrix):
    if not matrix:
        return None

    for key, value in six.iteritems(matrix):
        if value.is_distribution and not value.is_uniform:
            raise ValidationError(
                "`{}` defines a non uniform distribution, "
                "and it cannot be used with bayesian optimization.".format(key)
            )

    return matrix


class BOSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("bo"))
    utility_function = fields.Nested(UtilityFunctionSchema, allow_none=True)
    n_initial_trials = RefOrObject(fields.Int(), required=True)
    n_iterations = RefOrObject(fields.Int(), required=True)
    metric = fields.Nested(SearchMetricSchema, required=True)
    matrix = fields.Dict(
        keys=fields.Str(), values=fields.Nested(MatrixSchema), required=True
    )
    seed = RefOrObject(fields.Int(allow_none=True))

    @staticmethod
    def schema_config():
        return BOConfig

    @validates_schema
    def validate_matrix(self, data):
        """Validates matrix data and creates the config objects"""
        validate_matrix(data.get("matrix"))


class BOConfig(BaseConfig):
    SCHEMA = BOSchema
    IDENTIFIER = "bo"

    def __init__(
        self,
        matrix,
        n_initial_trials,
        n_iterations,
        metric,
        utility_function=None,
        seed=None,
        kind=IDENTIFIER,
    ):
        self.matrix = validate_matrix(matrix)
        self.kind = kind
        self.n_initial_trials = n_initial_trials
        self.n_iterations = n_iterations
        self.utility_function = utility_function
        self.metric = metric
        self.seed = seed
