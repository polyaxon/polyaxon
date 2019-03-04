import conf
from scheduler.spawners.kf_experiment_spawner import KFExperimentSpawner
from scheduler.spawners.templates import kubeflow


class PytorchJobSpawner(KFExperimentSpawner):
    KIND = kubeflow.PYTORCH_JOB_KIND
    VERSION = kubeflow.PYTORCH_JOB_VERSION
    PLURAL = kubeflow.PYTORCH_JOB_PLURAL
    SPEC = kubeflow.PYTORCH_SPEC

    @staticmethod
    def get_job_container_name(job_container_name):
        return job_container_name or conf.get('CONTAINER_NAME_PYTORCH_JOB')
