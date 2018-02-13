# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from kubernetes import client

from polyaxon_k8s import constants as k8s_constants

from spawner.templates import constants
from spawner.templates import pods


def get_labels(name, project_name, project_uuid, role=None, type=None):
    labels = {'app': name, 'project_name': project_name, 'project_uuid': project_uuid}
    if role:
        labels['role'] = role
    if type:
        labels['type'] = type
    return labels


def get_project_pod_spec(project_uuid,
                         name,
                         volume_mounts,
                         volumes,
                         image,
                         command=None,
                         args=None,
                         ports=None,
                         resources=None,
                         env_vars=None,
                         restart_policy=None):
    """Pod spec to be used to create pods for project side: tensorboard, notebooks."""
    volume_mounts = volume_mounts or []
    volumes = volumes or []

    gpu_volume_mounts, gpu_volumes = pods.get_gpu_volumes_def(resources)
    volume_mounts += gpu_volume_mounts
    volumes += gpu_volumes

    ports = [client.V1ContainerPort(container_port=port) for port in ports]

    container_name = constants.POD_CONTAINER_PROJECT_NAME.format(
        project_uuid=project_uuid, name=name)
    containers = [client.V1Container(name=container_name,
                                     image=image,
                                     command=command,
                                     args=args,
                                     ports=ports,
                                     env=env_vars,
                                     resources=pods.get_resources(resources),
                                     volume_mounts=volume_mounts)]
    return client.V1PodSpec(restart_policy=restart_policy, containers=containers, volumes=volumes)


def get_deployment_spec(namespace,
                        name,
                        project_name,
                        project_uuid,
                        volume_mounts,
                        volumes,
                        image,
                        command,
                        args,
                        ports,
                        resources=None,
                        role=None,
                        type=None,
                        replicas=1):
    labels = get_labels(name=name,
                        project_name=project_name,
                        project_uuid=project_uuid,
                        role=role,
                        type=type)
    metadata = client.V1ObjectMeta(
        name=constants.DEPLOYMENT_NAME.format(name=name, project_uuid=project_uuid),
        labels=labels,
        namespace=namespace)
    pod_spec = get_project_pod_spec(project_uuid=project_uuid,
                                    name=name,
                                    volume_mounts=volume_mounts,
                                    volumes=volumes,
                                    image=image,
                                    command=command,
                                    args=args,
                                    resources=resources,
                                    ports=ports)
    template_spec = client.V1PodTemplateSpec(metadata=metadata, spec=pod_spec)
    return client.AppsV1beta1DeploymentSpec(replicas=replicas, template=template_spec)


def get_deployment(namespace,
                   name,
                   project_name,
                   project_uuid,
                   volume_mounts,
                   volumes,
                   image,
                   command,
                   args,
                   ports,
                   resources=None,
                   role=None,
                   type=None,
                   replicas=1):
    labels = get_labels(name=name,
                        project_name=project_name,
                        project_uuid=project_uuid,
                        role=role,
                        type=type)
    metadata = client.V1ObjectMeta(
        name=constants.DEPLOYMENT_NAME.format(project_uuid=project_uuid, name=name),
        labels=labels,
        namespace=namespace)
    spec = get_deployment_spec(namespace=namespace,
                               name=name,
                               project_name=project_name,
                               project_uuid=project_uuid,
                               volume_mounts=volume_mounts,
                               volumes=volumes,
                               image=image,
                               command=command,
                               args=args,
                               ports=ports,
                               resources=resources,
                               role=role,
                               type=type,
                               replicas=replicas)
    return client.AppsV1beta1Deployment(api_version=k8s_constants.K8S_API_VERSION_V1_BETA1,
                                        kind=k8s_constants.K8S_DEPLOYMENT_KIND,
                                        metadata=metadata,
                                        spec=spec)
