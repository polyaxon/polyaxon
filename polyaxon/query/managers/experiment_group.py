from django.db.models import Q
from polyaxon_schemas.utils import to_list

from query.builder import ArrayCondition, DateTimeCondition, ValueCondition, CallbackCondition, \
    ComparisonCondition
from query.managers.base import BaseQueryManager
from query.parser import parse_datetime_operation, parse_value_operation, parse_scalar_operation


def _search_algorithm_condition(queryset, params, negation):
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
        # Dates
        'created_at': parse_datetime_operation,
        'updated_at': parse_datetime_operation,
        'started_at': parse_datetime_operation,
        'finished_at': parse_datetime_operation,
        # User
        'user': parse_value_operation,
        # Status
        'status': parse_value_operation,
        # Tags
        'tags': parse_value_operation,
        # hptuning
        'search_algorithm': parse_value_operation,
        'concurrency': parse_scalar_operation,
    }
    CONDITIONS_BY_FIELD = {
        # Dates
        'created_at': DateTimeCondition,
        'updated_at': DateTimeCondition,
        'started_at': DateTimeCondition,
        'finished_at': DateTimeCondition,
        # User
        'user': ValueCondition,
        # Status
        'status': ValueCondition,
        # Tags
        'tags': ArrayCondition,
        # hptuning
        'search_algorithm': CallbackCondition(_search_algorithm_condition),
        'concurrency': ComparisonCondition,
    }
