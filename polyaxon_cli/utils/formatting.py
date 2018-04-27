# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import six
import sys

from collections import OrderedDict

import click

from tabulate import tabulate

from polyaxon_schemas.environments import K8SResourcesConfig
from polyaxon_schemas.experiment import ContainerResourcesConfig
from polyaxon_schemas.utils import to_list, to_percentage, to_unit_memory


def get_meta_response(response):
    results = {}
    if response.get('next'):
        results['next'] = '--page={}'.format(response['next'])
    if response.get('previous'):
        results['previous'] = '--page={}'.format(response['previous'])
    if response.get('count'):
        results['count'] = response['count']
    return results


def list_dicts_to_tabulate(list_dicts):
    results = OrderedDict()
    for d_value in list_dicts:
        for k, v in six.iteritems(d_value):
            if k in results:
                results[k].append(v)
            else:
                results[k] = [v]

    return results


def dict_tabulate(dict_value, is_list_dict=False):
    if is_list_dict:
        headers = six.iterkeys(dict_value)
        click.echo(tabulate(dict_value, headers=headers))
    else:
        click.echo(tabulate(six.iteritems(dict_value)))


def pprint(value):
    """Prints as formatted JSON"""
    click.echo(
        json.dumps(value,
                   sort_keys=True,
                   indent=4,
                   separators=(',', ': ')))


class Printer(object):
    COLORS = ['yellow', 'blue', 'magenta', 'green', 'cyan', 'red', 'white']

    @staticmethod
    def print_header(text):
        click.secho('\n{}\n'.format(text), fg='yellow')

    @staticmethod
    def print_warning(text):
        click.secho('\n{}\n'.format(text), fg='magenta')

    @staticmethod
    def print_success(text):
        click.secho('\n{}\n'.format(text), fg='green')

    @staticmethod
    def print_error(text):
        click.secho('\n{}\n'.format(text), fg='red')

    @staticmethod
    def add_color(value, color):
        return click.style('{}'.format(value), fg=color)

    @classmethod
    def add_status_color(cls, obj_dict):
        if obj_dict.get('is_running'):
            obj_dict['last_status'] = cls.add_color(obj_dict['last_status'], color='yellow')
        elif obj_dict.get('is_done'):
            color = 'green' if obj_dict['last_status'] == 'Succeeded' else 'red'
            obj_dict['last_status'] = cls.add_color(obj_dict['last_status'], color=color)
        elif obj_dict.get('last_status'):
            obj_dict['last_status'] = cls.add_color(obj_dict['last_status'], color='cyan')

        obj_dict.pop('is_done', None)
        obj_dict.pop('is_running', None)
        return obj_dict

    @classmethod
    def add_memory_unit(cls, obj_dict, keys):
        keys = to_list(keys)
        for key in keys:
            obj_dict[key] = to_unit_memory(obj_dict[key])
        return obj_dict

    @classmethod
    def handle_statuses(cls, obj_dict):
        if obj_dict.get('status') == 'Created':
            obj_dict['status'] = cls.add_color(obj_dict['status'], color='cyan')
        elif obj_dict.get('status') == 'Succeeded':
            obj_dict['status'] = cls.add_color(obj_dict['status'], color='green')
        elif obj_dict.get('status') in ['Failed', 'Stopped']:
            obj_dict['status'] = cls.add_color(obj_dict['status'], color='red')
        obj_dict['status'] = cls.add_color(obj_dict['status'], color='yellow')
        return obj_dict

    @classmethod
    def decorate_format_value(cls, text_format, values, color):
        values = to_list(values)
        values = [cls.add_color(value, color) for value in values]
        click.echo(text_format.format(*values))

    @staticmethod
    def log(value):
        click.echo(value, nl=False)

    @classmethod
    def resources(cls, jobs_resources):
        jobs_resources = to_list(jobs_resources)
        click.clear()
        data = [['Job', 'Mem Usage / Total', 'CPU% - CPUs']]
        for job_resources in jobs_resources:
            job_resources = ContainerResourcesConfig.from_dict(job_resources)
            line = [
                job_resources.job_name,
                '{} / {}'.format(to_unit_memory(job_resources.memory_used),
                                 to_unit_memory(job_resources.memory_limit)),
                '{} - {}'.format(to_percentage(job_resources.cpu_percentage / 100),
                                 job_resources.n_cpus)]
            data.append(line)
        click.echo(tabulate(data, headers="firstrow"))
        sys.stdout.flush()

    @classmethod
    def gpu_resources(cls, jobs_resources):
        jobs_resources = to_list(jobs_resources)
        click.clear()
        data = [
            ['job_name', 'name', 'GPU Usage', 'GPU Mem Usage / Total', 'GPU Temperature',
             'Power Draw / Limit']
        ]
        non_gpu_jobs = 0
        for job_resources in jobs_resources:
            job_resources = ContainerResourcesConfig.from_dict(job_resources)
            line = []
            if not job_resources.gpu_resources:
                non_gpu_jobs += 1
                continue
            for gpu_resources in job_resources.gpu_resources:
                line += [
                    job_resources.job_name,
                    gpu_resources.name,
                    to_percentage(gpu_resources.utilization_gpu / 100),
                    '{} / {}'.format(
                        to_unit_memory(gpu_resources.memory_used),
                        to_unit_memory(gpu_resources.memory_total)),
                    gpu_resources.temperature_gpu,
                    '{} / {}'.format(gpu_resources.power_draw, gpu_resources.power_limit),
                ]
            data.append(line)
        if non_gpu_jobs == len(jobs_resources):
            Printer.print_error(
                'No GPU job was found, please run `resources` command without `-g | --gpu` option.')
            exit(1)
        click.echo(tabulate(data, headers="firstrow"))
        sys.stdout.flush()


def get_experiments_with_metrics(response):
    objects = [
        o.to_light_dict(include_attrs=['sequence', 'unique_name', 'total_run', 'last_metric'])
        for o in response['results']
    ]
    # Extend experiment with metrics
    metric_keys = set([])
    for obj in objects:
        last_metric = obj.pop('last_metric', {}) or {}
        metric_keys |= set(six.iterkeys(last_metric))
        obj.update(last_metric)

    # Check that all obj have all metrics
    # TODO: optimize this process
    for obj in objects:
        obj_keys = set(six.iterkeys(obj))
        for metric in metric_keys:
            if metric not in obj_keys:
                obj[metric] = None

    return objects


def get_resources(resources, header=None):
    header = header or 'Resources:'
    Printer.print_header(header)
    objects = []
    for item in six.iterkeys(resources):
        item_dict = OrderedDict()
        item_dict['resource'] = item
        item_dict.update(resources[item] or K8SResourcesConfig().to_dict())
        objects.append(item_dict)
    objects = list_dicts_to_tabulate(objects)
    dict_tabulate(objects, is_list_dict=True)
