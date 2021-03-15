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

from polyaxon import types
from polyaxon.k8s.k8s_schemas import V1Container
from polyaxon.schemas.types import V1GitType
from polyaxon.polyflow import V1Component, V1Init, V1IO, V1Job

"""
This is the same Polyaxonfile as in typed.yaml using the Python library.

Note: Running this file using CLI is similar as well:

```bash
polyaxon run -pm experimentation/typed.py:component -P epochs=5 -l
```

 * -pm: --python-module
"""

inputs = [
    V1IO(name="conv1_size", type=types.INT, value=32, is_optional=True),
    V1IO(name="conv2_size", type=types.INT, value=64, is_optional=True),
    V1IO(name="dropout", type=types.FLOAT, value=0.2, is_optional=True),
    V1IO(name="hidden1_size", type=types.INT, value=500, is_optional=True),
    V1IO(name="conv_activation", type=types.STR, value="relu", is_optional=True),
    V1IO(name="dense_activation", type=types.STR, value="relu", is_optional=True),
    V1IO(name="optimizer", type=types.STR, value="adam", is_optional=True),
    V1IO(name="learning_rate", type=types.FLOAT, value=0.01, is_optional=True),
    V1IO(name="epochs", type=types.INT),
]

outputs = [
    V1IO(name="loss", type=types.FLOAT),
    V1IO(name="accuracy", type=types.FLOAT),
]

job = V1Job(
    init=[V1Init(git=V1GitType(url="https://github.com/polyaxon/polyaxon-quick-start"))],
    container=V1Container(
        image="polyaxon/polyaxon-quick-start",
        working_dir="{{ globals.artifacts_path }}",
        command=["python3", "polyaxon-quick-start/model.py"],
        args=[
          "--conv1_size={{ conv1_size }}",
          "--conv2_size={{ conv2_size }}",
          "--dropout={{ dropout }}",
          "--hidden1_size={{ hidden1_size }}",
          "--optimizer={{ optimizer }}",
          "--conv_activation={{ conv_activation }}",
          "--dense_activation={{ dense_activation }}",
          "--learning_rate={{ learning_rate }}",
          "--epochs={{ epochs }}"
        ]
    ),
)

component = V1Component(
    name="typed-experiment",
    description="experiment with inputs",
    tags=["examples"],
    inputs=inputs,
    outputs=outputs,
    run=job,
)
