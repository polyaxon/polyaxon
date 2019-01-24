from hestia.list_utils import to_list
from kubernetes import client

import conf

from constants.k8s_jobs import JOB_NAME_FORMAT
from polyaxon_k8s import constants as k8s_constants
from scheduler.spawners.templates.env_vars import get_resources_env_vars
from scheduler.spawners.templates.gpu_volumes import get_gpu_volumes_def
from scheduler.spawners.templates.project_jobs.labels import get_labels
from scheduler.spawners.templates.resources import get_resources


def get_pod_container(volume_mounts,
                      image,
                      command,
                      args,
                      ports,
                      env_vars=None,
                      env_from=None,
                      container_name=None,
                      resources=None,
                      image_pull_policy=None):
    env_vars = to_list(env_vars, check_none=True)
    env_vars += get_resources_env_vars(resources=resources)

    ports = [client.V1ContainerPort(container_port=port) for port in ports]
    return client.V1Container(name=container_name,
                              image=image,
                              image_pull_policy=image_pull_policy,
                              command=command,
                              args=args,
                              ports=ports,
                              env=env_vars,
                              env_from=env_from,
                              resources=get_resources(resources),
                              volume_mounts=volume_mounts)


def get_project_pod_spec(volume_mounts,
                         volumes,
                         image,
                         command,
                         args,
                         ports,
                         env_vars=None,
                         env_from=None,
                         container_name=None,
                         resources=None,
                         node_selector=None,
                         affinity=None,
                         tolerations=None,
                         image_pull_policy=None,
                         restart_policy=None,
                         service_account_name=None):
    """Pod spec to be used to create pods for project: tensorboard, notebooks."""
    volume_mounts = to_list(volume_mounts, check_none=True)
    volumes = to_list(volumes, check_none=True)

    gpu_volume_mounts, gpu_volumes = get_gpu_volumes_def(resources)
    volume_mounts += gpu_volume_mounts
    volumes += gpu_volumes

    ports = [client.V1ContainerPort(container_port=port) for port in ports]

    pod_container = get_pod_container(
        volume_mounts=volume_mounts,
        image=image,
        command=command,
        args=args,
        ports=ports,
        env_vars=env_vars,
        env_from=env_from,
        container_name=container_name,
        resources=resources,
        image_pull_policy=image_pull_policy)
    containers = [pod_container]

    if service_account_name and not conf.get('K8S_RBAC_ENABLED'):
        service_account_name = None

    return client.V1PodSpec(restart_policy=restart_policy,
                            service_account_name=service_account_name,
                            containers=containers,
                            volumes=volumes,
                            node_selector=node_selector,
                            affinity=affinity,
                            tolerations=tolerations)


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
            affinity=None,
            tolerations=None,
            type=None,  # pylint:disable=redefined-builtin
            role=None,
            image_pull_policy=None,
            restart_policy=None,
            service_account_name=None):
    pod_spec = get_project_pod_spec(
        volume_mounts=volume_mounts,
        volumes=volumes,
        image=image,
        image_pull_policy=image_pull_policy,
        container_name=container_name,
        command=command,
        args=args,
        resources=resources,
        node_selector=node_selector,
        affinity=affinity,
        tolerations=tolerations,
        ports=ports,
        env_vars=env_vars,
        service_account_name=service_account_name,
        restart_policy=restart_policy)

    labels = get_labels(app=app,
                        project_name=project_name,
                        project_uuid=project_uuid,
                        job_name=job_name,
                        job_uuid=job_uuid,
                        role=role,
                        type=type)
    metadata = client.V1ObjectMeta(
        name=JOB_NAME_FORMAT.format(name=name, job_uuid=job_uuid),
        labels=labels,
        namespace=namespace)
    return client.V1Pod(api_version=k8s_constants.K8S_API_VERSION_V1,
                        kind=k8s_constants.K8S_POD_KIND,
                        metadata=metadata,
                        spec=pod_spec)
