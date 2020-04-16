#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys

from collections import OrderedDict

import click

from tabulate import tabulate

from polyaxon.schemas.api.resources import ContainerResourcesConfig
from polyaxon.utils.humanize import humanize_timesince
from polyaxon.utils.list_utils import to_list
from polyaxon.utils.units import to_percentage, to_unit_memory


def get_meta_response(response):
    results = {}
    if response.next:
        results["next"] = response.next
    if response.previous:
        results["previous"] = response.previous
    if response.count:
        results["count"] = response.count
    return results


def humanize_attrs(key, value, rounding=2):
    if key in [
        "created_at",
        "updated_at",
        "started_at",
        "finished_at",
        "last_update_time",
        "last_transition_time",
    ]:
        return humanize_timesince(value)
    if key in ["cpu_percentage"]:
        return to_percentage(value, rounding)
    if key in ["memory_free", "memory_used", "memory_total"]:
        return to_unit_memory(value)
    return value


def list_dicts_to_tabulate(list_dicts, exclude_attrs=None, humanize_values=True):
    exclude_attrs = exclude_attrs or {}
    results = OrderedDict()
    for d_value in list_dicts:
        for k, v in d_value.items():
            if k in exclude_attrs:
                continue

            if humanize_values:
                v = humanize_attrs(k, v)

            k = k.upper()
            if k in results:
                results[k].append(v)
            else:
                results[k] = [v]

    return results


def dict_to_tabulate(d_value, exclude_attrs=None, humanize_values=True):
    exclude_attrs = exclude_attrs or {}
    results = OrderedDict()
    for k, v in d_value.items():
        if k in exclude_attrs:
            continue

        if humanize_values:
            v = humanize_attrs(k, v)

        results[k.upper()] = v

    return results


def dict_tabulate(dict_value, is_list_dict=False):
    if is_list_dict:
        headers = dict_value.keys()
        click.echo(tabulate(dict_value, headers=headers))
    else:
        click.echo(tabulate(dict_value.items()))


def pprint(value):
    """Prints as formatted JSON"""
    click.echo(json.dumps(value, sort_keys=True, indent=4, separators=(",", ": ")))


class Printer(object):
    COLORS = ["yellow", "blue", "magenta", "green", "cyan", "red", "white"]

    @staticmethod
    def print_header(text):
        click.secho("\n{}\n".format(text), fg="yellow")

    @staticmethod
    def print_warning(text):
        click.secho("\n{}\n".format(text), fg="magenta")

    @staticmethod
    def print_success(text):
        click.secho(text, fg="green")

    @staticmethod
    def print_error(text, sys_exit: bool = False):
        click.secho(text, fg="red")
        if sys_exit:
            sys.exit(1)

    @staticmethod
    def add_color(value, color):
        return click.style("{}".format(value), fg=color)

    @classmethod
    def get_colored_status(cls, status):
        if status == "created":
            return cls.add_color(status, "cyan")
        elif status == "succeeded":
            return cls.add_color(status, color="green")
        elif status in ["failed", "stopped", "upstream_failed"]:
            return cls.add_color(status, color="red")
        elif status == "done":
            return cls.add_color(status, color="white")

        return cls.add_color(status, color="yellow")

    @classmethod
    def add_status_color(cls, obj_dict, status_key="status"):
        if obj_dict.get(status_key) is None:
            return obj_dict

        obj_dict[status_key] = cls.get_colored_status(obj_dict[status_key])
        return obj_dict

    @classmethod
    def add_memory_unit(cls, obj_dict, keys):
        keys = to_list(keys)
        for key in keys:
            obj_dict[key] = to_unit_memory(obj_dict[key])
        return obj_dict

    @classmethod
    def decorate_format_value(cls, text_format, values, color):
        values = to_list(values)
        values = [cls.add_color(value, color) for value in values]
        click.echo(text_format.format(*values))

    @staticmethod
    def log(value, nl=False):
        click.echo(value, nl=nl)

    @classmethod
    def resources(cls, jobs_resources):
        jobs_resources = to_list(jobs_resources)
        click.clear()
        data = [["Job", "Mem Usage / Total", "CPU% - CPUs"]]
        for job_resources in jobs_resources:
            job_resources = ContainerResourcesConfig.from_dict(job_resources)
            line = [
                job_resources.job_name,
                "{} / {}".format(
                    to_unit_memory(job_resources.memory_used),
                    to_unit_memory(job_resources.memory_limit),
                ),
                "{} - {}".format(
                    to_percentage(job_resources.cpu_percentage / 100),
                    job_resources.n_cpus,
                ),
            ]
            data.append(line)
        click.echo(tabulate(data, headers="firstrow"))
        sys.stdout.flush()

    @classmethod
    def gpu_resources(cls, jobs_resources):
        jobs_resources = to_list(jobs_resources)
        click.clear()
        data = [
            [
                "job_name",
                "name",
                "GPU Usage",
                "GPU Mem Usage / Total",
                "GPU Temperature",
                "Power Draw / Limit",
            ]
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
                    "{} / {}".format(
                        to_unit_memory(gpu_resources.memory_used),
                        to_unit_memory(gpu_resources.memory_total),
                    ),
                    gpu_resources.temperature_gpu,
                    "{} / {}".format(
                        gpu_resources.power_draw, gpu_resources.power_limit
                    ),
                ]
            data.append(line)
        if non_gpu_jobs == len(jobs_resources):
            Printer.print_error(
                "No GPU job was found, please run `resources` command without `-g | --gpu` option."
            )
            exit(1)
        click.echo(tabulate(data, headers="firstrow"))
        sys.stdout.flush()


def get_runs_with_keys(objects, params_keys):
    # Extend run with params_keys
    keys = set([])
    for params_key in params_keys:
        for obj in objects:
            params = obj.pop(params_key, {}) or {}
            keys |= set(params.keys())
            obj.update(params)

    # Check that all obj have all metrics
    # TODO: optimize this process
    for obj in objects:
        obj_keys = set(obj.keys())
        for param in keys:
            if param not in obj_keys:
                obj[param] = None

    return objects
