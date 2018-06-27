from kubernetes import client

from django.conf import settings

from libs.utils import get_list
from polyaxon_k8s import constants as k8s_constants
from scheduler.spawners.templates import constants
from scheduler.spawners.templates.env_vars import get_resources_env_vars
from scheduler.spawners.templates.gpu_volumes import get_gpu_volumes_def
from scheduler.spawners.templates.project_jobs.labels import get_labels
from scheduler.spawners.templates.resources import get_resources


def get_project_pod_spec(volume_mounts,
                         volumes,
                         image,
                         command,
                         args,
                         ports,
                         env_vars=None,
                         container_name=None,
                         resources=None,
                         node_selector=None,
                         restart_policy=None,
                         use_service_account=False):
    """Pod spec to be used to create pods for project: tensorboard, notebooks."""
    env_vars = get_list(env_vars)
    volume_mounts = get_list(volume_mounts)
    volumes = get_list(volumes)

    gpu_volume_mounts, gpu_volumes = get_gpu_volumes_def(resources)
    volume_mounts += gpu_volume_mounts
    volumes += gpu_volumes

    ports = [client.V1ContainerPort(container_port=port) for port in ports]
    env_vars += get_resources_env_vars(resources=resources)

    containers = [client.V1Container(name=container_name,
                                     image=image,
                                     command=command,
                                     args=args,
                                     ports=ports,
                                     env=env_vars,
                                     resources=get_resources(resources),
                                     volume_mounts=volume_mounts)]

    service_account_name = None
    if use_service_account and settings.K8S_RBAC_ENABLED:
        service_account_name = settings.K8S_SERVICE_ACCOUNT_NAME

    return client.V1PodSpec(restart_policy=restart_policy,
                            service_account_name=service_account_name,
                            containers=containers,
                            volumes=volumes,
                            node_selector=node_selector)


def get_pod(namespace,
            app,
            name,
            project_name,
            project_uuid,
            job_name,
            job_uuid,
            volume_mounts,
            volumes,
            image,
            command,
            args,
            ports,
            container_name,
            env_vars=None,
            resources=None,
            node_selector=None,
            type=None,  # pylint:disable=redefined-builtin
            role=None,
            restart_policy=None,
            use_service_account=False):
    pod_spec = get_project_pod_spec(
        volume_mounts=volume_mounts,
        volumes=volumes,
        image=image,
        container_name=container_name,
        command=command,
        args=args,
        resources=resources,
        node_selector=node_selector,
        ports=ports,
        env_vars=env_vars,
        use_service_account=use_service_account,
        restart_policy=restart_policy)

    labels = get_labels(app=app,
                        project_name=project_name,
                        project_uuid=project_uuid,
                        job_name=job_name,
                        job_uuid=job_uuid,
                        role=role,
                        type=type)
    metadata = client.V1ObjectMeta(
        name=constants.JOB_NAME.format(name=name, job_uuid=job_uuid),
        labels=labels,
        namespace=namespace)
    return client.V1Pod(api_version=k8s_constants.K8S_API_VERSION_V1,
                        kind=k8s_constants.K8S_POD_KIND,
                        metadata=metadata,
                        spec=pod_spec)
