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

from marshmallow import ValidationError as MarshmallowValidationError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from polyaxon.polyboard.artifacts import V1RunArtifact
from polyaxon.utils.list_utils import to_list


def create(view, request, *args, **kwargs):
    if not request.data:
        raise ValidationError("Received no artifacts.")

    data = to_list(request.data)
    try:
        [V1RunArtifact(r) for r in data]
    except MarshmallowValidationError as e:
        raise ValidationError(e)

    view.audit(request, *args, **kwargs, artifacts=data)
    return Response(status=status.HTTP_201_CREATED)
