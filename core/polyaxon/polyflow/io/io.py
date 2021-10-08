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
from typing import Any, List

import polyaxon_sdk

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon import types
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.parser import parser
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.utils.signal_decorators import check_partial

IO_NAME_BLACK_LIST = ["globals", "params", "connections"]
IO_NAME_ERROR = (
    "Received an input/output with a name in {}, "
    "please use a different name that does "
    "not already taken by the context".format(IO_NAME_BLACK_LIST)
)


def validate_io_value(
    name: str,
    type: str,
    value: Any,
    default: Any,
    is_optional: bool,
    is_list: bool,
    options: List[Any],
    parse: bool = True,
):
    try:
        parsed_value = parser.TYPE_MAPPING[type](
            key=name,
            value=value,
            is_list=is_list,
            is_optional=is_optional,
            default=default,
            options=options,
        )
        if parse:
            return parsed_value
        # Return the original value, the parser will return specs sometimes
        if value is not None:
            return value
        return default
    except PolyaxonSchemaError as e:
        raise ValidationError(
            "Could not parse value `%s`, an error was encountered: %s" % (value, e)
        )


def validate_io(name, type, value, is_optional, is_list, is_flag, options):
    if type and value:
        validate_io_value(
            name=name,
            type=type,
            value=value,
            default=None,
            is_list=is_list,
            is_optional=is_optional,
            options=options,
        )

    if not is_optional and value:
        raise ValidationError(
            "IO `{}` is not optional and has default value `{}`. "
            "Please either make it optional or remove the default value.".format(
                name, value
            )
        )

    if is_flag and type != types.BOOL:
        raise ValidationError(
            "IO type `{}` cannot be a flag, it must be of type `{}`".format(
                type, types.BOOL
            )
        )


class IOSchema(BaseCamelSchema):
    name = fields.Str(
        required=True, validate=validate.NoneOf(IO_NAME_BLACK_LIST, error=IO_NAME_ERROR)
    )
    description = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True, validate=validate.OneOf(types.VALUES))
    value = fields.Raw(allow_none=True)
    is_optional = fields.Bool(allow_none=True)
    is_list = fields.Bool(allow_none=True)
    is_flag = fields.Bool(allow_none=True)
    arg_format = fields.Str(allow_none=True)
    delay_validation = fields.Bool(allow_none=True)
    options = fields.List(fields.Raw(), allow_none=True)
    connection = fields.Str(allow_none=True)
    to_init = fields.Bool(allow_none=True)
    to_env = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return V1IO

    @validates_schema
    @check_partial
    def validate_io(self, values, **kwargs):
        validate_io(
            name=values.get("name"),
            type=values.get("type"),
            value=values.get("value"),
            is_list=values.get("is_list"),
            is_optional=values.get("is_optional"),
            is_flag=values.get("is_flag"),
            options=values.get("options"),
        )


