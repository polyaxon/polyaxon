# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


def get_task_configs(cluster, is_distributed, configs, default_config, task_type):
    result_configs = {}
    if not is_distributed:
        return result_configs

    if default_config:
        for i in range(cluster.get(task_type, 0)):
            result_configs[i] = configs.get(i, default_config)

    return result_configs


def get_task_job_resources(cluster, is_distributed, resources, default_resources, task_type):
    if not is_distributed:
        return None

    result_resources = {}
    if default_resources:
        for i in range(cluster.get(task_type, 0)):
            result_resources[i] = resources.get(i, default_resources)

    return result_resources


def get_task_job_node_selectors(cluster,
                                is_distributed,
                                node_selectors,
                                default_node_selectors,
                                task_type):
    if not is_distributed:
        return None

    result_node_selectors = {}
    if default_node_selectors:
        for i in range(cluster.get(task_type, 0)):
            result_node_selectors[i] = node_selectors.get(i, default_node_selectors)

    return result_node_selectors


def get_task_job_tolerations(cluster,
                             is_distributed,
                             tolerations,
                             default_tolerations,
                             task_type):
    if not is_distributed:
        return None

    result_tolerations = {}
    if default_tolerations:
        for i in range(cluster.get(task_type, 0)):
            result_tolerations[i] = tolerations.get(i, default_tolerations)

    return result_tolerations


def get_task_job_affinities(cluster,
                            is_distributed,
                            affinities,
                            default_affinity,
                            task_type):
    if not is_distributed:
        return None

    result_affinities = {}
    if default_affinity:
        for i in range(cluster.get(task_type, 0)):
            result_affinities[i] = affinities.get(i, default_affinity)

    return result_affinities
