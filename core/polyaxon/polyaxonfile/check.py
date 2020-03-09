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
import sys

from collections import OrderedDict

from polyaxon.cli.errors import handle_cli_error
from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.polyaxonfile.manager import PolyaxonFile
from polyaxon.polyaxonfile.params import parse_params
from polyaxon.utils import constants
from polyaxon.utils.formatting import Printer, dict_tabulate
from polyaxon.utils.list_utils import to_list


def check_polyaxonfile(
    polyaxonfile=None,
    python_module=None,
    params=None,
    profile=None,
    queue=None,
    nocache=None,
    log=True,
):
    if not any([polyaxonfile, python_module]):
        polyaxonfile = PolyaxonFile.check_default_path(path=".")
    if not any([polyaxonfile, python_module]):
        polyaxonfile = ""

    polyaxonfile = to_list(polyaxonfile)
    exists = [os.path.isfile(f) for f in polyaxonfile]

    parsed_params = None
    if params:
        parsed_params = parse_params(params)

    if not any(exists) and not python_module:
        Printer.print_error(
            "Polyaxonfile is not present, "
            "please run {}".format(constants.INIT_COMMAND)
        )
        sys.exit(1)

    if python_module:
        config = ConfigSpec.get_from(python_module)
        return config.read()

    try:
        plx_file = PolyaxonFile(polyaxonfile)
        plx_file = plx_file.get_op_specification(
            params=parsed_params, profile=profile, queue=queue, nocache=nocache
        )
        if log:
            Printer.print_success("Polyaxonfile valid")
        return plx_file
    except Exception as e:
        handle_cli_error(e, message="Polyaxonfile is not valid.")
        sys.exit(1)


def check_polyaxonfile_kind(specification, kind):
    if specification.kind != kind:
        Printer.print_error(
            "Your polyaxonfile must be of kind: `{}`, "
            "received: `{}`.".format(kind, specification.kind)
        )
        sys.exit(-1)


def get_parallel_info(kind, concurrency, early_stopping=False, **kwargs):
    info = OrderedDict()
    info["Parallel kind"] = kind.lower()
    info["Concurrency"] = (
        "{} runs".format("sequential")
        if concurrency == 1
        else "{} concurrent runs".format(concurrency)
    )
    info["Early stopping"] = "activated" if early_stopping else "deactivated"
    if "num_runs" in kwargs:
        info["Num of runs to create"] = kwargs["num_runs"]

    dict_tabulate(info)
