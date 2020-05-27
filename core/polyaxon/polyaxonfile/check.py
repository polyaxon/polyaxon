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

import os

from collections import OrderedDict
from typing import Dict

from polyaxon.cli.errors import handle_cli_error
from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.exceptions import PolyaxonfileError
from polyaxon.polyaxonfile.manager import check_default_path, get_op_specification
from polyaxon.polyaxonfile.params import parse_params
from polyaxon.polyaxonfile.specs import get_specification, kinds
from polyaxon.polyflow import V1Operation
from polyaxon.utils.formatting import Printer, dict_tabulate
from polyaxon.utils.list_utils import to_list


def collect_references(config: V1Operation, path_context: str = None):
    if config.has_component_reference or (
        config.has_hub_reference and not config.has_public_hub_reference
    ):
        return config
    elif config.has_public_hub_reference:
        component = ConfigSpec.get_from(config.hub_ref, "hub").read()
    elif config.has_url_reference:
        component = ConfigSpec.get_from(config.url_ref, "url").read()
    elif config.has_path_reference:
        path_ref = config.path_ref
        if path_context:
            path_ref = os.path.join(
                os.path.dirname(os.path.abspath(path_context)), path_ref
            )
        component = ConfigSpec.get_from(path_ref).read()
    else:
        raise PolyaxonfileError("Operation found without component")

    component = get_specification(data=component)
    if component.kind != kinds.COMPONENT:
        if config.has_url_reference:
            ref_type = "Url ref"
            ref = config.url_ref
        else:
            ref_type = "Path ref"
            ref = config.path_ref
        raise PolyaxonfileError(
            "the reference ({}) `{}` is of kind `{}`, it should be a `{}`".format(
                ref, ref_type, component.kind, kinds.COMPONENT
            )
        )
    config.component = component
    return config


def check_polyaxonfile(
    polyaxonfile: str = None,
    python_module: str = None,
    url: str = None,
    hub: str = None,
    params: Dict = None,
    profile: str = None,
    queue: str = None,
    nocache: bool = None,
    log: bool = True,
    eager_hub: bool = True,
    is_cli: bool = True,
    to_op: bool = True,
):
    if sum([1 for i in [polyaxonfile, python_module, url, hub] if i]) > 1:
        message = (
            "You can only use one and only one option: "
            "hub, url, module, or path ro polyaxonfile.".format(hub)
        )
        if is_cli:
            Printer.print_error(message, sys_exit=True)
        else:
            raise PolyaxonfileError(message)
    if not any([polyaxonfile, python_module, url, hub]):
        polyaxonfile = check_default_path(path=".")
    if not any([polyaxonfile, python_module, url, hub]):
        polyaxonfile = ""
    if hub and not to_op:
        message = "Something went wrong, calling hub component `{}` without operation.".format(
            hub
        )
        if is_cli:
            Printer.print_error(message, sys_exit=True)
        else:
            raise PolyaxonfileError(message)

    polyaxonfile = to_list(polyaxonfile, check_none=True)

    parsed_params = None
    if params:
        parsed_params = parse_params(params, is_cli=is_cli)

    if not any([os.path.isfile(f) for f in polyaxonfile]) and not any(
        [python_module, url, hub]
    ):
        message = (
            "Please pass a valid polyaxonfile, a python module, url, or component name"
        )
        if is_cli:
            Printer.print_error(message, sys_exit=True)
        else:
            raise PolyaxonfileError(message)

    try:
        plx_file = None
        path_context = None
        public_hub = hub and "/" not in hub

        if not hub or (public_hub and eager_hub):
            if python_module:
                path_context = python_module[0]
                plx_file = ConfigSpec.get_from(python_module, config_type=".py").read()

            elif url:
                plx_file = ConfigSpec.get_from(url, "url").read()

            elif hub:
                plx_file = ConfigSpec.get_from(hub, "hub").read()

            else:
                path_context = polyaxonfile[0]
                plx_file = ConfigSpec.read_from(polyaxonfile)

            plx_file = get_specification(data=plx_file)
            if plx_file.kind == kinds.OPERATION:
                plx_file = collect_references(plx_file, path_context)

        if to_op or hub:
            plx_file = get_op_specification(
                hub=hub,
                config=plx_file,
                params=parsed_params,
                profile=profile,
                queue=queue,
                nocache=nocache,
                path_context=path_context,
            )
        if log and not is_cli:
            Printer.print_success("Polyaxonfile valid")
        return plx_file
    except Exception as e:
        message = "Polyaxonfile is not valid."
        if is_cli:
            handle_cli_error(e, message=message, sys_exit=True)
        else:
            raise PolyaxonfileError(message) from e


def check_polyaxonfile_kind(specification, kind):
    if specification.kind != kind:
        Printer.print_error(
            "Your polyaxonfile must be of kind: `{}`, "
            "received: `{}`.".format(kind, specification.kind),
            sys_exit=True,
        )


def get_matrix_info(kind, concurrency, early_stopping=False, **kwargs):
    info = OrderedDict()
    info["Matrix kind"] = kind.lower()
    info["Concurrency"] = (
        "{} runs".format("sequential")
        if concurrency == 1
        else "{} concurrent runs".format(concurrency)
    )
    info["Early stopping"] = "activated" if early_stopping else "deactivated"
    if "num_runs" in kwargs:
        info["Num of runs to create"] = kwargs["num_runs"]

    dict_tabulate(info)
