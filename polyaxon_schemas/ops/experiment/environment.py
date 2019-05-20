# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.ops.environments.pods import EnvironmentConfig, EnvironmentSchema


class TensorflowClusterSchema(BaseSchema):
    master = fields.List(fields.Str(), allow_none=True)
    worker = fields.List(fields.Str(), allow_none=True)
    ps = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return TensorflowClusterConfig


class TensorflowClusterConfig(BaseConfig):
    """
    Tensorflow cluster config.

    Args:
        master: list(str). The list of master host in a tensorflow cluster.
        worker: list(str). The list of worker host in a tensorflow cluster.
        ps: list(str). The list of ps host in a tensorflow cluster.
    """
    IDENTIFIER = 'tensorflow_cluster'
    SCHEMA = TensorflowClusterSchema

    def __init__(self, master=None, worker=None, ps=None):
        self.master = master
        self.worker = worker
        self.ps = ps


class HorovodClusterSchema(BaseSchema):
    master = fields.List(fields.Str(), allow_none=True)
    worker = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return HorovodClusterConfig


class HorovodClusterConfig(BaseConfig):
    """
    Horovod cluster config.

    Args:
        master: list(str). The list of master host in a Horovod cluster.
        worker: list(str). The list of worker host in a Horovod cluster.
    """
    IDENTIFIER = 'horovod_cluster'
    SCHEMA = HorovodClusterSchema

    def __init__(self, master=None, worker=None):
        self.master = master
        self.worker = worker


class PytorchClusterSchema(BaseSchema):
    master = fields.List(fields.Str(), allow_none=True)
    worker = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return PytorchClusterConfig


class PytorchClusterConfig(BaseConfig):
    """
    Pytorch cluster config.

    Args:
        master: list(str). The list of master host in a Pytorch cluster.
        worker: list(str). The list of worker host in a Pytorch cluster.
    """
    IDENTIFIER = 'pytorch_cluster'
    SCHEMA = PytorchClusterSchema

    def __init__(self, master=None, worker=None):
        self.master = master
        self.worker = worker


class MPIClusterSchema(BaseSchema):
    worker = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return MPIClusterConfig


class MPIClusterConfig(BaseConfig):
    """
    MPI cluster config.

    Args:
        worker: list(str). The list of worker host in a Horovod cluster.
    """
    IDENTIFIER = 'mpi_cluster'
    SCHEMA = MPIClusterSchema

    def __init__(self, worker=None):
        self.worker = worker


class MXNetClusterSchema(BaseSchema):
    master = fields.List(fields.Str(), allow_none=True)
    worker = fields.List(fields.Str(), allow_none=True)
    server = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return MXNetClusterConfig


class MXNetClusterConfig(BaseConfig):
    """
    MXNet cluster config.

    Args:
        master: list(str). The list of master host in a mxnet cluster.
        worker: list(str). The list of worker host in a mxnet cluster.
        server: list(str). The list of server host in a mxnet cluster.
    """
    IDENTIFIER = 'mxnet_cluster'
    SCHEMA = MXNetClusterSchema

    def __init__(self, master=None, worker=None, server=None):
        self.master = master
        self.worker = worker
        self.server = server


class FrameworkEnvironmentMixin(object):
    @staticmethod
    def _get_env_indexed_property(obj, getter):
        if not obj:
            return {}
        return {o.index: getter(o) for o in obj if getter(o)}

    # @property
    # def default_worker_config(self):
    #     return self.default_worker.config if self.default_worker else None

    @property
    def default_worker_resources(self):
        return self.default_worker.resources if self.default_worker else None

    @property
    def default_worker_node_selector(self):
        return self.default_worker.node_selector if self.default_worker else None

    @property
    def default_worker_affinity(self):
        return self.default_worker.affinity if self.default_worker else None

    @property
    def default_worker_tolerations(self):
        return self.default_worker.tolerations if self.default_worker else None

    # @property
    # def default_ps_config(self):
    #     return self.default_ps.config if self.default_ps else None

    @property
    def default_ps_resources(self):
        return self.default_ps.resources if self.default_ps else None

    @property
    def default_ps_node_selector(self):
        return self.default_ps.node_selector if self.default_ps else None

    @property
    def default_ps_affinity(self):
        return self.default_ps.affinity if self.default_ps else None

    @property
    def default_ps_tolerations(self):
        return self.default_ps.tolerations if self.default_ps else None

    # @property
    # def worker_configs(self):
    #     return self._get_env_indexed_property(obj=self.worker, getter=lambda o: o.config)

    @property
    def worker_resources(self):
        return self._get_env_indexed_property(obj=self.worker, getter=lambda o: o.resources)

    @property
    def worker_node_selectors(self):
        return self._get_env_indexed_property(obj=self.worker, getter=lambda o: o.node_selector)

    @property
    def worker_affinities(self):
        return self._get_env_indexed_property(obj=self.worker, getter=lambda o: o.affinity)

    @property
    def worker_tolerations(self):
        return self._get_env_indexed_property(obj=self.worker, getter=lambda o: o.tolerations)

    # @property
    # def ps_configs(self):
    #     return self._get_env_indexed_property(obj=self.ps, getter=lambda o: o.config)

    @property
    def ps_resources(self):
        return self._get_env_indexed_property(obj=self.ps, getter=lambda o: o.resources)

    @property
    def ps_node_selectors(self):
        return self._get_env_indexed_property(obj=self.ps, getter=lambda o: o.node_selector)

    @property
    def ps_affinities(self):
        return self._get_env_indexed_property(obj=self.ps, getter=lambda o: o.affinity)

    @property
    def ps_tolerations(self):
        return self._get_env_indexed_property(obj=self.ps, getter=lambda o: o.tolerations)


