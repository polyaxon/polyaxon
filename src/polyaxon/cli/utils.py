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

from polyaxon.utils.formatting import Printer, dict_tabulate, dict_to_tabulate


def get_entity_details(entity: str, entity_name: str):
    if entity.description:
        Printer.print_header("{} description:".format(entity_name))
        click.echo("{}\n".format(entity.description))

    if entity.settings:
        Printer.print_header("{} settings:".format(entity_name))
        click.echo("{}\n".format(entity.settings.to_dict()))

    response = dict_to_tabulate(
        entity.to_dict(),
        humanize_values=True,
        exclude_attrs=["description", "settings", "readme"],
    )

    Printer.print_header("{} info:".format(entity_name))
    dict_tabulate(response)
