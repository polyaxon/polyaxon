from kubernetes import client

from constants.k8s_jobs import JOB_NAME_FORMAT
from polyaxon_k8s import constants as k8s_constants
from polypod.templates.project_jobs.labels import get_labels
from polypod.templates.project_jobs.pods import get_project_pod_spec


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
                        env_from=None,
                        container_name=None,
                        resources=None,
                        node_selector=None,
                        affinity=None,
                        tolerations=None,
                        role=None,
                        type=None,  # pylint:disable=redefined-builtin
                        replicas=1,
                        service_account_name=None):
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
    pod_spec = get_project_pod_spec(volume_mounts=volume_mounts,
                                    volumes=volumes,
                                    image=image,
                                    container_name=container_name,
                                    command=command,
                                    args=args,
                                    resources=resources,
                                    node_selector=node_selector,
                                    affinity=affinity,
                                    tolerations=tolerations,
                                    ports=ports,
                                    env_vars=env_vars,
                                    env_from=env_from,
                                    service_account_name=service_account_name)
    template_spec = client.V1PodTemplateSpec(metadata=metadata, spec=pod_spec)
    return client.V1DeploymentSpec(
        replicas=replicas,
        template=template_spec,
        selector=client.V1LabelSelector(match_labels=labels),
    )


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
                   env_from=None,
                   resources=None,
                   node_selector=None,
                   affinity=None,
                   tolerations=None,
                   role=None,
                   type=None,  # pylint:disable=redefined-builtin
                   replicas=1,
                   service_account_name=None):
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
                               env_from=env_from,
                               container_name=container_name,
                               resources=resources,
                               node_selector=node_selector,
                               affinity=affinity,
                               tolerations=tolerations,
                               role=role,
                               type=type,
                               replicas=replicas,
                               service_account_name=service_account_name)
    return client.V1Deployment(
        api_version=k8s_constants.K8S_API_VERSION_APPS_V1,
        kind=k8s_constants.K8S_DEPLOYMENT_KIND,
        metadata=metadata,
        spec=spec)
