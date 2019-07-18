import uuid

import pytest

from db.models.experiment_jobs import ExperimentJob
from factories.factory_experiments import ExperimentFactory
from polypod.experiment import ExperimentSpawner
from polypod.horovod import HorovodSpawner
from polypod.mpi_job import MPIJobSpawner
from polypod.mxnet import MXNetSpawner
from polypod.pytorch import PytorchSpawner
from polypod.pytorch_job import PytorchJobSpawner
from polypod.tensorflow import TensorflowSpawner
from polypod.tf_job import TFJobSpawner
from scheduler.experiment_scheduler import create_job, get_spawner_class, set_job_definition
from schemas import ExperimentBackend, ExperimentFramework, TaskType
from tests.base.case import BaseTest


@pytest.mark.scheduler_mark
class TestExperimentScheduler(BaseTest):

    def test_create_job(self):
        experiment = ExperimentFactory()
        assert ExperimentJob.objects.count() == 0

        node_selector = {'polyaxon': 'selector'}
        affinity = {
            'podAffinity': {
                'preferredDuringSchedulingIgnoredDuringExecution': [
                    {
                        'podAffinityTerm': {
                            'topologyKey': 'kubernetes.io/hostname', 'labelSelector': {
                                'matchExpressions': [
                                    {'operator': 'In',
                                     'key': 'polyaxon',
                                     'values': ['high-cpu']
                                     }]}},
                        'weight': 100
                    }
                ]
            }
        }
        tolerations = [
            {'operator': 'Equal', 'effect': 'NoSchedule', 'key': 'polyaxon', 'value': 'somevalue'}
        ]

        create_job(job_uuid=uuid.uuid4().hex,
                   experiment=experiment,
                   node_selector=node_selector,
                   affinity=affinity,
                   tolerations=tolerations)
        assert ExperimentJob.objects.count() == 1
        job = ExperimentJob.objects.last()
        assert job.role == TaskType.MASTER
        assert job.resources is None
        assert job.node_selector == node_selector
        assert job.affinity == affinity
        assert job.tolerations == tolerations

    def test_set_job_definition(self):
        experiment = ExperimentFactory()
        job_uuid = uuid.uuid4().hex
        create_job(job_uuid=job_uuid,
                   experiment=experiment)
        job = ExperimentJob.objects.last()
        assert job.role == TaskType.MASTER
        assert job.resources is None
        assert job.node_selector is None
        assert job.affinity is None
        assert job.tolerations is None
        assert job.definition == {}
        definition = {'spec': {}}
        set_job_definition(job_uuid=job_uuid, definition=definition)
        job = ExperimentJob.objects.last()
        assert job.definition == definition

    def test_get_spawner_class(self):
        class DummySpec(object):
            def __init__(self, framework=None, backend=None, is_distributed=False):
                self.framework = framework
                self.backend = backend
                self.is_distributed = is_distributed

            @property
            def cluster_def(self):
                return None, self.is_distributed

        tf_spec = DummySpec(framework=ExperimentFramework.TENSORFLOW,
                            backend=ExperimentBackend.NATIVE)
        assert get_spawner_class(specification=tf_spec) == ExperimentSpawner
        tf_spec.is_distributed = True
        assert get_spawner_class(specification=tf_spec) == TensorflowSpawner
        tf_spec.backend = ExperimentBackend.KUBEFLOW
        assert get_spawner_class(specification=tf_spec) == TFJobSpawner
        tf_spec.backend = ExperimentBackend.MPI
        assert get_spawner_class(specification=tf_spec) == MPIJobSpawner

        pytorch_spec = DummySpec(framework=ExperimentFramework.PYTORCH,
                                 backend=ExperimentBackend.NATIVE)
        assert get_spawner_class(specification=pytorch_spec) == ExperimentSpawner
        pytorch_spec.is_distributed = True
        assert get_spawner_class(specification=pytorch_spec) == PytorchSpawner
        pytorch_spec.backend = ExperimentBackend.KUBEFLOW
        assert get_spawner_class(specification=pytorch_spec) == PytorchJobSpawner
        pytorch_spec.backend = ExperimentBackend.MPI
        assert get_spawner_class(specification=pytorch_spec) == MPIJobSpawner

        horovod_spec = DummySpec(framework=ExperimentFramework.HOROVOD,
                                 backend=ExperimentBackend.NATIVE)
        assert get_spawner_class(specification=horovod_spec) == ExperimentSpawner
        horovod_spec.is_distributed = True
        assert get_spawner_class(specification=horovod_spec) == HorovodSpawner
        horovod_spec.backend = ExperimentBackend.KUBEFLOW
        assert get_spawner_class(specification=horovod_spec) == HorovodSpawner
        pytorch_spec.backend = ExperimentBackend.MPI
        assert get_spawner_class(specification=pytorch_spec) == MPIJobSpawner

        mxnet_spec = DummySpec(framework=ExperimentFramework.MXNET,
                               backend=ExperimentBackend.NATIVE)
        assert get_spawner_class(specification=mxnet_spec) == ExperimentSpawner
        mxnet_spec.is_distributed = True
        assert get_spawner_class(specification=mxnet_spec) == MXNetSpawner
        mxnet_spec.backend = ExperimentBackend.KUBEFLOW
        assert get_spawner_class(specification=mxnet_spec) == MXNetSpawner
        pytorch_spec.backend = ExperimentBackend.MPI
        assert get_spawner_class(specification=pytorch_spec) == MPIJobSpawner

        spec = DummySpec()
        assert get_spawner_class(specification=spec) == ExperimentSpawner
