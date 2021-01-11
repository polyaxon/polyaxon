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

import base64


def encode(value):
    return base64.b64encode(value.encode("utf-8")).decode("utf-8")


def decode(value):
    return base64.b64decode(value).decode("utf-8")


def urlsafe_b64decode(b64string):
    if isinstance(b64string, str):
        b64string = bytes(b64string, "utf-8")
    padded = b64string + b"=" * (4 - len(b64string) % 4)
    payload = base64.urlsafe_b64decode(padded)
    try:
        return payload.decode("utf-8")
    except:
        return payload
