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

import click

from polyaxon import settings
from polyaxon.cli.errors import handle_cli_error
from polyaxon.deploy.schemas.deployment_types import DeploymentTypes
from polyaxon.managers.cli import CliConfigManager
from polyaxon.managers.client import ClientConfigManager
from polyaxon.utils.formatting import Printer


@click.command()
@click.option(
    "-p", "--port", type=int, help="The port to expose the gateway, default to 8000"
)
@click.option(
    "-n",
    "--namespace",
    type=str,
    help="The namespace used for deploying Polyaxon, default polyaxon.",
)
@click.option(
    "-t", "--deployment-type", help="Deployment type.",
)
@click.option(
    "-r",
    "--release-name",
    type=str,
    help="The release name used for deploying Polyaxon, default polyaxon.",
)
def port_forward(port, namespace, deployment_type, release_name):
    """If you deploy Polyaxon using ClusterIP, you can use this command
    to access the gateway through `localhost:port`.
    """
    from polyaxon.deploy.operators.kubectl import KubectlOperator

    if not port and deployment_type in [
        DeploymentTypes.MICRO_K8S,
        DeploymentTypes.MINIKUBE,
    ]:
        port = 31833
    port = port or 8000
    namespace = namespace or "polyaxon"
    release_name = release_name or "polyaxon"

    kubectl = KubectlOperator()
    args = [
        "port-forward",
        "-n",
        namespace,
        "svc/{}-polyaxon-gateway".format(release_name),
        "{}:80".format(port),
    ]

    try:
        _config = ClientConfigManager.get_config_or_default()
    except Exception as e:
        handle_cli_error(e, message="Polyaxon load configuration.")
        Printer.print_header(
            "You can reset your config by running: polyaxon config purge"
        )
        sys.exit(1)

    _config.host = "http://localhost:{}".format(port)
    ClientConfigManager.set_config(_config)
    CliConfigManager.purge()
    Printer.print_header("Client configuration is updated!")
    Printer.print_success("Polyaxon will be available at: {}".format(_config.host))
    stdout = kubectl.execute(
        args=args, is_json=False, stream=settings.CLIENT_CONFIG.debug
    )
    click.echo(stdout)
