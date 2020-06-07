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

import click

from polyaxon.logger import clean_outputs


@click.command()
@click.option(
    "--port", type=int, help="The port to expose the gateway, default to 8000"
)
@click.option(
    "--namespace",
    type=int,
    help="The namespace used for deploying Polyaxon, default polyaxon.",
)
@click.option(
    "--release",
    type=int,
    help="The release name used for deploying Polyaxon, default polyaxon.",
)
@clean_outputs
def port_forward(port, namespace, release):
    """If you deploy Polyaxon using ClusterIP, you can use this command
    to access the gateway through `localhost:port`.
    """
    from polyaxon.deploy.operators.kubectl import KubectlOperator

    port = port or 8000
    namespace = namespace or "polyaxon"
    release = release or "polyaxon"

    kubectl = KubectlOperator()
    args = [
        "port-forward",
        "-n",
        namespace,
        "svc/{}-polyaxon-gateway".format(release),
        "{}:80".format(port),
    ]
    print("Polyaxon will be available at: localhost:{}".format(port))
    stdout = kubectl.execute(args=args, is_json=False)
    click.echo(stdout)
