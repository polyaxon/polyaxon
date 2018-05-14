# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


def get_task_configs(cluster, is_distributed, configs, default_config, task_type):
    result_configs = {}
    if not is_distributed:
        return result_configs

    for session_config in configs or []:
        result_configs[session_config.index] = session_config

    if default_config:
        for i in range(cluster.get(task_type, 0)):
            result_configs[i] = result_configs.get(i, default_config)

    return result_configs


def get_task_job_resources(cluster, is_distributed, resources, default_resources, task_type):
    if not is_distributed:
        return None

    result_resources = {}
    for resources_config in resources or []:
        result_resources[resources_config.index] = resources_config

    if default_resources:
        for i in range(cluster.get(task_type, 0)):
            result_resources[i] = result_resources.get(i, default_resources)

    return result_resources


def get_task_job_node_selectors(cluster,
                                is_distributed,
                                node_selectors,
                                default_node_selectors,
                                task_type):
    if not is_distributed:
        return None

    result_node_selectors = {}
    for node_selectors_config in node_selectors or []:
        result_node_selectors[node_selectors_config.pop('index', 0)] = node_selectors_config

    if default_node_selectors:
        for i in range(cluster.get(task_type, 0)):
            result_node_selectors[i] = result_node_selectors.get(i, default_node_selectors)

    return result_node_selectors
