from django.conf import settings
from kubernetes import client
from polyaxon_schemas.utils import to_list

from scheduler.spawners.templates.env_vars import get_env_var, get_service_env_vars


def get_sidecar_env_vars(job_name, job_container_name):
    return [
        get_env_var(name='POLYAXON_POD_ID', value=job_name),
        get_env_var(name='POLYAXON_JOB_ID', value=job_container_name),
    ]


def get_sidecar_args(pod_id):
    return [pod_id,
            "--log_sleep_interval={}".format(settings.JOB_SIDECAR_LOG_SLEEP_INTERVAL),
            "--persist=true"]


def get_sidecar_command(app_label):
    if app_label == settings.APP_LABELS_JOB:
        return ["python3", "polyaxon/manage.py", "start_job_sidecar"]
    if app_label == settings.APP_LABELS_EXPERIMENT:
        return ["python3", "polyaxon/manage.py", "start_experiment_sidecar"]


def get_sidecar_container(job_name,
                          job_container_name,
                          sidecar_container_name,
                          sidecar_docker_image,
                          namespace,
                          app_label,
                          sidecar_config,
                          sidecar_args,
                          env_vars=None):
    """Return a pod sidecar container."""
    env_vars = to_list(env_vars) if env_vars else []
    env_vars += get_sidecar_env_vars(job_name=job_name, job_container_name=job_container_name)
    env_vars += get_service_env_vars(namespace=namespace)
    for k, v in sidecar_config.items():
        env_vars.append(get_env_var(name=k, value=v))
    return client.V1Container(name=sidecar_container_name,
                              image=sidecar_docker_image,
                              command=get_sidecar_command(app_label=app_label),
                              env=env_vars,
                              args=sidecar_args)
