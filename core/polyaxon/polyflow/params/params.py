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
from typing import Dict, Optional

import polyaxon_sdk

from marshmallow import ValidationError, fields, validates_schema

from polyaxon import types
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.params import PARAM_REGEX

INPUTS = "inputs"
OUTPUTS = "outputs"
INPUTS_OUTPUTS = "io"
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
    INPUTS_OUTPUTS,
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
    context_only = fields.Bool(allow_none=True)
    connection = fields.Str(allow_none=True)
    to_init = fields.Bool(allow_none=True)

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
    """Params can provide values to inputs/outputs.

    Params can be passed in several ways
        * literal values that the user sets manually.
        * a reference from a previous run, in which case
          Polyaxon will validate during the compilation time if the user who initiated the run
          has access to that organization/project/run.
        * a reference from an upstream operation in the context of a DAG.
        * a search, in which case the param will be a list of values based on the results
          from executing the search.


    When a param is passed from the CLI or directly in the YAML/Python specification,
    it will be validated against the [inputs/outputs](/docs/core/specification/io/)
    defined in the [component](/docs/core/specification/component/)

    Args:
         value: any
         search: V1SearchParam, optional
         ref: str, optional
         context_only: bool, optional
         connection: str, optional
         to_init: bool, optional

    ## YAML usage

    ```yaml
    >>> params:
    >>>   loss:
    >>>     value: MeanSquaredError
    >>>   preprocess:
    >>>     value: true
    >>>   accuracy:
    >>>     value: 0.1
    >>>   outputs_path:
    >>>     ref: ops.upstream-job1
    >>>     value: outputs.images_path
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1Param
    >>> params = {
    >>>     "loss": V1Param(value="MeanSquaredError"),
    >>>     "preprocess": V1Param(value=True),
    >>>     "accuracy": V1Param(value=0.1),
    >>>     "outputs-path": V1Param(ref="ops.upstream_job1", value="outputs.images_path")
    >>> }
    ```

    ## Fields

    ### value

    The value to pass, if no `ref` or `search` is passed then it corresponds to a literal value,
    and will be validated eagerly.
    Otherwise it will be a future validation during the compilation time.

    ```yaml
    >>> params:
    >>>   loss:
    >>>     value: MeanSquaredError
    ```

    The value could be coming from the [context](/docs/core/specification/context/), for example:

    ```yaml
    >>> params:
    >>>   current_project:
    >>>     value: {{globals.project_name}}
    >>>   current_run:
    >>>     value: {{globals.uuid}}
    ```

    ### ref

    Ref corresponds to a reference of an object.

    A reference could be a previous run in the database or
    an operation in DAG that has not been executed yet.

    ```yaml
    >>> params:
    >>>   loss:
    >>>     value: outputs.loss
    >>>     ref: ops.upstream-job-1
    ```

    ```yaml
    >>> params:
    >>>   loss:
    >>>     value: outputs.loss
    >>>     ref: runs.fcc462d764104eb698d3cca509f34154
    ```

    ### search

    A Search corresponds to a valid search that can be resolved by Polyaxon,
    the result will be injected to resolve the param value.

    ```yaml
    >>> params:
    >>>   paths:
    >>>     value: outputs.artifacts
    >>>     search: {query: "metrics.loss: <0.01", sort: "metrics.loss", limit: 5}
    ```

    ```python
    >>> params = {
    >>>     "paths": V1Param(
    >>>         value="outputs.artifacts",
    >>>         search=V1ParamSearch(query="metrics.loss: <0.01", sort="metrics.loss", limit=5),
    >>>     )
    >>> }
    ```

    This will expose the artifacts generated by
    the top 5 runs where the loss is less than 0.01 ascending.

    ### contextOnly

    A flag to signal to Polyaxon that this param should not be validated
    against the inputs/outputs, and it's only used to resolve some
    information and inject it into the context.

    ```yaml
    >>> params:
    >>>   convolutions:
    >>>     contextOnly: true
    >>>     value:
    >>>       conv1:
    >>>          kernels: [32, 32]
    >>>          size: [2, 2]
    >>>          strides: [1, 1]
    >>>       conv2:
    >>>          kernels: [64, 64]
    >>>          size: [2, 2]
    >>>          strides: [1, 1]
    ```

    Polyaxon will not check if this param was required by an input/output,
    and will inject it automatically in the context to be used.
    You can use for example `{{ convolutions.conv1 }}` in the specification.

    ### connection

    A connection to use with the parame.
    if the initial Input/Output definition has a predefined connection and this connection
    is provided, it will override the that value and will be added to the context.

    ### to_init

    if True the param will be converted to an init container.
    """

    SCHEMA = ParamSchema
    IDENTIFIER = "param"
    REDUCED_ATTRIBUTES = [
        "search",
        "ref",
        "contextOnly",
        "connection",
        "toInit",
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

    def get_spec(
        self,
        name: str,
        iotype: str,
        is_flag: bool,
        is_list: bool,
        is_context: bool,
        arg_format: str,
    ):
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

            value_parts = [s.strip() for s in value_parts.split(".")]
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

        return ParamSpec(
            name=name,
            iotype=iotype,
            param=self,
            is_flag=is_flag,
            is_list=is_list,
            is_context=is_context,
            arg_format=arg_format,
        )


class ParamSpec(
    namedtuple("ParamSpec", "name iotype param is_flag is_list is_context arg_format")
):
    def get_display_value(self):
        if self.is_flag:
            return "--{}".format(self.name) if self.param.value else ""
        return self.param.value

    def __repr__(self):
        return str(self.get_display_value())

    def as_str(self):
        return str(self)

    def as_arg(self):
        if self.iotype == types.BOOL:
            return "--{}".format(self.name) if self.param.value else ""
        if self.arg_format:
            return (
                self.arg_format.format(**{self.name: self.param.value})
                if self.param.value
                else ""
            )
        return "--{}={}".format(self.name, self.param.value)

    def to_parsed_param(self):
        parsed_param = {
            "connection": self.param.connection,
            "value": self.param.value,
            "type": self.iotype,
            "as_str": self.as_str(),
            "as_arg": self.as_arg(),
        }
        return parsed_param

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
                "and it does not correspond to the type of ref `{}.".format(
                    self.name, self.param.value, self.param.ref
                )
            )

        if self.is_list != context[self.param.searchable_ref].is_list:
            raise ValidationError(
                "Param `{}` has a an input type List[`{}`]"
                "and it does not correspond to the output type of ref `{}.".format(
                    self.name, self.param.value, self.param.ref
                )
            )
