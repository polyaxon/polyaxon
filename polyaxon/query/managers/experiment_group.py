from typing import Any

from hestia.list_utils import to_list

from django.db.models import Q

from query.builder import (
    ArrayCondition,
    CallbackCondition,
    ComparisonCondition,
    DateTimeCondition,
    ValueCondition
)
from query.managers.base import BaseQueryManager
from query.parser import parse_datetime_operation, parse_scalar_operation, parse_value_operation


def _search_algorithm_condition(queryset: Any, params: Any, negation: bool) -> Any:
    params = to_list(params)
    updated_params = []
    for param in params:
        param = param.lower()
        if param == 'random':
            param = 'random_search'
        if param == 'grid':
            param = 'grid_search'
        updated_params.append(param)
    if len(params) == 1:
        query = Q(hptuning__has_key=updated_params[0])
    else:
        query = Q(hptuning__has_any_keys=updated_params)

    if negation:
        query = ~query

    return queryset.filter(query)


class ExperimentGroupQueryManager(BaseQueryManager):
    NAME = 'experiment_group'
    FIELDS_PROXY = {
        'status': 'status__status',
        'concurrency': 'hptuning__concurrency'
    }
    PARSERS_BY_FIELD = {
        # Id
        'id': parse_value_operation,
        # Dates
        'created_at': parse_datetime_operation,
        'updated_at': parse_datetime_operation,
        'started_at': parse_datetime_operation,
        'finished_at': parse_datetime_operation,
        # Name
        'name': parse_value_operation,
        # User
        'user': parse_value_operation,
        # Status
        'status': parse_value_operation,
        # Project
        'project': parse_value_operation,
        # Tags
        'tags': parse_value_operation,
        # hptuning
        'search_algorithm': parse_value_operation,
        'concurrency': parse_scalar_operation,
    }
    CONDITIONS_BY_FIELD = {
        # Id
        'id': ValueCondition,
        # Dates
        'created_at': DateTimeCondition,
        'updated_at': DateTimeCondition,
        'started_at': DateTimeCondition,
        'finished_at': DateTimeCondition,
        # Name
        'name': ValueCondition,
        # User
        'user': ValueCondition,
        # Status
        'status': ValueCondition,
        # Project
        'project': ValueCondition,
        # Tags
        'tags': ArrayCondition,
        # hptuning
        'search_algorithm': CallbackCondition(_search_algorithm_condition),
        'concurrency': ComparisonCondition,
    }
