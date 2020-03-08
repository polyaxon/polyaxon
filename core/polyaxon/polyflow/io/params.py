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
import uuid

from collections import namedtuple
from typing import Dict, List, Optional, Union

import polyaxon_sdk

from marshmallow import ValidationError, fields, validates_schema

from polyaxon.polyflow.io.io import V1IO
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.params import PARAM_REGEX

INPUTS = "inputs"
OUTPUTS = "outputs"
ARTIFACTS = "artifacts"
EVENTS = "events"
STATUS = "status"
NAME = "name"
UUID = "uuid"
PROJECT_NAME = "project_name"
PROJECT_UUID = "project_uuid"
ITERATION = "iteration"
CONTEXTS = {
    INPUTS,
    OUTPUTS,
    ARTIFACTS,
    EVENTS,
    STATUS,
    NAME,
    UUID,
    PROJECT_NAME,
    PROJECT_UUID,
    ITERATION,
}
CONTEXTS_WITH_NESTING = {
    INPUTS,
    OUTPUTS,
    ARTIFACTS,
    EVENTS,
}

OPS = "ops"
RUNS = "runs"
DAG = "dag"
DAG_ENTITY_REF = "_"
ENTITIES = {OPS, RUNS}


def validate_param_value(value, search, ref):
    if search and ref:
        raise ValidationError(
            "Only one field `ref` or `search` is possible, received both:\n"
            "ref: {}\n"
            "search: {}".format(ref, search)
        )
    if (search or ref) and not isinstance(value, str):
        raise ValidationError(
            "Value `{}` must be of type string when a search or ref is provided.".format(
                value
            )
        )


class ParamSearchSchema(BaseCamelSchema):
    query = fields.Str(required=True)
    sort = fields.Str(allow_none=True)
    limit = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return V1ParamSearch


class V1ParamSearch(BaseConfig, polyaxon_sdk.V1ParamSearch):
    SCHEMA = ParamSearchSchema
    IDENTIFIER = "search_param"
    REDUCED_ATTRIBUTES = [
        "sort",
        "limit",
    ]


class ParamSchema(BaseCamelSchema):
    value = fields.Raw(required=True)
    search = fields.Nested(ParamSearchSchema, allow_none=True)
    ref = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return V1Param

    @validates_schema
    def validate_param(self, values, **kwargs):
        validate_param_value(
            value=values.get("value"),
            search=values.get("search"),
            ref=values.get("ref"),
        )


