import conf

from constants.k8s_jobs import EXPERIMENT_KF_JOB_NAME_FORMAT
from scheduler.spawners.kf_experiment_spawner import KFExperimentSpawner
from scheduler.spawners.templates import kubeflow
from scheduler.spawners.templates.kubeflow import KUBEFLOW_JOB_GROUP
from scheduler.spawners.pytorch_spawner import PytorchSpawnerMixin
from schemas.tasks import TaskType


class PytorchJobSpawner(PytorchSpawnerMixin, KFExperimentSpawner):
    KIND = kubeflow.PYTORCH_JOB_KIND
    VERSION = kubeflow.PYTORCH_JOB_VERSION
    PLURAL = kubeflow.PYTORCH_JOB_PLURAL
    SPEC = kubeflow.PYTORCH_SPEC

    @staticmethod
    def get_job_container_name(job_container_name):
        return job_container_name or conf.get('CONTAINER_NAME_PYTORCH_JOB')

    def start_experiment(self):
        labels = self.resource_manager.experiment_labels
        template_spec = {
            self.SPEC: {
                TaskType.MASTER.capitalize(): self.create_master(),
                TaskType.WORKER.capitalize(): self.create_multi_jobs(task_type=TaskType.WORKER),
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
