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

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six
import uuid

from collections import namedtuple

from marshmallow import ValidationError

from polyaxon.schemas.fields.params import PARAM_REGEX

OUTPUTS = "outputs"
OPS = "ops"
RUNS = "runs"
PIPELINE = "pipeline"
ENTITIES = {OPS, RUNS, PIPELINE}


class ParamSpec(
    namedtuple("ParamSpec", "name iotype value entity entity_ref entity_value is_flag")
):
    @property
    def display_value(self):
        if self.is_flag:
            return "--{}".format(self.name) if self.value else ""
        return self.value

    def set_value(self, value):
        return ParamSpec(
            name=self.name,
            iotype=self.iotype,
            value=value,
            entity=self.entity,
            entity_ref=self.entity_ref,
            entity_value=self.entity_value,
            is_flag=self.is_flag,
        )


def get_param(name, value, iotype, is_flag):
    """
    Checks if the value is param ref and validates it.

    returns: ParamSpec or None
    raises: ValidationError
    """
    if not isinstance(value, six.string_types):
        return ParamSpec(
            name=name,
            iotype=iotype,
            value=value,
            entity=None,
            entity_ref=None,
            entity_value=None,
            is_flag=is_flag,
        )

    param = PARAM_REGEX.search(value)
    if not param:
        return ParamSpec(
            name=name,
            iotype=iotype,
            value=value,
            entity=None,
            entity_ref=None,
            entity_value=None,
            is_flag=is_flag,
        )

    param = param.group(1)
    param_parts = param.split(".")
    if len(param_parts) < 3 or len(param_parts) > 4:
        raise ValidationError(
            "Could not parse value `{}` for param `{}`.".format(value, name)
        )
    if param_parts[2] != OUTPUTS:
        raise ValidationError(
            "Param `{}` value `{}` is not valid, "
            "it should follow a format "
            "`entity.entity-id.outputs.name`.".format(name, value)
        )
    if param_parts[0] not in ENTITIES:
        raise ValidationError(
            "Could not parse value `{}` for param `{}`.".format(value, name)
        )
    if param_parts[0] == RUNS:
        try:
            uuid.UUID(param_parts[1])
        except (KeyError, ValueError):
            raise ValidationError(
                "Param value `{}` should reference a valid uuid.".format(
                    value, param_parts[1]
                )
            )

    return ParamSpec(
        name=name,
        iotype=iotype,
        value=param,
        entity=param_parts[0],
        entity_ref=param_parts[1],
        entity_value=param_parts[3],
        is_flag=is_flag,
    )


def validate_param(param, context, is_template=False, check_runs=False):
    """
    Given a param reference to an operation, we check that the operation exists in the context,
    and that the types
    """
    if is_template or (param.entity == RUNS and not check_runs):
        return

    context = context or {}

    if param.value not in context:
        raise ValidationError(
            "Param `{}` has a ref value `{}`, "
            "but op with name `{}` has no such output, "
            "please check that your pipeline defines the correct template.".format(
                param.name, param.value, param.entity_ref
            )
        )

    if param.iotype != context[param.value].iotype:
        raise ValidationError(
            "Param `{}` has a an input type `{}` "
            "and it does not correspond to the output type of ref `{}.".format(
                param.name, param.iotype, param.entity_ref
            )
        )


def validate_params(
    params, inputs, outputs, context=None, is_template=True, check_runs=False
):
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
            raise ValidationError(
                "The Polyaxonfile has non optional inputs/outputs, "
                "you need to pass valid params."
            )
    elif not accepts_params(inputs, outputs) and params:
        raise ValidationError("Received unexpected params `{}`.".format(params))

    params = params or {}
    inputs = inputs or []
    outputs = outputs or []

    processed_params = []
    validated_params = []

    for inp in inputs:
        if inp.name in params:
            param_value = params[inp.name]
            param = get_param(
                name=inp.name, value=param_value, iotype=inp.iotype, is_flag=inp.is_flag
            )
            if param.entity_ref:
                validate_param(param, context, is_template, check_runs)
            else:  # Plain value
                inp.validate_value(param_value)
            validated_params.append(param)
            processed_params.append(inp.name)
        elif not inp.is_optional and not is_template:
            raise ValidationError(
                "Input {} is required, no param was passed.".format(inp.name)
            )
        else:
            validated_params.append(
                ParamSpec(
                    name=inp.name,
                    value=inp.value,
                    iotype=inp.iotype,
                    entity=None,
                    entity_ref=None,
                    entity_value=None,
                    is_flag=inp.is_flag,
                )
            )

    for out in outputs:
        if out.name in params:
            param_value = params[out.name]
            param = get_param(
                name=out.name, value=param_value, iotype=out.iotype, is_flag=out.is_flag
            )
            validated_params.append(param)
            if param.entity_ref:
                validate_param(param, None, is_template=False, check_runs=check_runs)
            else:  # Plain value
                out.validate_value(param_value)
            validated_params.append(param)
            processed_params.append(out.name)
        # No validation for outputs we assume that the op might populate a context or send a metric
        else:
            validated_params.append(
                ParamSpec(
                    name=out.name,
                    value=out.value,
                    iotype=out.iotype,
                    entity=None,
                    entity_ref=None,
                    entity_value=None,
                    is_flag=out.is_flag,
                )
            )
    extra_params = set(six.iterkeys(params)) - set(processed_params)
    if extra_params:
        raise ValidationError("Received unexpected params `{}`.".format(extra_params))

    return validated_params


def requires_params(inputs, outputs):
    if not inputs and not outputs:
        return False

    def parse_io(io):
        if not io:
            return False
        for i in io:
            if not i.is_optional:
                return True
        return False

    if parse_io(inputs):
        return True

    if parse_io(outputs):
        return True

    return False


def accepts_params(inputs, outputs):
    return bool(inputs or outputs)


def get_params_with_refs(params):
    return [param for param in params if param.entity_ref]


def get_upstream_op_params_by_names(params):
    upstream = {}

    if not params:
        return upstream

    for param in params:
        param_ref = get_param(
            name=param, value=params[param], iotype=None, is_flag=None
        )
        if param_ref and param_ref.entity == OPS:
            if param_ref.entity_ref in upstream:
                upstream[param_ref.entity_ref].append(param_ref)
            else:
                upstream[param_ref.entity_ref] = [param_ref]

    return upstream


def get_upstream_run_params_by_names(params):
    upstream = {}

    if not params:
        return upstream

    for param in params:
        param_ref = get_param(
            name=param, value=params[param], iotype=None, is_flag=None
        )
        if param_ref and param_ref.entity == RUNS:
            if param_ref.entity_ref in upstream:
                upstream[param_ref.entity_ref].append(param_ref)
            else:
                upstream[param_ref.entity_ref] = [param_ref]

    return upstream
