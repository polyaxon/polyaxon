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

import copy

from collections.abc import Mapping

from marshmallow import ValidationError

from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.exceptions import PolyaxonfileError
from polyaxon.pkg import SCHEMA_VERSION
from polyaxon.polyaxonfile.specs import kinds
from polyaxon.polyaxonfile.specs.sections import Sections
from polyaxon.utils.list_utils import to_list


class BaseSpecification(Sections):
    """Base abstract specification for plyaxonfiles and configurations."""

    _SPEC_KIND = None

    MAX_VERSION = (
        SCHEMA_VERSION  # Max Polyaxonfile specification version this CLI supports
    )
    MIN_VERSION = (
        SCHEMA_VERSION  # Min Polyaxonfile specification version this CLI supports
    )

    CONFIG = None

    @classmethod
    def check_version(cls, data):
        if data.get(cls.IS_PRESET):
            return
        if cls.VERSION not in data:
            raise PolyaxonfileError("The Polyaxonfile `version` must be specified.")
        if not cls.MIN_VERSION <= data[cls.VERSION] <= cls.MAX_VERSION:
            raise PolyaxonfileError(
                "The Polyaxonfile's version specified is not supported by your current CLI."
                "Your CLI support Polyaxonfile versions between: {} <= v <= {}."
                "You can run `polyaxon upgrade` and "
                "check documentation for the specification.".format(
                    cls.MIN_VERSION, cls.MAX_VERSION
                )
            )

    @classmethod
    def check_kind(cls, data):
        if cls.KIND not in data:
            raise PolyaxonfileError("The Polyaxonfile `kind` must be specified.")

        if data[cls.KIND] not in kinds.KINDS:
            raise PolyaxonfileError(
                "The Polyaxonfile with kind `{}` is not a supported value.".format(
                    data[cls.KIND]
                )
            )

    @classmethod
    def check_data(cls, data):
        cls.check_version(data)
        cls.check_kind(data)
        if data[cls.KIND] != cls._SPEC_KIND:
            raise PolyaxonfileError(
                "The specification used `{}` is incompatible with the kind `{}`.".format(
                    cls.__name__, data[cls.KIND]
                )
            )
        for key in set(data.keys()) - set(cls.SECTIONS):
            in_specification = "Polyaxonfile"
            if data.get(cls.VERSION):
                in_specification = "Polyaxonfile version `{}`".format(
                    data.get(cls.VERSION)
                )
            if data.get(cls.IS_PRESET):
                in_specification = "Polyaxonfile preset"

            raise PolyaxonfileError(
                "Unexpected section `{}` in {}. "
                "Please check the Polyaxonfile specification "
                "for this version.".format(key, in_specification)
            )

        for key in cls.REQUIRED_SECTIONS:
            if data.get(cls.IS_PRESET) and key == cls.VERSION:
                continue
            if key not in data:
                raise PolyaxonfileError(
                    "{} is a required section for a valid Polyaxonfile".format(key)
                )

    @classmethod
    def get_kind(cls, data):
        cls.check_kind(data=data)
        return data[cls.KIND]

    @classmethod
    def read(cls, values):
        if isinstance(values, cls.CONFIG):
            return values

        if not isinstance(values, Mapping) or Sections.KIND not in values:
            values = to_list(values)
            values = ConfigSpec.read_from([{Sections.KIND: cls._SPEC_KIND}] + values)
        cls.check_data(values)
        try:
            config = cls.CONFIG.from_dict(copy.deepcopy(values))
        except TypeError as e:
            raise ValidationError(
                "Received a non valid config `{}`: `{}`".format(cls._SPEC_KIND, e)
            )
        return config
