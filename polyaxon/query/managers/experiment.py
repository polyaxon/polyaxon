from query.builder import DateTimeCondition, ValueCondition, ComparisonCondition
from query.managers.base import BaseQueryManager
from query.parser import parse_datetime_operation, parse_value_operation


class ExperimentQueryManager(BaseQueryManager):
    NAME = 'experiment_query_manager'
    FIELDS_PROXY = {
        'metric': 'metric__values',
        'started_at': 'status__created_at',
        'finished_at': 'status__finished_at',
    }
    PARSERS_BY_FIELD = {
        # Dates
        'created_at': parse_datetime_operation,
        'updated_at': parse_datetime_operation,
        'started_at': parse_datetime_operation,
        'finished_at': parse_datetime_operation,
        # User
        'user': parse_value_operation,
        # Groups
        'experiment_group': parse_value_operation,
        # Declarations
        'declarations': parse_value_operation,
        # Tags
        'tags': parse_value_operation,
        # Metrics
        'metric': parse_value_operation,
    }
    CONDITIONS_BY_FIELD = {
        # Dates
        'created_at': DateTimeCondition,
        'updated_at': DateTimeCondition,
        'started_at': DateTimeCondition,
        'finished_at': DateTimeCondition,
        # User
        'user': ValueCondition,
        # Groups
        'experiment_group': ValueCondition,
        # Declarations
        'declarations': ValueCondition,
        # Tags
        'tags': ValueCondition,
        # Metrics
        'metric': ComparisonCondition,
    }
