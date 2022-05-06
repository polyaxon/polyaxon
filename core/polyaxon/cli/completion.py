#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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
        Printer.print_heading(
            "Please save the following scripts:",
        )
        Printer.print(
            "_POLYAXON_COMPLETE=bash_source polyaxon > ~/.polyaxon-complete.bash"
        )
        Printer.print("_PLX_COMPLETE=bash_source plx > ~/.plx-complete.bash")
        Printer.print_heading(
            "Add the following lines to your: `~/.bashrc`",
        )
        Printer.print_text(
            "# Polyaxon completion\n. ~/.polyaxon-complete.bash\n. ~/.plx-complete.bash"
        )
        Printer.print_heading(
            "Reload your shell.",
        )
    elif shell == "zsh":
        Printer.print_heading(
            "Please save the following scripts:",
        )
        Printer.print(
            "_POLYAXON_COMPLETE=zsh_source polyaxon > ~/.polyaxon-complete.zsh"
        )
        Printer.print("_PLX_COMPLETE=zsh_source plx > ~/.plx-complete.zsh")
        Printer.print_heading(
            "Add the following lines to your: `~/.zshrc`",
        )
        Printer.print_text(
            "# Polyaxon completion\n. ~/.polyaxon-complete.zsh\n. ~/.plx-complete.zsh"
        )
        Printer.print_heading(
            "Reload your shell.",
        )
    elif shell == "fish":
        Printer.print_heading(
            "Please save the following scripts under `~/.config/fish/completions`:",
        )
        Printer.print(
            "_POLYAXON_COMPLETE=fish_source polyaxon > ~/.config/fish/completions/polyaxon-complete.fish"  # noqa
        )
        Printer.print(
            "_PLX_COMPLETE=fish_source plx > ~/.config/fish/completions/plx-complete.fish"
        )
    else:
        Printer.print("Shell {} is not supported.".format(shell))
