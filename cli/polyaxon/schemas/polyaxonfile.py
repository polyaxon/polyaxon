# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from collections import Mapping

import rhea

from hestia.list_utils import to_list

from polyaxon.exceptions import PolyaxonfileError
from polyaxon.schemas.ops.termination import TerminationConfig
from polyaxon.schemas.polyflow.ops import OpConfig
from polyaxon.schemas.specs import get_specification, kinds

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

    def get_op_specification(self, params=None, debug_ttl=False, profile=None):
        op_data = OpConfig(version=self.specification.version, kind=kinds.OPERATION)
        if params:
            if not isinstance(params, Mapping):
                raise PolyaxonfileError(
                    "Params: `{}` must be a valid mapping".format(params)
                )
            op_data.params = params
        if profile:
            op_data.profile = profile
        if debug_ttl:
            if not isinstance(debug_ttl, int):
                raise PolyaxonfileError(
                    "Debug TTL `{}` must be a valid integer".format(debug_ttl)
                )
            op_data.termination = TerminationConfig(ttl=debug_ttl)

        debug_cond = debug_ttl and not (
            self.specification.is_job
            or self.specification.is_service
            or (
                self.specification.is_operation
                and not (
                    self.specification.is_template_job
                    or self.specification.is_template_job
                )
            )
        )
        if debug_cond:
            raise PolyaxonfileError(
                "You can only trigger debug mode on a job/service specification, "
                "received instead a `{}` specification.".format(self.specification.kind)
            )

        if self.specification.is_operation:
            specification = get_specification(
                data=[self.specification.config.to_dict(), op_data.to_dict()]
            )
        else:
            op_data._template = self.specification.config
            specification = get_specification(data=[op_data.to_dict()])
        # Sanity check if params were passed
        run_spec = get_specification(specification.generate_run_data())
        run_spec.validate_params(params=op_data.params)
        return specification
