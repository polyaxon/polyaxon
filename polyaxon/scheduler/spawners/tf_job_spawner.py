import conf

from scheduler.spawners.kf_experiment_spawner import KFExperimentSpawner
from scheduler.spawners.templates import kubeflow
from scheduler.spawners.tensorflow_spawner import TensorflowSpawnerMixin


class TFJobSpawner(TensorflowSpawnerMixin, KFExperimentSpawner):
    KIND = kubeflow.TF_JOB_KIND
    VERSION = kubeflow.TF_JOB_VERSION
    PLURAL = kubeflow.TF_JOB_PLURAL
    SPEC = kubeflow.TF_SPEC

    @staticmethod
    def get_job_container_name(job_container_name):
        return job_container_name or conf.get('CONTAINER_NAME_TF_JOB')
