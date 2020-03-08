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
import click_completion

from polyaxon.logger import clean_outputs


@click.command()
@click.option(
    "--append/--overwrite", help="Append the completion code to the file", default=None
)
@click.argument(
    "shell",
    required=False,
    type=click_completion.DocumentedChoice(click_completion.core.shells),
)
@click.argument("path", required=False)
@clean_outputs
def completion(append, shell, path):
    """Install the auto-completion for polyaxon-cli"""
    shell, path = click_completion.core.install(shell=shell, path=path, append=append)
    click.echo("%s completion installed in %s" % (shell, path))
