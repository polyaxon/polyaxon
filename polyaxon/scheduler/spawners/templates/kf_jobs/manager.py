from constants.k8s_jobs import EXPERIMENT_KF_TASK_NAME_FORMAT
from scheduler.spawners.templates.experiment_jobs.manager import (
    ResourceManager as ExperimentResourceManager
)


class ResourceManager(ExperimentResourceManager):

    def get_resource_name(self, task_type):  # pylint:disable=arguments-differ
        return EXPERIMENT_KF_TASK_NAME_FORMAT.format(task_type=task_type,
                                                     experiment_uuid=self.experiment_uuid)

    def get_labels(self, task_type):  # pylint:disable=arguments-differ
        labels = self.get_recommended_labels(job_uuid=self.experiment_uuid)
        labels.update(self.get_experiment_labels())
        labels.update({
            'task_type': task_type,
        })
        return labels
