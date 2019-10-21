import uuid

import conf

from options.registry.container_names import (
    CONTAINER_NAME_EXPERIMENT_JOBS,
    CONTAINER_NAME_PYTORCH_JOBS,
    CONTAINER_NAME_TF_JOBS
)
from schemas import ExperimentBackend, ExperimentFramework


def get_experiment_job_uuid(experiment_uuid, task_type, task_index):
    if isinstance(experiment_uuid, str):
        experiment_uuid = uuid.UUID(experiment_uuid)
    return uuid.uuid5(experiment_uuid, '{}-{}'.format(task_type, task_index)).hex


def get_experiment_job_container_name(backend, framework):
    if backend == ExperimentBackend.KUBEFLOW:
        if framework == ExperimentFramework.TENSORFLOW:
            return conf.get(CONTAINER_NAME_TF_JOBS)
        elif framework == ExperimentFramework.PYTORCH:
            return conf.get(CONTAINER_NAME_PYTORCH_JOBS)
    return conf.get(CONTAINER_NAME_EXPERIMENT_JOBS)
