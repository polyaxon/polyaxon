#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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
from polyaxon.utils.formatting import Printer


@click.command()
@click.argument("shell")
@clean_outputs
def completion(shell):
    """Show documentation for installing the auto-completion for polyaxon cli.

    Valid options: [bash, zsh, fish]

    \b
    $ polyaxon completion SHELL
    """

    if shell == "bash":
        Printer.print_header(
            "Please save the following scripts:",
        )
        click.echo(
            "_POLYAXON_COMPLETE=bash_source polyaxon > ~/.polyaxon-complete.bash"
        )
        click.echo("_PLX_COMPLETE=bash_source plx > ~/.plx-complete.bash")
        Printer.print_header(
            "Add the following lines to your: `~/.bashrc`",
        )
        click.echo("# Polyaxon completion")
        click.echo(". ~/.polyaxon-complete.bash")
        click.echo(". ~/.plx-complete.bash")
        Printer.print_header(
            "Reload your shell.",
        )
    elif shell == "zsh":
        Printer.print_header(
            "Please save the following scripts:",
        )
        click.echo("_POLYAXON_COMPLETE=zsh_source polyaxon > ~/.polyaxon-complete.zsh")
        click.echo("_PLX_COMPLETE=zsh_source plx > ~/.plx-complete.zsh")
        Printer.print_header(
            "Add the following lines to your: `~/.zshrc`",
        )
        click.echo("# Polyaxon completion")
        click.echo(". ~/.polyaxon-complete.zsh")
        click.echo(". ~/.plx-complete.zsh")
        Printer.print_header(
            "Reload your shell.",
        )
    elif shell == "fish":
        Printer.print_header(
            "Please save the following scripts under `~/.config/fish/completions`:",
        )
        click.echo(
            "_POLYAXON_COMPLETE=fish_source polyaxon > ~/.config/fish/completions/polyaxon-complete.fish"  # noqa
        )
        click.echo(
            "_PLX_COMPLETE=fish_source plx > ~/.config/fish/completions/plx-complete.fish"
        )
    else:
        click.echo("Shell {} is not supported.".format(shell))
    raise click.exceptions.Exit(1)
