#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

import sys

import click

from marshmallow import ValidationError

from polyaxon.builds.generator import DockerFileGenerator
from polyaxon.cli.check import check_polyaxonfile
from polyaxon.cli.errors import handle_cli_error
from polyaxon.config_reader import reader
from polyaxon.exceptions import (
    PolyaxonBuildException,
    PolyaxonException,
    PolyaxonSchemaError,
)
from polyaxon.logger import clean_outputs
from polyaxon.schemas.fields.docker_image import validate_image
from polyaxon.schemas.polyflow.init.build_context import BuildContextConfig
from polyaxon.specs import get_specification
from polyaxon.utils.formatting import Printer


@click.group()
@clean_outputs
def docker():
    pass


@docker.command()
@click.option(
    "-f",
    "--file",
    "polyaxonfile",
    multiple=True,
    type=click.Path(exists=True),
    help="The polyaxonfiles to generate the dockerfile from.",
)
@click.option(
    "--build-context", help="The build context config to generate the dockerfile from."
)
@click.option(
    "-dest", "--destination", help="The destination where to generate the build."
)
@click.option(
    "--params",
    "-P",
    metavar="NAME=VALUE",
    multiple=True,
    help="A parameter to override the default params of the run, form -P name=value.",
)
@clean_outputs
def generate(polyaxonfile, build_context, destination, params):
    """Generate a dockerfile given the polyaxonfile."""
    if all([polyaxonfile, build_context]):
        Printer.print_error(
            "Only a polyaxonfile or a build context option is required."
        )
        sys.exit(1)

    if build_context:
        try:
            build_context = BuildContextConfig.from_dict(reader.read(build_context))
        except (PolyaxonSchemaError, ValidationError) as e:
            Printer.print_error("received a non valid build context.")
            Printer.print_error("Error message: {}.".format(e))
            sys.exit(1)
    else:
        specification = check_polyaxonfile(polyaxonfile, params=params, log=False)

        try:
            run_spec = get_specification(specification.generate_run_data())
            run_spec.apply_params(params=specification.config.params)
            run_spec.apply_context()
        except PolyaxonSchemaError:
            Printer.print_error(
                "Could not run this polyaxonfile locally, "
                "a context is required to resolve it dependencies."
            )
            sys.exit(1)

        build_context = run_spec.build_context

    generator = DockerFileGenerator(
        build_context=build_context, destination=destination or "."
    )
    generator.create()
    Printer.print_success(
        "Dockerfile was generated: `{}`".format(generator.dockerfile_path)
    )


@docker.command()
@click.option(
    "-c",
    "--context",
    required=True,
    type=click.Path(exists=True),
    help="A build context accessible to Polyaxon.",
)
@click.option(
    "-d", "--destination", help="The tagged image destination $PROJECT/$IMAGE:$TAG."
)
@click.option(
    "--nocache",
    is_flag=True,
    default=False,
    show_default=False,
    help="To force rebuild the image.",
)
@click.option(
    "--max-retries",
    type=int,
    default=3,
    help="Number of times to retry the build process.",
)
@click.option(
    "--sleep-interval",
    type=int,
    default=2,
    help="Sleep interval between retries in seconds.",
)
@click.option(
    "--reraise",
    is_flag=True,
    default=False,
    show_default=False,
    help="To force rebuild the image.",
)
@clean_outputs
def build(context, destination, nocache, max_retries, sleep_interval, reraise):
    """Build a dockerfile, this command required Docker to be installed."""
    from polyaxon.builds.builder import build

    try:
        validate_image(destination)
    except ValidationError as e:
        handle_cli_error(e, message="Image destination is invalid.")

    try:
        build(
            context=context,
            destination=destination,
            nocache=nocache,
            max_retries=max_retries,
            sleep_interval=sleep_interval,
        )
    except PolyaxonBuildException as e:
        handle_cli_error(e, message="Docker build failed")
        if reraise:
            raise e
        sys.exit(1)


@docker.command()
@click.option(
    "-d", "--destination", help="The tagged image destination $PROJECT/$IMAGE:$TAG."
)
@click.option(
    "--max-retries",
    type=int,
    default=3,
    help="Number of times to retry the build process.",
)
@click.option(
    "--sleep-interval",
    type=int,
    default=2,
    help="Sleep interval between retries in seconds.",
)
@click.option(
    "--reraise",
    is_flag=True,
    default=False,
    show_default=False,
    help="To force rebuild the image.",
)
@clean_outputs
def push(destination, max_retries, sleep_interval, reraise):
    """Push an image, this command required Docker to be installed."""
    from polyaxon.builds.builder import push

    try:
        push(
            destination=destination,
            max_retries=max_retries,
            sleep_interval=sleep_interval,
        )
    except PolyaxonBuildException as e:
        handle_cli_error(e, message="Docker push failed")
        if reraise:
            raise e
        sys.exit(1)


@docker.command()
@click.option(
    "-c",
    "--context",
    required=True,
    type=click.Path(exists=True),
    help="A build context accessible to Polyaxon.",
)
@click.option(
    "-d", "--destination", help="The tagged image destination $PROJECT/$IMAGE:$TAG."
)
@click.option(
    "--nocache",
    is_flag=True,
    default=False,
    show_default=False,
    help="To force rebuild the image.",
)
@click.option(
    "--max-retries",
    type=int,
    default=3,
    help="Number of times to retry the build process.",
)
@click.option(
    "--sleep-interval",
    type=int,
    default=2,
    help="Sleep interval between retries in seconds.",
)
@click.option(
    "--reraise",
    is_flag=True,
    default=False,
    show_default=False,
    help="To force rebuild the image.",
)
@clean_outputs
def build_and_push(context, destination, nocache, max_retries, sleep_interval, reraise):
    """
    Build a dockerfile and push it to the provided registry,
    this command required Docker to be installed.
    """

    from polyaxon.builds.builder import build_and_push

    try:
        build_and_push(
            context=context,
            destination=destination,
            nocache=nocache,
            max_retries=max_retries,
            sleep_interval=sleep_interval,
        )
    except PolyaxonBuildException as e:
        handle_cli_error(e, message="Docker build and push failed")
        if reraise:
            raise e
        sys.exit(1)