class V1IO(BaseConfig, polyaxon_sdk.V1IO):
    """Each Component may have its own inputs and outputs.
    The inputs and outputs describe the expected parameters to pass to the component
    and their types. In the context of a DAG,
    inputs and outputs types are used to validate the flow of information
    going from one operation to another.

    The final value of an input/output can be resolved
    from [params](/docs/core/specification/params/), or from other values in
    the [context](/docs/core/context/).

    Examples:
     * A build component may have a git repository as input and a container image as output.
     * A training component may have a container image, data path,
       and some hyperparameters as input and a list of metrics and artifacts as outputs.

    An input/output section includes a name, a description, a type to check the value passed,
    a flag to tell if the input/output is optional, and a default value if it's optional.

    Sometimes users prefer to pass a param to the `command` or `args`
    section only if the value is not null. Polyaxon provides a way to do that using
    `{{ params.PARAM_NAME.as_arg }}`,
    this will be empty if the value is null or `--PARAM_NAME=value` if the value is not null.
    If the value is of type bool, it will be `--PARAM_NAME`.
    It's also possible to control how the param should be
    converted to an argument using the `arg_format`.

    To learn how to pass valid values,
    please check the [param section](/docs/core/specification/params/).

    Args:
        name: str
        description: str, optional
        type: str, one of: [any, int, float, bool, str, dict, dict_of_dicts, uri, auth, list, gcs, s3, wasb, dockerfile, git, image, event, artifacts, path, metric, metadata, date, datetime]  # noqa
        value: any, optional
        is_optional: bool, optional
        is_list: bool, optional
        is_flag: bool, optional
        arg_format: str, optional
        delay_validation: bool, optional
        options: List[any], optional
        connection: str, optional
        to_init: bool, optional
        to_env: str, optional

    ## YAML usage

    ```yaml
    >>> inputs:
    >>>   - name: loss
    >>>     type: str
    >>>     isOptional: true
    >>>     value: MeanSquaredError
    >>>   - name: preprocess
    >>>     type: bool
    >>> outputs:
    >>>   - name: accuracy
    >>>     type: float
    >>>   - name: outputs-path
    >>>     type: path
    ```

    ## Python usage

    ```python
    >>> from polyaxon import types
    >>> from polyaxon.polyflow import V1IO
    >>> inputs = [
    >>>     V1IO(
    >>>         name="loss",
    >>>         type=types.STR,
    >>>         description="Loss to use for training my model",
    >>>         is_optional=True,
    >>>         value="MeanSquaredError"
    >>>     ),
    >>>     V1IO(
    >>>         name="preprocess",
    >>>         type=types.BOOL,
    >>>         description="A flag to preprocess data before training",
    >>>     )
    >>> ]
    >>> outputs = [
    >>>     V1IO(
    >>>         name="accuracy",
    >>>         type=types.FLOAT,
    >>>     ),
    >>>     V1IO(
    >>>         name="outputs-path",
    >>>         type=types.PATH,
    >>>     )
    >>> ]
    ```

    These inputs/outputs declarations can be used to pass values to our program:

    ```bash
     ... --loss={{ loss }} {{ params.preprocess.as_arg }}
    ```

    ## Fields

    ### name

    The input/output name. The name must be a valid slug, and cannot include dots `.`.

    ```yaml
    >>> inputs:
    >>>   - name: learning_rate
    ```

    ### description

    An optional description for the input/output.

    ```yaml
    >>> inputs:
    >>>   - name: learning_rate
    >>>     description: A short description about this input
    ```

    ### type

    The type of the input/output. The type will be used to validate the value

    ```yaml
    >>> inputs:
    >>>   - name: learning_rate
    >>>     description: A short description about this input
    >>>     type: float
    ```

    for more details about composite type validation and schema,
    please check the [types section](/docs/core/specification/types/),
    possible types:
        * ANY: "any"
        * INT: "int"
        * FLOAT: "float"
        * BOOL: "bool"
        * STR: "str"
        * DICT: "dict"
        * DICT_OF_DICTS: "dict_of_dicts"
        * URI: "uri"
        * AUTH: "auth"
        * LIST: "list"
        * GCS: "gcs"
        * S3: "s3"
        * WASB: "wasb"
        * DOCKERFILE: "dockerfile"
        * GIT: "git"
        * IMAGE: "image"
        * EVENT: "event"
        * ARTIFACTS: "artifacts"
        * PATH: "path"
        * METRIC: "metric"
        * METADATA: "metadata"
        * DATE: "date"
        * DATETIME: "datetime"

    ### value

    If an input is optional you should assign it a value.
    If an output is optional you can assign it a value.

    ```yaml
    >>> inputs:
    >>>   - name: learning_rate
    >>>     description: A short description about this input
    >>>     type: float
    >>>     value: 1.1
    ```

    ### isOptional

    A flag to tell if an input/output is optional.

    ```yaml
    >>> inputs:
    >>>   - name: learning_rate
    >>>     description: A short description about this input
    >>>     type: float
    >>>     value: 1.1
    >>>     isOptional: true
    ```

    ### isList

    A flag to tell if an input/output is a list of the type passed.

    ```yaml
    >>> inputs:
    >>>   - name: learning_rates
    >>>     type: float
    >>>     isList: true
    ```

    In this case the input name `learning_rates` will expect a value of type `List[float]`,
    e.g. [0.1 0.01, 0.0001]

    ### argFormat

    A key to control how to convert an input/output to a CLI argument if the value is not null,
    the default behavior:

     * For bool type: If the resolved value of the input is True,
       `"{{ params.PARAM_NAME.as_arg }}"` will be resolved to `"--PARAM_NAME"`
       otherwise it will be an empty string `""`.
     * For non-bool types: If the resolved value of the input is not null,
       `"{{ params.PARAM_NAME.as_arg }}"` will be resolved to `"--PARAM_NAME=value"`
       otherwise it will be an empty string `""`.

    Let's look at the flowing example:

    ```yaml
    >>> inputs:
    >>>   - name: lr
    >>>     type: float
    >>>   - name: check
    >>>     type: bool
    ```

    **This manifest**:

    ```yaml
    >>> container:
    >>>    command: ["{{ lr }}", "{{ check }}"]
    ```

    Will be transformed to:

    ```yaml
    >>> container:
    >>>    command: ["0.01", "true"]
    ```

    **This manifest**:

    ```yaml
    >>> container:
    >>>    command: ["{{ params.lr.as_arg }}", "{{ params.check.as_arg }}"]
    ```

    Will be transformed to:

    ```yaml
    >>> container:
    >>>    command: ["--lr=0.01", "--check"]
    ```

    Changing the behavior with `argFormat`:

    ```yaml
    >>> inputs:
    >>>   - name: lr
    >>>     type: float
    >>>     argFormat: "lr={{ lr }}"
    >>>   - name: check
    >>>     type: bool
    >>>     argFormat: "{{ 1 if check else 0 }}"
    ```

    **This manifest**:

    ```yaml
    >>> container:
    >>>    command: ["{{ params.lr.as_arg }}", "{{ params.check.as_arg }}"]
    ```

    Will be transformed to:

    ```yaml
    >>> container:
    >>>    command: ["lr=0.01", "1"]
    ```

    ### delayValidation

    A flag to tell if an input/output should not be
    validated at compilation or resolution time.

    This flag is enabled by default for outputs, since they can only be
    resolved after or during the run. To request validation at compilation time for outputs,
    you need to set this flag to `False`.

    ### connection

    A connection to use with the input/outputs.

    ### toInit

    If True, it will be converted to an init container.

    ### toEnv

    > **N.B**: Requires Polyaxon CLI and Polyaxon Agent/CE version `>= 1.12`

    If passed, it will be converted automatically to an environment variable.

    ```yaml
    >>> inputs:
    >>>   - name: learning_rate
    >>>     type: float
    >>>     value: 1.1
    >>>     toEnv: MY_LEARNING_RATE
    ```

    ### options

    Options allow to pass a list of values that will be used to validate any passed params.

    ```yaml
    >>> inputs:
    >>>   - name: learning_rate
    >>>     description: A short description about this input
    >>>     type: float
    >>>     value: 1.1
    >>>     options: [1.1, 2.2, 3.3]
    ```

    If you pass the value `4.4` for the learning rate it will raise a validation error.

    ## Example


    ```yaml
    >>> version: 1.1
    >>> kind: component
    >>> inputs:
    >>>   - name: batch_size
    >>>     description: batch size
    >>>     isOptional: true
    >>>     value: 128
    >>>     type: int
    >>>   - name: num_steps
    >>>     isOptional: true
    >>>     default: 500
    >>>     type: int
    >>>   - name: learning_rate
    >>>     isOptional: true
    >>>     default: 0.001
    >>>     type: float
    >>>   - name: dropout
    >>>     isOptional: true
    >>>     default: 0.25
    >>>     type: float
    >>>   - name: num_epochs
    >>>     isOptional: true
    >>>     default: 1
    >>>     type: int
    >>>   - name: activation
    >>>     isOptional: true
    >>>     default: relu
    >>>     type: str
    >>> run:
    >>>   kind: job
    >>>   image: foo:bar
    >>>   container:
    >>>     command: [python3, model.py]
    >>>     args: [
    >>>         "--batch_size={{ batch_size }}",
    >>>         "--num_steps={{ num_steps }}",
    >>>         "--learning_rate={{ learning_rate }}",
    >>>         "--dropout={{ dropout }",
    >>>         "--num_epochs={{ num_epochs }}",
    >>>         "--activation={{ activation }}"
    >>>     ]
    ```

    ### Running a typed component using the CLI

    Using the Polyaxon CLI we can now run this component and override the inputs' default values:

    ```bash
    polyaxon run -f polyaxonfile.yaml -P activation=sigmoid -P dropout=0.4
    ```

    This will generate a manifest and will replace the params passed and validated against the inputs' types.

    ### Required inputs

    In the example all inputs are optional.
    If we decide for instance to make the activation required:

    ````yaml
    >>> ...
    >>> inputs:
    >>>   ...
    >>>   - name: activation
    >>>     type: str
    >>>   ...
    ...
    ````

    By changing this input, polyaxon can not run this component without passing the activation:


    ```bash
    polyaxon run -f polyaxonfile.yaml -P activation=sigmoid
    ```
    """

    SCHEMA = IOSchema
    IDENTIFIER = "io"
    REDUCED_ATTRIBUTES = [
        "description",
        "type",
        "value",
        "isOptional",
        "isFlag",
        "isList",
        "argFormat",
        "delayValidation",
        "options",
        "connection",
        "toInit",
        "toEnv",
    ]

    def __init__(
        self,
        name=None,
        description=None,
        type=None,
        value=None,
        is_optional=None,
        is_list=None,
        is_flag=None,
        arg_format=None,
        delay_validation=None,
        options=None,
        connection=None,
        to_init=None,
        to_env=None,
        iotype=None,
        local_vars_configuration=None,
    ):
        # Backward compatibility
        if iotype:
            print(
                "`iotype` was deprecated in favor of `type`, "
                "and will be removed in future releases."
            )
        type = type or iotype
        super().__init__(
            name=name,
            description=description,
            type=type,
            value=value,
            is_optional=is_optional,
            is_list=is_list,
            is_flag=is_flag,
            arg_format=arg_format,
            delay_validation=delay_validation,
            options=options,
            connection=connection,
            to_init=to_init,
            to_env=to_env,
            local_vars_configuration=local_vars_configuration,
        )

    def validate_value(self, value: Any, parse: bool = True):
        if self.type is None:
            return value

        return validate_io_value(
            name=self.name,
            type=self.type,
            value=value,
            default=self.value,
            is_list=self.is_list,
            is_optional=self.is_optional,
            options=self.options,
            parse=parse,
        )

    def get_repr_from_value(self, value):
        """A string representation that is used to create hash cache"""
        value = self.validate_value(value=value, parse=False)
        io_dict = self.to_light_dict(include_attrs=["name", "type"])
        io_dict["value"] = value
        return io_dict

    def get_repr(self):
        """A string representation that is used to create hash cache"""
        io_dict = self.to_light_dict(include_attrs=["name", "type", "value"])
        return io_dict
