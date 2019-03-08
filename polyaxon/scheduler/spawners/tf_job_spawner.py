import conf

from constants.k8s_jobs import EXPERIMENT_KF_JOB_NAME_FORMAT
from scheduler.spawners.kf_experiment_spawner import KFExperimentSpawner
from scheduler.spawners.templates import kubeflow
from scheduler.spawners.templates.kubeflow import KUBEFLOW_JOB_GROUP
from scheduler.spawners.tensorflow_spawner import TensorflowSpawnerMixin
from schemas.tasks import TaskType


class TFJobSpawner(TensorflowSpawnerMixin, KFExperimentSpawner):
    KIND = kubeflow.TF_JOB_KIND
    VERSION = kubeflow.TF_JOB_VERSION
    PLURAL = kubeflow.TF_JOB_PLURAL
    SPEC = kubeflow.TF_SPEC

    @staticmethod
    def get_job_container_name(job_container_name):
        return job_container_name or conf.get('CONTAINER_NAME_TF_JOB')

    def start_experiment(self):
        labels = self.resource_manager.experiment_labels
        template_spec = {
            self.SPEC: {
                TaskType.CHIEF: self.create_master(),
                TaskType.WORKER: self.create_multi_jobs(task_type=TaskType.WORKER),
                TaskType.PS: self.create_multi_jobs(task_type=TaskType.PS)
            }
        }
        resource_name = EXPERIMENT_KF_JOB_NAME_FORMAT.format(
            experiment_uuid=self.resource_manager.experiment_uuid)
        custom_object = self.resource_manager.get_custom_object(resource_name=resource_name,
                                                                kind=self.KIND,
                                                                api_version=self.api_version,
                                                                labels=labels,
                                                                template_spec=template_spec)
        self.create_or_update_custom_object(name=resource_name,
                                            group=KUBEFLOW_JOB_GROUP,
                                            version=self.VERSION,
                                            plural=self.PLURAL,
                                            data=custom_object)
        return custom_object
