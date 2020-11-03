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

import polyaxon_sdk

from marshmallow import fields

from polyaxon.polyflow.params import ParamSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class ActionSchema(BaseCamelSchema):
    hub_ref = fields.Str(required=True)
    label = fields.Str(allow_none=True)
    many = fields.Bool(allow_none=True)
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(ParamSchema), allow_none=True
    )
    run_patch = fields.Dict(keys=fields.Str(), values=fields.Raw(), allow_none=True)

    @staticmethod
    def schema_config():
        return V1Action


class V1Action(BaseConfig, polyaxon_sdk.V1Action):
    """In order to extend Polyaxon UI and CLI, you can set actions on your operations.
    Every action is a reference to a component that can be executed
    based on the context of the operation where it's defined

    **Use cases**

     * A training job can have Tensorboard as an action, this will automatically
    add a UI button in the dashboard so that you can start a Tensorboard based
    on the outputs of the run.
     * Streamlit app that can consume the outputs of some specific jobs.
     * Papermill for parametrized notebooks.


    **UI**

    Polyaxon UI will display up-to 3 actions in the run's dropdown,
    and allow users to view all of them (if there are more than 3),
    users interacting with the dashboard can start an action by clicking the buttons.

    **CLI**

    Polyaxon CLI will also allow to start actions in a much usable than passing
    params to another component, and it will make the CLI much usable,
    for instance, this is the behavior for starting a Keras operation and running a Tensorboard:

    ```bash
    polyaxon run -f polyaxonfile.yaml
    polyaxon run --hub tensorboard --uuid UUID
    ```

    By adding actions to a specific training component,
    the CLI can leverage the context of a run to resolve the parameters automatically:

    ```bash
    polyaxon run -f polyaxonfile.yaml
    polyaxon ops start --action=tensorboard
    ```

    **Comparison**

    Actions will be indexed as special tags to allow users to filter all
    runs based on an action or multiple.
    For example filtering all runs with a Tensorboard action,
    the table comparison will also provide an action for the group.

     Args:
         hub_ref: str
         label: str, optional
         many: str, bool
         params: Dict[str, [V1Param](/docs/core/specification/params/)], optional
         run_patch: Dict, optional

    ## YAML usage

    ```yaml
    >>> notification:
    >>>   hubRef: tensorboard
    >>>   label: "Start Tensorboard"
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1Action
    >>> action = V1Action(
    >>>     hub_ref="tensorboard",
    >>>     label="Start Tensorboard",
    >>> )
    ```

    ## Fields

    ### hubRef

    Polyaxon provides a [Component Hub](/docs/management/component-hub/)
    for hosting versioned components with an access control system to improve
    the productivity of your team.

    To trigger a hook based on a component hosted on Polyaxon Component Hub, you can use `hubRef`

    ```yaml
    >>> action:
    >>>   hubRef: slack:v1
    ...
    ```

    Or custom hook component

    ```yaml
    >>> action:
    >>>   hubRef:  my-component:dev
    ...
    ```

    ### label

    The UI label to use for the button, if not provided it will default to the component's name.

    ```yaml
    >>> action:
    >>>   label: "Start My App"
    ...
    ```

    ### many

    This is an optional boolean to tell Polyaxon if this action
    is expected to act on a single run or multiple runs.

    ```yaml
    >>> action:
    >>>   hubRef: tensorboard:multi-runs
    >>>   many: true
    ```

    ### params

    The [params](/docs/core/specification/params/) to pass if the handler requires extra params,
    they will be validated against the inputs/outputs.
    If a parameter is passed and the component does not define a corresponding inputs/outputs,
    a validation error will be raised unless the param has the contextOnly flag enabled.

    ```yaml
    >>> action:
    >>>   params:
    >>>     param1: {value: 1.1}
    >>>     param2: {value: test}
    >>>   ...
    ```

    ### runPatch

    Component's environment section can be [patched](/docs/core/specification/operation/#runPatch).

    Example patching the container resources:

    ```yaml
    >>> action:
    >>>   runPatch:
    >>>     container:
    >>>       resources:
    >>>         limits:
    >>>           cpu: 50m
    ```
    """

    IDENTIFIER = "action"
    SCHEMA = ActionSchema
    REDUCED_ATTRIBUTES = [
        "hubRef",
        "label",
        "many",
        "params",
        "runPatch",
    ]
