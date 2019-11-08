#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

import os

from collections import Mapping

import rhea

from hestia.list_utils import to_list

from polyaxon import kinds
from polyaxon.exceptions import PolyaxonfileError
from polyaxon.specs import get_specification

DEFAULT_POLYAXON_FILE_NAME = [
    "polyaxon",
    "polyaxonci",
    "polyaxon-ci",
    "polyaxon.ci",
    "polyaxonfile",
]

DEFAULT_POLYAXON_FILE_EXTENSION = ["yaml", "yml", "json"]


class PolyaxonFile(object):
    """Parses Polyaxonfiles, and validate that it respects the current file specification"""

    def __init__(self, filepaths):
        filepaths = to_list(filepaths)
        for filepath in filepaths:
            if not os.path.isfile(filepath):
                raise PolyaxonfileError("`{}` must be a valid file".format(filepath))
        self._filenames = [os.path.basename(filepath) for filepath in filepaths]

        self.specification = get_specification(data=rhea.read(filepaths))

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

    def get_op_specification(self, params=None, profile=None):
        job_data = {"version": self.specification.version, "kind": kinds.OP}
        if params:
            if not isinstance(params, Mapping):
                raise PolyaxonfileError(
                    "Params: `{}` must be a valid mapping".format(params)
                )
            job_data["params"] = params
        if profile:
            job_data["profile"] = profile

        if self.specification.is_op:
            specification = get_specification(
                data=[self.specification.config.to_dict(), job_data]
            )
        else:
            job_data["component"] = self.specification.config.to_dict()
            specification = get_specification(data=[job_data])
        # Sanity check if params were passed
        run_spec = get_specification(specification.generate_run_data())
        run_spec.validate_params(params=params, is_template=False)
        if run_spec.has_dag:
            run_spec.apply_context()
        return specification
