# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from collections import Mapping

import rhea

from hestia.list_utils import to_list

from polyaxon.exceptions import PolyaxonfileError
from polyaxon.schemas.specs import get_specification

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

    def __init__(self, filepaths, params=None, debug_ttl=False, profile=None):
        filepaths = to_list(filepaths)
        for filepath in filepaths:
            if not os.path.isfile(filepath):
                raise PolyaxonfileError("`{}` must be a valid file".format(filepath))
        self._filenames = [os.path.basename(filepath) for filepath in filepaths]

        op_data = {"version": 0.6, "kind": "op"}
        if params:  # TODO: If params are provided we need to generate an op with params
            if not isinstance(params, Mapping):
                raise PolyaxonfileError(
                    "Params: `{}` must be a valid mapping".format(params)
                )
            op_data["params"] = params
        if profile:
            op_data["profile"] = profile
        if debug_ttl:
            if not isinstance(debug_ttl, int):
                raise PolyaxonfileError(
                    "Debug TTL `{}` must be a valid integer".format(debug_ttl)
                )
            op_data["termination"] = {"ttl": debug_ttl}

        specification = get_specification(data=rhea.read(filepaths))

        debug_cond = debug_ttl and not (
            specification.is_job or
            specification.is_service or
            (specification.is_operation and not (
                specification.is_template_job or specification.is_template_job
            ))
        )
        if debug_cond:
            raise PolyaxonfileError(
                "You can only trigger debug mode on a job/service specification, "
                "received instead a `{}` specification.".format(specification.kind)
            )
        if specification.is_operation:
            specification = get_specification(data=[specification.config.to_dict(), op_data])
        else:
            op_data["_template"] = specification.config.to_dict()
            specification = get_specification(data=[op_data])
        self.specification = specification

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