class TensorflowSchema(BaseSchema):
    n_workers = fields.Int(allow_none=True)
    n_ps = fields.Int(allow_none=True)
    delay_workers_by_global_step = fields.Bool(allow_none=True)
    default_worker = fields.Nested(EnvironmentSchema, allow_none=True)
    default_ps = fields.Nested(EnvironmentSchema, allow_none=True)
    worker = fields.Nested(EnvironmentSchema, many=True, allow_none=True)
    ps = fields.Nested(EnvironmentSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return TensorflowConfig


class TensorflowConfig(BaseConfig, FrameworkEnvironmentMixin):
    """
    Tensorflow environment config.

    Args:
        n_workers: `int`. The number of workers requested for training the model.
        n_ps: `int`. The number of ps requested for training the model.
        default_worker: `PodEnvironment`. The default pod environment to use for all workers.
        default_ps: `PodEnvironment`. The default pod environment to use for all ps.
        worker: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific worker.
        ps: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific ps.
    """
    IDENTIFIER = 'tensorflow'
    SCHEMA = TensorflowSchema

    def __init__(self,
                 n_workers=0,
                 n_ps=0,
                 delay_workers_by_global_step=False,
                 run_config=None,
                 default_worker=None,
                 default_ps=None,
                 worker=None,
                 ps=None,
                 ):
        self.n_workers = n_workers
        self.n_ps = n_ps
        self.delay_workers_by_global_step = delay_workers_by_global_step
        self.run_config = run_config
        self.default_worker = default_worker
        self.default_ps = default_ps
        self.worker = worker
        self.ps = ps


class HorovodSchema(BaseSchema):
    n_workers = fields.Int(allow_none=True)
    default_worker = fields.Nested(EnvironmentSchema, allow_none=True)
    worker = fields.Nested(EnvironmentSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return HorovodConfig


class HorovodConfig(BaseConfig, FrameworkEnvironmentMixin):
    """
    Horovod environment config.

    Args:
        n_workers: `int`. The number of workers requested for training the model.
        default_worker: `PodEnvironment`. The default pod environment to use for all workers.
        worker: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific worker.
    """
    IDENTIFIER = 'horovod'
    SCHEMA = HorovodSchema

    def __init__(self,
                 n_workers=0,
                 default_worker=None,
                 worker=None,
                 ):
        self.n_workers = n_workers
        self.default_worker = default_worker
        self.worker = worker


class MPISchema(BaseSchema):
    n_workers = fields.Int(allow_none=True)
    default_worker = fields.Nested(EnvironmentSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return MPIConfig


class MPIConfig(BaseConfig, FrameworkEnvironmentMixin):
    """
    MPI job environment config.

    Args:
        n_workers: `int`. The number of workers requested for training the model.
        default_worker: `PodEnvironment`. The default pod environment to use for all workers.
    """
    IDENTIFIER = 'mpi'
    SCHEMA = MPISchema

    def __init__(self,
                 n_workers=0,
                 default_worker=None,
                 ):
        self.n_workers = n_workers
        self.default_worker = default_worker
        self.worker = None


class PytorchSchema(BaseSchema):
    n_workers = fields.Int(allow_none=True)
    default_worker = fields.Nested(EnvironmentSchema, allow_none=True)
    worker = fields.Nested(EnvironmentSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return PytorchConfig


class PytorchConfig(BaseConfig, FrameworkEnvironmentMixin):
    """
    Pytorch environment config.

    Args:
        n_workers: `int`. The number of workers requested for training the model.
        default_worker: `PodEnvironment`. The default pod environment to use for all workers.
        worker: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific worker.
    """
    IDENTIFIER = 'pytorch'
    SCHEMA = PytorchSchema

    def __init__(self,
                 n_workers=0,
                 default_worker=None,
                 worker=None,
                 ):
        self.n_workers = n_workers
        self.default_worker = default_worker
        self.worker = worker


class MXNetSchema(BaseSchema):
    n_workers = fields.Int(allow_none=True)
    n_ps = fields.Int(allow_none=True)
    default_worker = fields.Nested(EnvironmentSchema, allow_none=True)
    default_ps = fields.Nested(EnvironmentSchema, allow_none=True)
    worker = fields.Nested(EnvironmentSchema, many=True, allow_none=True)
    ps = fields.Nested(EnvironmentSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return MXNetConfig


class MXNetConfig(BaseConfig, FrameworkEnvironmentMixin):
    """
    MXNet environment config.

    Args:
        n_workers: `int`. The number of workers requested for training the model.
        n_ps: `int`. The number of ps requested for training the model.
        default_worker: `PodEnvironment`. The default pod environment to use for all workers.
        default_ps: `PodEnvironment`. The default pod environment to use for all ps.
        worker: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific worker.
        ps: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific ps.
    """
    IDENTIFIER = 'mxnet'
    SCHEMA = MXNetSchema

    def __init__(self,
                 n_workers=0,
                 n_ps=0,
                 default_worker=None,
                 default_ps=None,
                 worker=None,
                 ps=None,
                 ):
        self.n_workers = n_workers
        self.n_ps = n_ps
        self.default_worker = default_worker
        self.default_ps = default_ps
        self.worker = worker
        self.ps = ps


class ReplicasSchema(BaseSchema):
    n_workers = fields.Int(allow_none=True)
    n_ps = fields.Int(allow_none=True)
    default_worker = fields.Nested(EnvironmentSchema, allow_none=True)
    default_ps = fields.Nested(EnvironmentSchema, allow_none=True)
    worker = fields.Nested(EnvironmentSchema, many=True, allow_none=True)
    ps = fields.Nested(EnvironmentSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return ReplicasConfig


class ReplicasConfig(BaseConfig):
    """
    Replicas environment config.

    Args:
        n_workers: `int`. The number of workers requested for training the model.
        n_ps: `int`. The number of ps requested for training the model.
        default_worker: `PodEnvironment`. The default pod environment to use for all workers.
        default_ps: `PodEnvironment`. The default pod environment to use for all ps.
        worker: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific worker.
        ps: `list(PodEnvironment)`. The pod environment with index specified to use
            for the specific ps.
    """
    IDENTIFIER = 'replicas'
    SCHEMA = ReplicasSchema
    REDUCED_ATTRIBUTES = ['n_workers', 'n_ps', 'default_worker', 'default_ps', 'worker', 'ps']

    def __init__(self,
                 n_workers=None,
                 n_ps=None,
                 default_worker=None,
                 default_ps=None,
                 worker=None,
                 ps=None,
                 ):
        self.n_workers = n_workers
        self.n_ps = n_ps
        self.default_worker = default_worker
        self.default_ps = default_ps
        self.worker = worker
        self.ps = ps


class ExperimentEnvironmentSchema(EnvironmentSchema):
    replicas = fields.Nested(ReplicasSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return ExperimentEnvironmentConfig


class ExperimentEnvironmentConfig(EnvironmentConfig):
    """
    Environment config.

    Args:
        resources: `PodResourcesConfig`. The resources config definition.
        node_selector: `dict`.
        affinity: `dict`.
        tolerations: `list(dict)`.
        replicas: `ReplicasConfig`.
    """
    IDENTIFIER = 'environment'
    SCHEMA = ExperimentEnvironmentSchema
    REDUCED_ATTRIBUTES = EnvironmentConfig.REDUCED_ATTRIBUTES + ['replicas']

    def __init__(self,
                 index=None,
                 resources=None,
                 node_selector=None,
                 affinity=None,
                 tolerations=None,
                 service_account=None,
                 image_pull_secrets=None,
                 max_restarts=None,
                 secret_refs=None,
                 config_map_refs=None,
                 configmap_refs=None,
                 data_refs=None,
                 artifact_refs=None,
                 outputs=None,
                 persistence=None,
                 replicas=None):
        super(ExperimentEnvironmentConfig, self).__init__(
            index=index,
            resources=resources,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            service_account=service_account,
            image_pull_secrets=image_pull_secrets,
            max_restarts=max_restarts,
            secret_refs=secret_refs,
            config_map_refs=config_map_refs,
            configmap_refs=configmap_refs,
            data_refs=data_refs,
            artifact_refs=artifact_refs,
            persistence=persistence,
            outputs=outputs,
        )
        self.replicas = replicas
