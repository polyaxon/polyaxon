# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from spawner.utils import constants


def get_status(node):
    status = [c.status for c in node.status.conditions if c.type == 'Ready'][0]
    if status == 'True':
        return constants.NodeLifeCycle.READY
    if status == 'FALSE':
        return constants.NodeLifeCycle.NOT_READY
    return constants.NodeLifeCycle.UNKNOWN


def get_n_gpus(node):
    return int(node.status.allocatable.get('alpha.kubernetes.io/nvidia-gpu', 0))


def get_n_cpus(node):
    return int(node.status.allocatable['cpu'])


def get_memory_size(node):
    return constants.to_bytes(node.status.allocatable['memory'])


def is_master(node):
    if ('node-role.kubernetes.io/master' in node.metadata.labels or
            node.metadata.labels.get('kubernetes.io/hostname') == 'minikube'):
        return True
    return False


def get_role(node):
    return constants.NodeRoles.MASTER if is_master(node) else constants.NodeRoles.WORKER


def get_docker_version(node):
    cri = node.status.node_info.container_runtime_version
    return cri[len('docker://'):] if cri.startswith('docker://') else constants.UNKNOWN


def is_schedulable(node):
    if not node.spec.taints:
        return True

    for t in node.spec.taints:
        if t.key == 'node-role.kubernetes.io/master' and t.effect == 'NoSchedule':
            return False


def get_schedulable_state(node):
    return not node.spec.unschedulable


def get_hostname(node):
    for a in node.status.addresses:
        if a.type == 'Hostname':
            return a.address
