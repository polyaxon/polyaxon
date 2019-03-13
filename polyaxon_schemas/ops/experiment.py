# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.ml.eval import EvalSchema
from polyaxon_schemas.ml.models import ModelSchema
from polyaxon_schemas.ml.train import TrainSchema
from polyaxon_schemas.ops.environments.experiments import (
    ExperimentEnvironmentSchema,
    HorovodConfig,
    MPIConfig,
    MXNetConfig,
    PytorchConfig,
    TensorflowConfig
)
from polyaxon_schemas.ops.run import BaseRunConfig, BaseRunSchema
from polyaxon_schemas.ops.run_exec import RunSchema
from polyaxon_schemas.utils import ExperimentBackend, ExperimentFramework


def validate_backend(backend):
    if backend and backend not in ExperimentBackend.VALUES:
        raise ValidationError('Experiment backend `{}` not supported'.format(backend))


def validate_replicas(framework, replicas):
    if replicas and framework and framework not in ExperimentFramework.VALUES:
        raise ValidationError(
            'Distributed Experiment framework `{}` not supported'.format(framework))

    if replicas and not framework:
        raise ValidationError(
            'You must specify which framework to use for distributed experiments.')

    config = replicas.to_light_dict() if isinstance(replicas, BaseConfig) else replicas

    if framework == 'tensorflow':
        TensorflowConfig.from_dict(config)
    if framework == 'horovod':
        HorovodConfig.from_dict(config)
    if framework == 'mpi':
        MPIConfig.from_dict(config)
    if framework == 'mxnet':
        MXNetConfig.from_dict(config)
    if framework == 'pytorch':
        PytorchConfig.from_dict(config)


class ExperimentSchema(BaseRunSchema):
    kind = fields.Str(allow_none=None, validate=validate.Equal('experiment'))
    declarations = fields.Raw(allow_none=True)
    environment = fields.Nested(ExperimentEnvironmentSchema, allow_none=True)
    backend = fields.Str(allow_none=True, validate=validate.OneOf(ExperimentBackend.VALUES))
    framework = fields.Str(allow_none=True)
    run = fields.Nested(RunSchema, allow_none=True)
    model = fields.Nested(ModelSchema, allow_none=True)
    train = fields.Nested(TrainSchema, allow_none=True)
    eval = fields.Nested(EvalSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return ExperimentConfig

    @validates_schema
    def validate_backend(self, data):
        """Validate backend"""
        validate_backend(data.get('backend'))

    @validates_schema
    def validate_replicas(self, data):
        """Validate distributed experiment"""
        environment = data.get('environment')
        if environment and environment.replicas:
            validate_replicas(data.get('framework'), environment.replicas)


class ExperimentConfig(BaseRunConfig):
    SCHEMA = ExperimentSchema
    IDENTIFIER = 'experiment'
    REDUCED_ATTRIBUTES = BaseRunConfig.REDUCED_ATTRIBUTES + ['backend', 'framework']

    def __init__(self,
                 kind=None,
                 version=None,
                 logging=None,
                 tags=None,
                 declarations=None,
                 environment=None,
                 build=None,
                 backend=None,
                 framework=None,
                 run=None,
                 model=None,
                 train=None,
                 eval=None,  # pylint:disable=redefined-builtin
                 ):
        validate_backend(backend)
        self.replicas = None
        if framework and environment and environment.replicas:
            validate_replicas(framework, environment.replicas)
            self.replicas = environment.replicas

        super(ExperimentConfig, self).__init__(kind=kind,
                                               version=version,
                                               logging=logging,
                                               tags=tags,
                                               environment=environment,
                                               build=build)
        self.backend = backend
        self.framework = framework
        self.declarations = declarations
        self.run = run
        self.model = model
        self.train = train
        self.eval = eval  # pylint:disable=redefined-builtin
        self.tensorflow = self.get_tensorflow()
        self.horovod = self.get_horovod()
        self.mxnet = self.get_mxnet()
        self.pytorch = self.get_pytorch()
        self.mpi = self.get_mpi()

    def has_framework(self, framework):
        return (
            self.framework == framework and
            self.replicas and
            self.backend != ExperimentBackend.MPI
        )

    def get_tensorflow(self):
        if self.has_framework(framework=ExperimentFramework.TENSORFLOW):
            return TensorflowConfig.from_dict(self.replicas.to_light_dict())

    def get_horovod(self):
        if self.has_framework(framework=ExperimentFramework.HOROVOD):
            return HorovodConfig.from_dict(self.replicas.to_light_dict())

    def get_mxnet(self):
        if self.has_framework(framework=ExperimentFramework.MXNET):
            return MXNetConfig.from_dict(self.replicas.to_light_dict())

    def get_pytorch(self):
        if self.has_framework(framework=ExperimentFramework.PYTORCH):
            return PytorchConfig.from_dict(self.replicas.to_light_dict())

    def get_mpi(self):
        if self.backend == ExperimentBackend.MPI and self.replicas:
            return MPIConfig.from_dict(self.replicas.to_light_dict())
