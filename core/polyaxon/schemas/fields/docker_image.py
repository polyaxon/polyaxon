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

from marshmallow import ValidationError

from polyaxon.schemas.fields.params import PARAM_REGEX


def validate_image(image, allow_none=False):
    if not image:
        if allow_none:
            return
        else:
            raise ValidationError("Image is required")
    param = PARAM_REGEX.search(image)
    if param:
        return
    if " " in image:
        raise ValidationError("Invalid docker image `{}`".format(image))
    tagged_image = image.split(":")
    if len(tagged_image) > 3:
        raise ValidationError("Invalid docker image `{}`".format(image))
    if len(tagged_image) == 3 and (
        "/" not in tagged_image[1] or tagged_image[1].startswith("/")
    ):
        raise ValidationError("Invalid docker image `{}`".format(image))
