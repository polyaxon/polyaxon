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


class ParamSpec(namedtuple("ParamSpec", "name iotype value entity entity_ref is_flag")):
    pass


def get_param_display_value(param, value):
    if param.is_flag:
        return '--{}'.format(param.name) if value else ''
    return value


def get_param(name, value, iotype, is_flag):
    """
    Checks if the value is param ref and validates it.

    returns: ParamSpec or None
    raises: ValidationError
    """
    if not isinstance(value, six.string_types):
        return ParamSpec(name=name,
                         iotype=iotype,
                         value=value,
                         entity=None,
                         entity_ref=None,
                         is_flag=is_flag)

    param = REGEX.search(value)
    if not param:
        return ParamSpec(name=name,
                         iotype=iotype,
                         value=value,
                         entity=None,
                         entity_ref=None,
                         is_flag=is_flag)

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
                     entity_ref=param_parts[1],
                     is_flag=is_flag)


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


def validate_params(params, inputs, outputs, context=None, is_template=True, is_run=True):
    """
    Validates Params given inputs, and an optional context.

    Params can be:
     * plain values: we check them against the inputs types
     * job/experiment references: We postpone to server side validation.
     * ops reference: in that case a context must be provided to validate that the reference exists.
        and types are correct.
    """
    if is_run and not inputs and not outputs:
        return []

    params = params or {}
    inputs = inputs or []
    outputs = outputs or []

    processed_params = []
    validated_params = []

    for inp in inputs:
        if inp.name in params:
            param_value = params[inp.name]
            param = get_param(name=inp.name,
                              value=param_value,
                              iotype=inp.iotype,
                              is_flag=inp.is_flag)
            if param.entity_ref:
                validate_param(param, context)
            else:  # Plain value
                inp.validate_value(param_value)
            validated_params.append(param)
            processed_params.append(inp.name)
        elif not inp.is_optional and not is_template:
            raise ValidationError('Input {} is required, no param was passed.'.format(inp.name))
        else:
            validated_params.append(ParamSpec(name=inp.name,
                                              value=inp.default,
                                              iotype=inp.iotype,
                                              entity=None,
                                              entity_ref=None,
                                              is_flag=inp.is_flag))

    for out in outputs:
        if out.name in params:
            param_value = params[out.name]
            param = get_param(name=out.name,
                              value=param_value,
                              iotype=out.iotype,
                              is_flag=out.is_flag)
            validated_params.append(param)
            if param.entity_ref:
                validate_param(param, None)
            else:  # Plain value
                out.validate_value(param_value)
            validated_params.append(param)
            processed_params.append(out.name)
        # No validation for outputs we assume that the op might populate a context or send a metric
        else:
            validated_params.append(ParamSpec(name=out.name,
                                              value=out.default,
                                              iotype=out.iotype,
                                              entity=None,
                                              entity_ref=None,
                                              is_flag=out.is_flag))
    extra_params = set(six.iterkeys(params)) - set(processed_params)
    if extra_params:
        raise ValidationError('Received unexpected params `{}`.'.format(extra_params))

    return validated_params
