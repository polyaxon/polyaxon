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
import uuid

from typing import Optional

from marshmallow import ValidationError

from polyaxon.contexts.params import PARAM_REGEX

OPS = "ops"
RUNS = "runs"
DAG = "dag"
DAG_ENTITY_REF = "_"
ENTITIES = {OPS, RUNS}

ENTITY_REF_FORMAT = "{}.{}"


def is_runs_ref(ref: str) -> bool:
    return ref.split(".")[0] == RUNS


def is_ops_ref(ref: str) -> bool:
    return ref.split(".")[0] == OPS


def is_dag_ref(ref: str) -> bool:
    return ref.split(".")[0] == DAG


def get_entity_ref(ref: str) -> Optional[str]:
    if is_ops_ref(ref) or is_runs_ref(ref):
        return ref.split(".")[1]
    if is_dag_ref(ref):
        return DAG_ENTITY_REF
    return None


def get_entity_type(value: str) -> str:
    value_parts = PARAM_REGEX.search(value)
    if value_parts:
        value_parts = value_parts.group(1).strip()
    else:
        value_parts = value

    return value_parts.split(".")[0]


def get_entity_value(value: str) -> str:
    value_parts = PARAM_REGEX.search(value)
    if value_parts:
        value_parts = value_parts.group(1).strip()
    else:
        value_parts = value

    value_parts = value_parts.split(".")
    if len(value_parts) < 2:
        return None
    return value_parts[-1]


def parse_ref_value(value: str) -> str:
    """Returns value without {{ }}"""
    value_parts = PARAM_REGEX.search(value)
    if value_parts:
        return value_parts.group(1).strip()
    return value


class RefMixin:
    @property
    def is_literal(self):
        return not self.ref

    @property
    def is_ref(self):
        return self.ref is not None

    @property
    def is_template_ref(self):
        try:
            value_parts = PARAM_REGEX.search(self.value)
            if value_parts:
                return True
        except Exception:  # noqa
            pass
        return False

    @property
    def is_runs_ref(self):
        if not self.is_ref:
            return False

        return is_runs_ref(self.ref)

    @property
    def is_ops_ref(self):
        if not self.is_ref:
            return False

        return is_ops_ref(self.ref)

    @property
    def is_dag_ref(self):
        if not self.is_ref:
            return False

        return is_dag_ref(self.ref)

    @property
    def is_join_ref(self):
        return False

    @property
    def entity_ref(self) -> Optional[str]:
        return get_entity_ref(self.ref)


def validate_ref(ref: str, name: str):
    # validate ref
    ref_parts = ref.split(".")
    if len(ref_parts) > 2:
        raise ValidationError(
            "Could not parse ref `{}` for param `{}`.".format(ref, name)
        )
    if len(ref_parts) == 1 and ref_parts[0] != DAG:
        raise ValidationError(
            "Could not parse ref `{}` for param `{}`.".format(ref_parts[0], name)
        )
    if len(ref_parts) == 2 and ref_parts[0] not in ENTITIES:
        raise ValidationError(
            "Could not parse ref `{}` for param `{}`. "
            "Operation ref must be one of `{}`".format(ref_parts[0], name, ENTITIES)
        )
    if ref_parts[0] == RUNS:
        try:
            uuid.UUID(ref_parts[1])
        except (KeyError, ValueError):
            raise ValidationError(
                "Param value `{}` should reference a valid run uuid.".format(
                    ref_parts[1]
                )
            )
