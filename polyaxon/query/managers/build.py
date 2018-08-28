from query.builder import ArrayCondition, DateTimeCondition, ValueCondition
from query.managers.base import BaseQueryManager
from query.parser import parse_datetime_operation, parse_value_operation


class BuildQueryManager(BaseQueryManager):
    NAME = 'build'
    FIELDS_PROXY = {
        'status': 'status__status',
        'commit': 'code_reference__commit',
    }
    PARSERS_BY_FIELD = {
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
        # Commit
        'commit': parse_value_operation,
    }
    CONDITIONS_BY_FIELD = {
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
        # Commit
        'commit': ValueCondition,
    }
