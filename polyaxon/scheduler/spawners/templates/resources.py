from kubernetes import client

from django.conf import settings


def get_resources(resources):
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
        if resources.gpu.limits:
            limits[settings.K8S_GPU_RESOURCE_KEY] = resources.gpu.limits
        if resources.gpu.requests:
            requests[settings.K8S_GPU_RESOURCE_KEY] = resources.gpu.requests
    return client.V1ResourceRequirements(limits=limits or None, requests=requests or None)
