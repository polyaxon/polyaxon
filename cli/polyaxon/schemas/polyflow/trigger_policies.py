#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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


class TriggerPolicy(object):
    ALL_SUCCEEDED = "all_succeeded"
    ALL_FAILED = "all_failed"
    ALL_DONE = "all_done"
    ONE_SUCCEEDED = "one_succeeded"
    ONE_FAILED = "one_failed"
    ONE_DONE = "one_done"

    VALUES = {ALL_SUCCEEDED, ALL_FAILED, ALL_DONE, ONE_SUCCEEDED, ONE_FAILED, ONE_DONE}
    CHOICES = (
        (ALL_SUCCEEDED, ALL_SUCCEEDED),
        (ALL_FAILED, ALL_FAILED),
        (ALL_DONE, ALL_DONE),
        (ONE_SUCCEEDED, ONE_SUCCEEDED),
        (ONE_FAILED, ONE_FAILED),
        (ONE_DONE, ONE_DONE),
    )


class StatusTriggerPolicy(object):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    DONE = "done"

    VALUES = {SUCCEEDED, FAILED, DONE}
    CHOICES = ((SUCCEEDED, SUCCEEDED), (FAILED, FAILED), (DONE, DONE))


class ExpressionTriggerPolicy(object):
    EQ = "eq"
    NE = "ne"
    IS_NULL = "isnull"
    NOT_NULL = "not_null"

    VALUES = {EQ, NE}
    CHOICES = ((EQ, EQ), (NE, NE), (IS_NULL, IS_NULL), (NOT_NULL, NOT_NULL))
