from kubernetes import client

from polyaxon_k8s import constants as k8s_constants
from scheduler.spawners.templates import constants
from scheduler.spawners.templates.project_jobs.labels import get_labels
from scheduler.spawners.templates.project_jobs.pods import get_project_pod_spec


def get_deployment_spec(namespace,
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
                        env_vars=None,
                        container_name=None,
                        resources=None,
                        node_selector=None,
                        role=None,
                        type=None,  # pylint:disable=redefined-builtin
                        replicas=1):
    labels = get_labels(app=app,
                        project_name=project_name,
                        project_uuid=project_uuid,
                        job_name=job_name,
                        job_uuid=job_uuid,
                        role=role,
                        type=type)
    metadata = client.V1ObjectMeta(
        name=constants.DEPLOYMENT_NAME.format(name=name, job_uuid=job_uuid),
        labels=labels,
        namespace=namespace)
    pod_spec = get_project_pod_spec(volume_mounts=volume_mounts,
                                    volumes=volumes,
                                    image=image,
                                    container_name=container_name,
                                    command=command,
                                    args=args,
                                    resources=resources,
                                    node_selector=node_selector,
                                    ports=ports,
                                    env_vars=env_vars)
    template_spec = client.V1PodTemplateSpec(metadata=metadata, spec=pod_spec)
    return client.AppsV1beta1DeploymentSpec(replicas=replicas, template=template_spec)


def get_deployment(namespace,
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
                   role=None,
                   type=None,  # pylint:disable=redefined-builtin
                   replicas=1):
    labels = get_labels(app=app,
                        project_name=project_name,
                        project_uuid=project_uuid,
                        job_name=job_name,
                        job_uuid=job_uuid,
                        role=role,
                        type=type)
    metadata = client.V1ObjectMeta(
        name=constants.DEPLOYMENT_NAME.format(name=name, job_uuid=job_uuid),
        labels=labels,
        namespace=namespace)
    spec = get_deployment_spec(namespace=namespace,
                               app=app,
                               name=name,
                               project_name=project_name,
                               project_uuid=project_uuid,
                               job_name=job_name,
                               job_uuid=job_uuid,
                               volume_mounts=volume_mounts,
                               volumes=volumes,
                               image=image,
                               command=command,
                               args=args,
                               ports=ports,
                               env_vars=env_vars,
                               container_name=container_name,
                               resources=resources,
                               node_selector=node_selector,
                               role=role,
                               type=type,
                               replicas=replicas)
    return client.AppsV1beta1Deployment(api_version=k8s_constants.K8S_API_VERSION_V1_BETA1,
                                        kind=k8s_constants.K8S_DEPLOYMENT_KIND,
                                        metadata=metadata,
                                        spec=spec)
