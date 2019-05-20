# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import re
import six

from collections import namedtuple

from marshmallow import ValidationError

REGEX = re.compile(r'{{\s*([^\s]*)\s*}}')

OUTPUTS = 'outputs'
OPS = 'ops'
EXPERIMENTS = 'experiments'
JOBS = 'jobs'
ENTITIES = {JOBS, EXPERIMENTS, OPS}


class ParamSpec(namedtuple("ParamSpec", "name iotype value entity entity_ref")):
    pass


def get_param(name, value, iotype):
    """
    Checks if the value is param ref and validates it.

    returns: ParamSpec or None
    raises: ValidationError
    """
    if not isinstance(value, six.string_types):
        return None

    param = REGEX.search(value)
    if not param:
        return None

    param = param.group(1)
    param_parts = param.split('.')
    if len(param_parts) < 3 or len(param_parts) > 4:
        raise ValidationError('Could not parse value `{}` for param `{}`.'.format(value, name))
    if param_parts[2] != OUTPUTS:
        raise ValidationError('Param `{}` value `{}` is not valid, '
                              'it should follow a format '
                              '`entity.entity-id.outputs.name`.'.format(name, value))
    if param_parts[0] not in ENTITIES:
        raise ValidationError('Could not parse value `{}` for param `{}`.'.format(value, name))
    if param_parts[0] in {EXPERIMENTS, JOBS}:
        try:
            int(param_parts[1])
        except (KeyError, ValueError):
            raise ValidationError('Param value `{}` is not valid, '
                                  'it should provide an id.'.format(value))

    return ParamSpec(name=name,
                     iotype=iotype,
                     value=param,
                     entity=param_parts[0],
                     entity_ref=param_parts[1])


def validate_param(param, context):
    """
    Given a param reference to an operation, we check that the operation exists in the context,
    and that the types
    """
    if param.entity != OPS:
        return

    context = context or {}

    if param.value not in context:
        raise ValidationError(
            'Param `{}` has a ref value `{}`, '
            'but op with name `{}` has no such output, '
            'please check that your pipeline defines the correct template.'.format(
                param.name, param.value, param.entity_ref
            ))

    if param.iotype != context[param.value].iotype:
        raise ValidationError(
            'Param `{}` has a an input type `{}` '
            'and it does not correspond to the output type of ref `{}.'.format(
                param.name, param.iotype, param.entity_ref
            ))


def validate_params(params, inputs, outputs, context=None, is_template=True):
    """
    Validates Params given inputs, and an optional context.

    Params can be:
     * plain values: we check them against the inputs types
     * job/experiment references: We postpone to server side validation.
     * ops reference: in that case a context must be provided to validate that the reference exists.
        and types are correct.
    """
    if is_template and (not params or (not inputs and not outputs)):
        return

    params = params or {}
    inputs = inputs or []
    outputs = outputs or []

    validated_params = []

    for inp in inputs:
        if inp.name in params:
            param_value = params[inp.name]
            param = get_param(name=inp.name, value=param_value, iotype=inp.iotype)
            if param:
                validate_param(param, context)
            else:  # Plain value
                inp.validate_value(param_value)
            validated_params.append(inp.name)
        elif not inp.is_optional:
            raise ValidationError('Input {} is required, no param was passed.'.format(inp.name))

    for out in outputs:
        if out.name in params:
            param_value = params[out.name]
            param = get_param(name=out.name, value=param_value, iotype=out.iotype)
            if param:
                validate_param(param, None)
            else:  # Plain value
                out.validate_value(param_value)
            validated_params.append(out.name)
        elif not out.is_optional:
            raise ValidationError('Input {} is required, no param was passed.'.format(out.name))

    extra_params = set(six.iterkeys(params)) - set(validated_params)
    if extra_params:
        raise ValidationError('Received unexpected params `{}`.'.format(extra_params))
