import conf

from constants.k8s_jobs import EXPERIMENT_KF_JOB_NAME_FORMAT
from options.registry.container_names import CONTAINER_NAME_PYTORCH_JOBS
from polypod.kf_experiment import KFExperimentSpawner
from polypod.pytorch import PytorchSpawnerMixin
from polypod.templates import kubeflow
from polypod.templates.kubeflow import KUBEFLOW_JOB_GROUP
from schemas import TaskType


class PytorchJobSpawner(PytorchSpawnerMixin, KFExperimentSpawner):
    KIND = kubeflow.PYTORCH_JOB_KIND
    VERSION = kubeflow.PYTORCH_JOB_VERSION
    PLURAL = kubeflow.PYTORCH_JOB_PLURAL
    SPEC = kubeflow.PYTORCH_SPEC

    @staticmethod
    def get_job_container_name(job_container_name):
        return job_container_name or conf.get(CONTAINER_NAME_PYTORCH_JOBS)

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
                                            body=custom_object,
                                            reraise=True)
        return custom_object
