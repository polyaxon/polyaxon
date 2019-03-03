from scheduler.spawners.kf_experiment_spawner import KFExperimentSpawner
from scheduler.spawners.templates import kubeflow


class TFJobSpawner(KFExperimentSpawner):
    GROUP = kubeflow.TF_JOB_KIND
    VERSION = kubeflow.TF_JOB_VERSION
    PLURAL = kubeflow.TF_JOB_PLURAL
