from kubernetes import client

import conf
from options.registry.k8s import K8S_GPU_RESOURCE_KEY, K8S_TPU_RESOURCE_KEY


def get_resources(resources):  # pylint:disable=too-many-branches
    """Create resources requirements.

    Args:
        resources: `PodResourcesConfig`

    Return:
        `V1ResourceRequirements`
    """
    limits = {}
    requests = {}
    if resources is None:
        return None
    if resources.cpu:
        if resources.cpu.limits:
            limits['cpu'] = resources.cpu.limits
        if resources.cpu.requests:
            requests['cpu'] = resources.cpu.requests

    if resources.memory:
        if resources.memory.limits:
            limits['memory'] = '{}Mi'.format(resources.memory.limits)
        if resources.memory.requests:
            requests['memory'] = '{}Mi'.format(resources.memory.requests)

    if resources.gpu:
        resource_key = conf.get(K8S_GPU_RESOURCE_KEY)
        if resources.gpu.limits:
            limits[resource_key] = resources.gpu.limits
        if resources.gpu.requests:
            requests[resource_key] = resources.gpu.requests

    if resources.tpu:
        resource_key = conf.get(K8S_TPU_RESOURCE_KEY)
        if resources.tpu.limits:
            limits[resource_key] = resources.tpu.limits
        if resources.tpu.requests:
            requests[resource_key] = resources.tpu.requests
    return client.V1ResourceRequirements(limits=limits or None, requests=requests or None)


def get_init_resources():
    return client.V1ResourceRequirements(limits={'cpu': 1, 'memory': '100Mi'},
                                         requests={'cpu': 0.1, 'memory': '60Mi'})


def get_sidecar_resources():
    return client.V1ResourceRequirements(limits={'cpu': 1, 'memory': '100Mi'},
                                         requests={'cpu': 0.1, 'memory': '60Mi'})
