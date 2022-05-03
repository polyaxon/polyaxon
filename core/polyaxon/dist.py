#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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


LOCAL = "local"
SANDBOX = "sandbox"
CE = "ce"
EE = "ee"


def is_local(value: str):
    return LOCAL == value


def is_sandbox(value: str):
    return SANDBOX == value


def is_ce(value: str):
    return CE == value


def is_community(value: str):
    return value is None or value in {LOCAL, SANDBOX, CE}


def is_ee(value: str):
    return EE == value
