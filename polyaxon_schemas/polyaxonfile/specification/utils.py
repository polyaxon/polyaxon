# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy


def get_task_values(cluster, is_distributed, values, default_value, task_type):
    result_values = {}
    if not is_distributed:
        return result_values

    result_values = copy.deepcopy(values) if values else {}
    if default_value:
        for i in range(cluster.get(task_type, 0)):
            result_values[i] = values.get(i, default_value)

    return result_values


def get_task_configs(cluster, is_distributed, configs, default_config, task_type):
    return get_task_values(cluster=cluster,
                           is_distributed=is_distributed,
                           values=configs,
                           default_value=default_config,
                           task_type=task_type)


def get_task_job_resources(cluster, is_distributed, resources, default_resources, task_type):
    return get_task_values(cluster=cluster,
                           is_distributed=is_distributed,
                           values=resources,
                           default_value=default_resources,
                           task_type=task_type)


def get_task_job_node_selectors(cluster,
                                is_distributed,
                                node_selectors,
                                default_node_selector,
                                task_type):
    return get_task_values(cluster=cluster,
                           is_distributed=is_distributed,
                           values=node_selectors,
                           default_value=default_node_selector,
                           task_type=task_type)


def get_task_job_tolerations(cluster,
                             is_distributed,
                             tolerations,
                             default_tolerations,
                             task_type):
    return get_task_values(cluster=cluster,
                           is_distributed=is_distributed,
                           values=tolerations,
                           default_value=default_tolerations,
                           task_type=task_type)


def get_task_job_affinities(cluster,
                            is_distributed,
                            affinities,
                            default_affinity,
                            task_type):
    return get_task_values(cluster=cluster,
                           is_distributed=is_distributed,
                           values=affinities,
                           default_value=default_affinity,
                           task_type=task_type)
