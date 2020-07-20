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

import sys
import yaml

import click

from polyaxon.cli.errors import handle_cli_error
from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.polyaxonfile import get_specification
from polyaxon.utils.formatting import Printer, dict_tabulate, list_dicts_to_tabulate


def get_component_details(polyaxonfile, specification):
    if specification.name:
        Printer.print_header("Component description:")
        click.echo("{}\n".format(specification.description))
    if specification.description:
        Printer.print_header("Component description:")
        click.echo("{}\n".format(specification.description))

    if specification.inputs:
        Printer.print_header("Component inputs:")
        objects = list_dicts_to_tabulate([i.to_dict() for i in specification.inputs])
        dict_tabulate(objects, is_list_dict=True)

    if specification.outputs:
        Printer.print_header("Component outputs:")
        objects = list_dicts_to_tabulate([o.to_dict() for o in specification.outputs])
        dict_tabulate(objects, is_list_dict=True)
        dict_tabulate(specification.outputs)

    Printer.print_header("Component:")
    click.echo(polyaxonfile)


@click.group()
@click.option("--name", type=str, help="The component name.")
@click.pass_context
def hub(ctx, name):
    """Commands for ops/runs."""
    ctx.obj = ctx.obj or {}
    ctx.obj["name"] = name


@hub.command()
@click.option(
    "--save",
    is_flag=True,
    default=False,
    help="Save the content to a local polyaxonfile.",
)
@click.option(
    "--filename",
    type=str,
    help="The filename to use for saving the polyaxonfile, default to `polyaxonfile.yaml`.",
)
@click.pass_context
def get(ctx, save, filename):
    """Get a component info by component_name, or owner/component_name.

    Uses /docs/core/cli/#caching

    Examples:

    To get a component by name

    \b
    $ polyaxon hub get component_name

    To get a component by owner/name

    \b
    $ polyaxon hub get owner/component_name
    """
    name = ctx.obj.get("name")
    if not name:
        Printer.print_error("Please provide a valid component name!")
        sys.exit(0)
    try:
        polyaxonfile = ConfigSpec.get_from(name, "hub").read()
    except Exception as e:
        handle_cli_error(e, message="Could not get component `{}`.".format(name))
        sys.exit(1)
    specification = get_specification(data=polyaxonfile)
    polyaxonfile = yaml.dump(polyaxonfile)
    get_component_details(polyaxonfile=polyaxonfile, specification=specification)
    if save:
        filename = filename or "polyaxonfile.yaml"
        with open(filename, "w") as env_file:
            env_file.write(polyaxonfile)
