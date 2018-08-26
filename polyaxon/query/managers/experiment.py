from polyaxon_schemas.utils import to_list

from libs.utils import to_bool
from query.builder import (
    ArrayCondition,
    CallbackCondition,
    ComparisonCondition,
    DateTimeCondition,
    ValueCondition,
)
from query.managers.base import BaseQueryManager
from query.parser import parse_datetime_operation, parse_scalar_operation, parse_value_operation


def _indepenent_condition(queryset, params, negation):
    params = to_list(params)
    if len(params) == 1 and to_bool(params[0]) is True:
        return queryset.filter(experiment_group__isnull=True)
    return queryset


class ExperimentQueryManager(BaseQueryManager):
    NAME = 'experiment'
    FIELDS_PROXY = {
        'metric': 'metric__values',
        'status': 'status__status',
        'group': 'experiment_group',
        'build': 'build_job',
        'commit': 'code_reference__commit',
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
        # Groups
        'group': parse_value_operation,
        # Builds
        'build': parse_value_operation,
        # Commit
        'commit': parse_value_operation,
        # Declarations
        'declarations': parse_value_operation,
        # Tags
        'tags': parse_value_operation,
        # Metrics
        'metric': parse_scalar_operation,
        # Idependent
        'independent': parse_value_operation,
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
        # Groups
        'group': ValueCondition,
        # Builds
        'build': ValueCondition,
        # Commit
        'commit': ValueCondition,
        # Declarations
        'declarations': ValueCondition,
        # Tags
        'tags': ArrayCondition,
        # Metrics
        'metric': ComparisonCondition,
        # Independent
        'independent': CallbackCondition(_indepenent_condition),
    }
