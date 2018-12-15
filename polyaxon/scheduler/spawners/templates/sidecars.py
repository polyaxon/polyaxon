from hestia.auth import AuthenticationTypes
from hestia.list_utils import to_list
from kubernetes import client

from django.conf import settings

from scheduler.spawners.templates import constants
from scheduler.spawners.templates.env_vars import get_env_var, get_service_env_vars


def get_sidecar_env_vars(job_name, job_container_name, internal_health_check_url):
    return [
        get_env_var(name='POLYAXON_POD_ID', value=job_name),
        get_env_var(name='POLYAXON_CONTAINER_ID', value=job_container_name),
        get_env_var(name='POLYAXON_INTERNAL_HEALTH_CHECK_URL', value=internal_health_check_url),
        get_env_var(name='POLYAXON_AUTHENTICATION_TYPE', value=AuthenticationTypes.INTERNAL_TOKEN),
        get_env_var(name=constants.CONFIG_MAP_INTERNAL_HEADER,
                    value=settings.HEADERS_INTERNAL.replace('_', '-')),
        get_env_var(name=constants.CONFIG_MAP_INTERNAL_HEADER_SERVICE,
                    value=settings.INTERNAL_SERVICES.SIDECAR),
    ]


def get_sidecar_args(pod_id, container_id, app_label):
    return ["--pod_id={}".format(pod_id),
            "--container_id={}".format(container_id),
            "--log_sleep_interval={}".format(settings.JOB_SIDECAR_LOG_SLEEP_INTERVAL),
            "--app_label={}".format(app_label)]


def get_sidecar_command():
    return ["python3", "sidecar/__main__.py"]


def get_sidecar_container(job_name,
                          job_container_name,
                          sidecar_container_name,
                          sidecar_docker_image,
                          sidecar_docker_image_pull_policy,
                          namespace,
                          sidecar_config,
                          sidecar_args,
                          internal_health_check_url,
                          env_vars=None):
    """Return a pod sidecar container."""
    env_vars = to_list(env_vars) if env_vars else []
    env_vars += get_sidecar_env_vars(job_name=job_name,
                                     job_container_name=job_container_name,
                                     internal_health_check_url=internal_health_check_url)
    env_vars += get_service_env_vars(namespace=namespace)
    for k, v in sidecar_config.items():
        env_vars.append(get_env_var(name=k, value=v))
    return client.V1Container(name=sidecar_container_name,
                              image=sidecar_docker_image,
                              image_pull_policy=sidecar_docker_image_pull_policy,
                              command=get_sidecar_command(),
                              env=env_vars,
                              args=sidecar_args)
