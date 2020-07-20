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

from polyaxon.utils.formatting import Printer


@click.command()
def upload():  # pylint:disable=assign-to-new-keyword
    """Upload code of the current directory while respecting the .polyaxonignore file.

    > **Note**: Please note that this command has been temporarily disabled.
    """
    Printer.print_warning(
        "Please note that this command has been temporarily disabled."
    )
