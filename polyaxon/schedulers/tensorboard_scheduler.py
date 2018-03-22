import logging

from django.conf import settings
from spawners.tensorboard_spawner import TensorboardSpawner
from spawners.utils.constants import ExperimentLifeCycle

logger = logging.getLogger('polyaxon.schedulers.tensorboard')


def start_tensorboard(project):
    spawner = TensorboardSpawner(
        project_name=project.unique_name,
        project_uuid=project.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    spawner.start_tensorboard(image=project.tensorboard.image,
                              resources=project.tensorboard.compiled_spec.resources)
    project.has_tensorboard = True
    project.save()


def stop_tensorboard(project, update_status=False):
    spawner = TensorboardSpawner(
        project_name=project.unique_name,
        project_uuid=project.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)

    spawner.stop_tensorboard()
    project.has_tensorboard = False
    project.save()
    if update_status:
        # Update experiment status to show that its stopped
        project.tensorboard.set_status(status=ExperimentLifeCycle.STOPPED,
                                       message='Tensorboard was stopped')


def get_tensorboard_url(project):
    spawner = TensorboardSpawner(
        project_name=project.unique_name,
        project_uuid=project.uuid.hex,
        k8s_config=settings.K8S_CONFIG,
        namespace=settings.K8S_NAMESPACE,
        in_cluster=True)
    return spawner.get_tensorboard_url()
