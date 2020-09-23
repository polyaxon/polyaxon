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

from typing import Any, Iterable, Union

from polyaxon.utils.bool_utils import to_bool
from polyaxon.utils.list_utils import to_list
from polycommon import live_state


def archived_condition(
    params: Union[str, Iterable],
    negation: bool,
    query_backend: Any,
    timezone: str = None,
    queryset: Any = None,
) -> Any:
    """
    Example:
        >>>  {"archived": CallbackCondition(callback_conditions.archived_condition)}
    """
    params = to_list(params)
    if len(params) == 1 and to_bool(params[0]) is True:
        return (
            queryset.filter(live_state=live_state.STATE_ARCHIVED)
            if queryset
            else query_backend(live_state=live_state.STATE_ARCHIVED)
        )
    return query_backend(live_state=live_state.STATE_LIVE)


def independent_condition(
    params: Union[str, Iterable],
    negation: bool,
    query_backend: Any,
    timezone: str = None,
    queryset: Any = None,
) -> Any:
    params = to_list(params)
    if len(params) == 1 and to_bool(params[0]) is True:
        return queryset.filter(experiment_group__isnull=True)
    return queryset


def metric_condition(
    queryset: Any,
    params: Union[str, Iterable],
    negation: bool,
    query_backend: Any,
    timezone: str = None,
) -> Any:
    params = to_list(params)
    if len(params) == 1 and to_bool(params[0]) is True:
        return queryset.filter(metric_annotations__name=True)
    return queryset