class V1Param(BaseConfig, polyaxon_sdk.V1Param):
    SCHEMA = ParamSchema
    IDENTIFIER = "param"
    REDUCED_ATTRIBUTES = [
        "search",
        "ref",
    ]

    def validate(self):
        validate_param_value(
            value=self.value, search=self.search, ref=self.ref,
        )

    @property
    def is_literal(self):
        return not any([self.search, self.ref])

    @property
    def is_ref(self):
        return self.ref is not None

    @property
    def is_runs_ref(self):
        if not self.is_ref:
            return False

        return self.ref.split(".")[0] == RUNS

    @property
    def is_ops_ref(self):
        if not self.is_ref:
            return False

        return self.ref.split(".")[0] == OPS

    @property
    def is_dag_ref(self):
        if not self.is_ref:
            return False

        return self.ref.split(".")[0] == DAG

    @property
    def is_search(self):
        return self.search is not None

    @property
    def entity_ref(self) -> Optional[str]:
        if self.is_ops_ref or self.is_runs_ref:
            return self.ref.split(".")[1]
        if self.is_dag_ref:
            return DAG_ENTITY_REF
        return None

    @property
    def entity_value(self) -> Optional[str]:
        if not self.is_ref:
            return None
        value_parts = PARAM_REGEX.search(self.value)
        if value_parts:
            value_parts = value_parts.group(1)
        else:
            value_parts = self.value

        return value_parts.split(".")[-1]

    @property
    def searchable_ref(self) -> str:
        if not self.is_ref:
            return ""
        return "{}.{}".format(self.ref, self.value)

    def get_spec(self, name: str, iotype: str, is_flag: bool):
        """
        Checks if the value is param ref and validates it.

        returns: ParamSpec or None
        raises: ValidationError
        """
        if not self.is_literal:
            # value validation is the same for search and ref
            value_parts = PARAM_REGEX.search(self.value)
            if value_parts:
                value_parts = value_parts.group(1)
            else:
                value_parts = self.value

            value_parts = value_parts.split(".")
            if len(value_parts) > 3:
                raise ValidationError(
                    "Could not parse value `{}` for param `{}`.".format(
                        self.value, name
                    )
                )
            if len(value_parts) == 1 and value_parts[0] not in CONTEXTS:
                raise ValidationError(
                    "Received an invalid value `{}` for param `{}`. "
                    "Value must be one of `{}`".format(self.value, name, CONTEXTS)
                )
            # Check the case of current DAG, it should not allow to use outputs
            if len(value_parts) == 1 and self.is_dag_ref and value_parts[0] == OUTPUTS:
                raise ValidationError(
                    "Received an invalid value `{}` for param `{}`. "
                    "You can not use `{}` of current dag".format(
                        self.value, name, OUTPUTS
                    )
                )
            if len(value_parts) == 2 and value_parts[0] not in CONTEXTS_WITH_NESTING:
                raise ValidationError(
                    "Received an invalid value `{}` for param `{}`. "
                    "Value `{}` must be one of `{}`".format(
                        self.value, name, value_parts[0], CONTEXTS_WITH_NESTING
                    )
                )
            if len(value_parts) == 3 and value_parts[0] != EVENTS:
                raise ValidationError(
                    "Received an invalid value `{}` for param `{}`. "
                    "Value `{}` must can only be equal to `{}`".format(
                        self.value, name, value_parts[0], EVENTS
                    )
                )
        if self.is_ref:
            # validate ref
            ref_parts = self.ref.split(".")
            if len(ref_parts) > 2:
                raise ValidationError(
                    "Could not parse ref `{}` for param `{}`.".format(self.ref, name)
                )
            if len(ref_parts) == 1 and ref_parts[0] != DAG:
                raise ValidationError(
                    "Could not parse ref `{}` for param `{}`.".format(
                        ref_parts[0], name
                    )
                )
            if len(ref_parts) == 2 and ref_parts[0] not in ENTITIES:
                raise ValidationError(
                    "Could not parse ref `{}` for param `{}`. "
                    "Ref must be one of `{}`".format(ref_parts[0], name, ENTITIES)
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

        return ParamSpec(name=name, iotype=iotype, param=self, is_flag=is_flag,)


class ParamSpec(namedtuple("ParamSpec", "name iotype param is_flag")):
    @property
    def display_value(self):
        if self.is_flag:
            return "--{}".format(self.name) if self.param.value else ""
        return self.param.value

    def validate_ref(
        self,
        context: Optional[Dict],
        is_template: bool = False,
        check_runs: bool = False,
    ):
        """
        Given a param reference to an operation, we check that the operation exists in the context,
        and that the types
        """
        if is_template or (self.param.is_runs_ref and not check_runs):
            return

        context = context or {}

        if self.param.searchable_ref not in context:
            raise ValidationError(
                "Param `{}` has a ref value `{}`, "
                "but reference with name `{}` has no such information, "
                "please check that your dag defines the correct template.".format(
                    self.name, self.param.value, self.param.ref
                )
            )

        if self.iotype != context[self.param.searchable_ref].iotype:
            raise ValidationError(
                "Param `{}` has a an input type `{}` "
                "and it does not correspond to the output type of ref `{}.".format(
                    self.name, self.param.value, self.param.ref
                )
            )


def validate_params(
    params: Dict[str, Union[Dict, V1Param]],
    inputs: List[V1IO],
    outputs: List[V1IO],
    context: Dict = None,
    is_template: bool = True,
    check_runs: bool = False,
    extra_info: str = None,
) -> List[ParamSpec]:
    """
    Validates Params given inputs, and an optional context.

    Params can be:
     * plain values: we check them against the inputs types
     * job/experiment references: We postpone to server side validation.
     * ops reference: in that case a context must be provided to validate that the reference exists.
        and types are correct.
    """
    if requires_params(inputs, outputs):
        if not is_template and not params:
            message = (
                "The Polyaxonfile has non optional inputs/outputs, "
                "you need to pass valid params."
            )
            if extra_info:
                message += " Please check: {}".format(extra_info)

            raise ValidationError(message)
    elif not accepts_params(inputs, outputs) and params:
        message = "Received unexpected params `{}`.".format(params)
        if extra_info:
            message += " Please check: {}".format(extra_info)
        raise ValidationError(message)

    def parse_param(v):
        if isinstance(v, V1Param):
            return v
        return V1Param.read(v, config_type=".yaml")

    params = params or {}
    params = {k: parse_param(params[k]) for k in params}
    inputs = inputs or []
    outputs = outputs or []

    processed_params = []
    validated_params = []

    for inp in inputs:
        if inp.name in params:
            param_value = params[inp.name]
            param_spec = param_value.get_spec(
                name=inp.name, iotype=inp.iotype, is_flag=inp.is_flag
            )
            if param_spec.param.is_ref:
                param_spec.validate_ref(context, is_template, check_runs)
            else:  # Plain value
                inp.validate_value(param_value.value)
            validated_params.append(param_spec)
            processed_params.append(inp.name)
        elif not inp.is_optional and not is_template:
            message = "Input {} is required, no param was passed.".format(inp.name)
            if extra_info:
                message += " Please check: {}".format(extra_info)
            raise ValidationError(message)
        else:
            validated_params.append(
                ParamSpec(
                    name=inp.name,
                    param=V1Param(value=inp.value),
                    iotype=inp.iotype,
                    is_flag=inp.is_flag,
                )
            )

    for out in outputs:
        if out.name in params:
            param_value = params[out.name]
            param_spec = param_value.get_spec(
                name=out.name, iotype=out.iotype, is_flag=out.is_flag
            )
            validated_params.append(param_spec)
            if param_spec.param.is_ref:
                param_spec.validate_ref(None, is_template=False, check_runs=check_runs)
            else:  # Plain value
                out.validate_value(param_value.value)
            validated_params.append(param_spec)
            processed_params.append(out.name)
        # No validation for outputs we assume that the op might populate a context or send a metric
        else:
            validated_params.append(
                ParamSpec(
                    name=out.name,
                    param=V1Param(value=out.value),
                    iotype=out.iotype,
                    is_flag=out.is_flag,
                )
            )
    extra_params = set(params.keys()) - set(processed_params)
    if extra_params:
        message = "Received unexpected params `{}`.".format(extra_params)
        if extra_info:
            message += " Please check: {}".format(extra_info)
        raise ValidationError(message)

    return validated_params


def requires_params(inputs: List[V1IO], outputs: List[V1IO]):
    if not inputs and not outputs:
        return False

    def parse_io(ios: List[V1IO], delay_validation: bool):
        if not ios:
            return False
        for i in ios:
            delay_validation = (
                i.delay_validation
                if i.delay_validation is not None
                else delay_validation
            )
            if not i.is_optional and not delay_validation:
                return True
        return False

    if parse_io(inputs, False):
        return True

    if parse_io(outputs, True):
        return True

    return False


def accepts_params(inputs: List[V1IO], outputs: List[V1IO]):
    return bool(inputs or outputs)


def get_upstream_op_params_by_names(params: Dict[str, V1Param]):
    upstream = {}

    if not params:
        return upstream

    for param in params:
        param_ref = params[param].get_spec(name=param, iotype=None, is_flag=None)
        if param_ref and param_ref.param.is_ops_ref:
            if param_ref.param.entity_ref in upstream:
                upstream[param_ref.param.entity_ref].append(param_ref)
            else:
                upstream[param_ref.param.entity_ref] = [param_ref]

    return upstream


def get_upstream_run_params_by_names(params: Dict[str, V1Param]):
    upstream = {}

    if not params:
        return upstream

    for param in params:
        param_ref = params[param].get_spec(name=param, iotype=None, is_flag=None)
        if param_ref and param_ref.param.is_runs_ref:
            if param_ref.param.entity_ref in upstream:
                upstream[param_ref.param.entity_ref].append(param_ref)
            else:
                upstream[param_ref.param.entity_ref] = [param_ref]

    return upstream


def get_dag_params_by_names(params: Dict[str, V1Param]):
    upstream = {}

    if not params:
        return upstream

    for param in params:
        param_ref = params[param].get_spec(name=param, iotype=None, is_flag=None)
        if param_ref and param_ref.param.is_dag_ref:
            if param_ref.param.entity_ref in upstream:
                upstream[param_ref.param.entity_ref].append(param_ref)
            else:
                upstream[param_ref.param.entity_ref] = [param_ref]

    return upstream
