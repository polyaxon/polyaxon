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
import copy
import os

from collections import Mapping

from polyaxon.config_reader import reader
from polyaxon.exceptions import PolyaxonfileError
from polyaxon.polyaxonfile.specs import (
    CompiledOperationSpecification,
    OperationSpecification,
    get_specification,
    kinds,
)
from polyaxon.polyflow import V1Operation
from polyaxon.utils.list_utils import to_list

DEFAULT_POLYAXON_FILE_NAME = [
    "polyaxon",
    "polyaxonci",
    "polyaxon-ci",
    "polyaxon.ci",
    "polyaxonfile",
]

DEFAULT_POLYAXON_FILE_EXTENSION = ["yaml", "yml", "json"]


class PolyaxonFile:
    """Parses Polyaxonfiles, and validate that it respects the current file specification"""

    def __init__(self, filepaths):
        filepaths = to_list(filepaths)
        for filepath in filepaths:
            if not os.path.isfile(filepath):
                raise PolyaxonfileError("`{}` must be a valid file".format(filepath))
        self._filenames = [os.path.basename(filepath) for filepath in filepaths]

        self.config = get_specification(data=reader.read(filepaths))

    @property
    def filenames(self):
        return self._filenames

    @staticmethod
    def check_default_path(path):
        path = os.path.abspath(path)
        for filename in DEFAULT_POLYAXON_FILE_NAME:
            for ext in DEFAULT_POLYAXON_FILE_EXTENSION:
                filepath = os.path.join(path, "{}.{}".format(filename, ext))
                if os.path.isfile(filepath):
                    return filepath

    def get_op_specification(
        self, params=None, profile=None, queue=None, nocache=None
    ) -> V1Operation:
        job_data = {"version": self.config.version, "kind": kinds.OPERATION}
        if params:
            if not isinstance(params, Mapping):
                raise PolyaxonfileError(
                    "Params: `{}` must be a valid mapping".format(params)
                )
            job_data["params"] = params
        if profile:
            job_data["profile"] = profile
        if queue:
            job_data["queue"] = queue
        if nocache is not None:
            job_data["cache"] = {"disable": nocache}

        if self.config.kind == kinds.OPERATION:
            config = get_specification(data=[self.config.to_dict(), job_data])
        else:
            job_data["component"] = self.config.to_dict()
            config = get_specification(data=[job_data])
        params = copy.deepcopy(config.params)
        # Sanity check if params were passed
        run_config = OperationSpecification.compile_operation(config)
        run_config.validate_params(params=params, is_template=False)
        if run_config.is_dag_run:
            CompiledOperationSpecification.apply_context(run_config)
        return config
