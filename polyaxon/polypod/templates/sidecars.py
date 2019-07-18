from hestia.auth import AuthenticationTypes
from hestia.internal_services import InternalServices
from hestia.list_utils import to_list
from kubernetes import client

import conf

from options.registry.sidecars import SIDECARS_SLEEP_INTERVAL
from polypod.templates.env_vars import get_env_var, get_from_field_ref, get_internal_env_vars
from polypod.templates.resources import get_sidecar_resources


def get_sidecar_env_vars(namespace,
                         job_container_name,
                         internal_health_check_url,
                         internal_reconcile_url):
    env_vars = get_internal_env_vars(namespace=namespace,
                                     service_internal_header=InternalServices.SIDECAR,
                                     authentication_type=AuthenticationTypes.INTERNAL_TOKEN,
                                     include_internal_token=True)

    return env_vars + [
        get_env_var(name='POLYAXON_CONTAINER_ID', value=job_container_name),
        get_env_var(name='POLYAXON_INTERNAL_HEALTH_CHECK_URL', value=internal_health_check_url),
        get_env_var(name='POLYAXON_INTERNAL_RECONCILE_URL', value=internal_reconcile_url),
        get_from_field_ref(name='POLYAXON_POD_ID', field_path='metadata.name'),
    ]


def get_sidecar_args(container_id, app_label, max_restarts):
    return ["--container_id={}".format(container_id),
            "--sleep_interval={}".format(conf.get(SIDECARS_SLEEP_INTERVAL)),
            "--app_label={}".format(app_label),
            "--max_restarts={}".format(max_restarts or 0)]


def get_sidecar_command():
    return ["python3", "sidecar/__main__.py"]


def get_sidecar_container(job_container_name,
                          sidecar_container_name,
                          sidecar_docker_image,
                          sidecar_docker_image_pull_policy,
                          namespace,
                          sidecar_config,
                          sidecar_args,
                          internal_health_check_url,
                          internal_reconcile_url,
                          volume_mounts,
                          env_vars=None):
    """Return a pod sidecar container."""
    env_vars = to_list(env_vars) if env_vars else []
    env_vars += get_sidecar_env_vars(namespace=namespace,
                                     job_container_name=job_container_name,
                                     internal_health_check_url=internal_health_check_url,
                                     internal_reconcile_url=internal_reconcile_url)
    for k, v in sidecar_config.items():
        env_vars.append(get_env_var(name=k, value=v))
    return client.V1Container(name=sidecar_container_name,
                              image=sidecar_docker_image,
                              image_pull_policy=sidecar_docker_image_pull_policy,
                              command=get_sidecar_command(),
                              env=env_vars,
                              volume_mounts=volume_mounts,
                              resources=get_sidecar_resources(),
                              args=sidecar_args)
